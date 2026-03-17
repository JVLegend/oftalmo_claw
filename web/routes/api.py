"""General API routes - Chat with LLM, calculators."""

import math
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from config import settings

router = APIRouter()


class ChatMessage(BaseModel):
    message: str
    model: Optional[str] = None
    system_prompt: Optional[str] = None


@router.post("/chat")
async def chat(data: ChatMessage):
    """Send a message to the AI agent. Supports OpenRouter, Anthropic, and OpenAI."""
    model = data.model or settings.default_model
    system = data.system_prompt or (
        "Você é um assistente especializado em oftalmologia clínica. "
        "Responda em português brasileiro. Seja preciso e cite referências quando possível. "
        "Sempre inclua o aviso: as informações não substituem consulta médica."
    )

    # Try providers in order of preference
    if settings.openrouter_api_key:
        return await _chat_openrouter(data.message, model, system)
    elif settings.anthropic_api_key:
        return await _chat_anthropic(data.message, model, system)
    elif settings.openai_api_key:
        return await _chat_openai(data.message, model, system)
    else:
        return {
            "response": (
                "Nenhuma chave de API configurada. "
                "Defina OPENROUTER_API_KEY, ANTHROPIC_API_KEY ou OPENAI_API_KEY no arquivo .env"
            ),
            "model": "not-configured",
        }


async def _chat_openrouter(message: str, model: str, system: str) -> dict:
    """Chat via OpenRouter (supports many models)."""
    import httpx

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.openrouter_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": message},
                ],
            },
        )
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        data = resp.json()
        return {
            "response": data["choices"][0]["message"]["content"],
            "model": data.get("model", model),
            "provider": "openrouter",
        }


async def _chat_anthropic(message: str, model: str, system: str) -> dict:
    """Chat via Anthropic API (Claude)."""
    import httpx

    # Map OpenRouter model names to Anthropic names
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
                "messages": [{"role": "user", "content": message}],
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


async def _chat_openai(message: str, model: str, system: str) -> dict:
    """Chat via OpenAI API (GPT)."""
    import httpx

    openai_model = model
    if "/" in model:
        openai_model = model.split("/")[-1]
    # Default to GPT-4o if model doesn't look like an OpenAI model
    if not openai_model.startswith(("gpt-", "o1", "o3", "o4")):
        openai_model = "gpt-4o"

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.openai_api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": openai_model,
                "messages": [
                    {"role": "system", "content": system},
                    {"role": "user", "content": message},
                ],
            },
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
