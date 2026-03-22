"""General API routes - Chat with LLM, calculators."""

import math
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func
from pydantic import BaseModel
from typing import Optional
from config import settings

from models.database import get_db
from models.chat import ChatHistory
from web.sanitize import sanitize_text

router = APIRouter()


class ChatMessage(BaseModel):
    message: str
    model: Optional[str] = None
    system_prompt: Optional[str] = None


# ---- Chat History Endpoints ----

@router.get("/chat/history")
async def get_chat_history(limit: int = 50, db: AsyncSession = Depends(get_db)):
    """Get recent chat messages (oldest first for display)."""
    query = (
        select(ChatHistory)
        .order_by(ChatHistory.id.desc())
        .limit(limit)
    )
    result = await db.execute(query)
    messages = result.scalars().all()
    # Return oldest first for chronological display
    return {"messages": [m.to_dict() for m in reversed(messages)]}


@router.delete("/chat/history")
async def clear_chat_history(db: AsyncSession = Depends(get_db)):
    """Clear all chat history (new conversation)."""
    await db.execute(delete(ChatHistory))
    await db.commit()
    return {"status": "ok", "message": "Histórico limpo"}


@router.post("/chat")
async def chat(data: ChatMessage, db: AsyncSession = Depends(get_db)):
    """Send a message to the AI agent with conversation context."""
    model = data.model or settings.default_model
    system = data.system_prompt or (
        "Você é um assistente especializado em oftalmologia clínica. "
        "Responda em português brasileiro. Seja preciso e cite referências quando possível. "
        "Sempre inclua o aviso: as informações não substituem consulta médica."
    )

    # Load last 10 messages for context (5 pairs of user/assistant)
    context_query = (
        select(ChatHistory)
        .order_by(ChatHistory.id.desc())
        .limit(10)
    )
    result = await db.execute(context_query)
    context_messages = list(reversed(result.scalars().all()))

    # Sanitize and validate input
    clean_message = sanitize_text(data.message, max_length=4000)
    if not clean_message:
        raise HTTPException(status_code=400, detail="Mensagem não pode estar vazia")

    # Build messages array with context
    messages = [{"role": m.role, "content": m.content} for m in context_messages]
    messages.append({"role": "user", "content": clean_message})

    # Save user message to history
    db.add(ChatHistory(role="user", content=clean_message))
    await db.flush()

    # Try providers in order of preference
    try:
        if settings.openrouter_api_key:
            response = await _chat_openrouter(messages, model, system)
        elif settings.anthropic_api_key:
            response = await _chat_anthropic(messages, model, system)
        elif settings.openai_api_key:
            response = await _chat_openai(messages, model, system)
        else:
            response = {
                "response": (
                    "Nenhuma chave de API configurada. "
                    "Defina OPENROUTER_API_KEY, ANTHROPIC_API_KEY ou OPENAI_API_KEY no arquivo .env"
                ),
                "model": "not-configured",
                "provider": None,
            }

        # Save assistant response to history
        db.add(ChatHistory(
            role="assistant",
            content=response["response"],
            model=response.get("model"),
            provider=response.get("provider"),
        ))
        await db.commit()

        return response

    except Exception as e:
        await db.rollback()
        raise


async def _chat_openrouter(messages: list, model: str, system: str) -> dict:
    """Chat via OpenRouter (supports many models)."""
    import httpx

    api_messages = [{"role": "system", "content": system}] + messages

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.openrouter_api_key}",
                "Content-Type": "application/json",
            },
            json={"model": model, "messages": api_messages},
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        data = resp.json()
        return {
            "response": data["choices"][0]["message"]["content"],
            "model": data.get("model", model),
            "provider": "openrouter",
        }


async def _chat_anthropic(messages: list, model: str, system: str) -> dict:
    """Chat via Anthropic API (Claude)."""
    import httpx

    anthropic_model = model
    if "/" in model:
        anthropic_model = model.split("/")[-1]

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": settings.anthropic_api_key,
                "anthropic-version": "2023-06-01",
                "Content-Type": "application/json",
            },
            json={
                "model": anthropic_model,
                "max_tokens": 2048,
                "system": system,
                "messages": messages,
            },
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        data = resp.json()
        return {
            "response": data["content"][0]["text"],
            "model": data.get("model", anthropic_model),
            "provider": "anthropic",
        }


async def _chat_openai(messages: list, model: str, system: str) -> dict:
    """Chat via OpenAI API (GPT)."""
    import httpx

    openai_model = model
    if "/" in model:
        openai_model = model.split("/")[-1]
    if not openai_model.startswith(("gpt-", "o1", "o3", "o4")):
        openai_model = "gpt-4o"

    api_messages = [{"role": "system", "content": system}] + messages

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.openai_api_key}",
                "Content-Type": "application/json",
            },
            json={"model": openai_model, "messages": api_messages},
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        data = resp.json()
        return {
            "response": data["choices"][0]["message"]["content"],
            "model": data.get("model", openai_model),
            "provider": "openai",
        }


@router.get("/calculators/iol")
async def iol_calculator(al: float = 23.5, k1: float = 43.0, k2: float = 44.0, target: float = -0.5):
    """IOL power calculation (simplified SRK/T)."""
    avg_k = (k1 + k2) / 2
    a_constant = 118.7
    iol_power = a_constant - (2.5 * al) - (0.9 * avg_k)

    return {
        "input": {"axial_length": al, "k1": k1, "k2": k2, "target_refraction": target},
        "result": {
            "iol_power": round(iol_power, 2),
            "formula": "SRK/T (simplificado)",
            "disclaimer": "Apenas para fins educacionais. Use software de biometria certificado para decisões clínicas.",
        },
    }


@router.get("/calculators/va-convert")
async def va_converter(snellen: str = "20/40"):
    """Visual acuity conversion."""
    parts = snellen.split("/")
    if len(parts) != 2:
        return {"error": "Formato deve ser como 20/40"}

    try:
        numerator, denominator = int(parts[0]), int(parts[1])
    except ValueError:
        return {"error": "Valores devem ser numéricos"}

    decimal_va = numerator / denominator
    logmar = round(-1 * math.log10(decimal_va), 2)

    return {
        "snellen": snellen,
        "decimal": round(decimal_va, 3),
        "logmar": logmar,
        "category": _classify_va(logmar),
    }


def _classify_va(logmar: float) -> str:
    if logmar <= 0.0:
        return "Normal (20/20 ou melhor)"
    elif logmar <= 0.3:
        return "Perda visual leve"
    elif logmar <= 0.5:
        return "Perda visual moderada"
    elif logmar <= 1.0:
        return "Perda visual severa"
    else:
        return "Perda visual profunda / Cegueira legal"
