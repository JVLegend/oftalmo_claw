"""General API routes."""

from fastapi import APIRouter

router = APIRouter()


@router.post("/chat")
async def chat(message: dict):
    """Send a message to the AI agent."""
    return {
        "response": "Agent response placeholder. Connect an LLM provider to enable.",
        "model": "not-configured",
    }


@router.get("/calculators/iol")
async def iol_calculator(al: float = 23.5, k1: float = 43.0, k2: float = 44.0, target: float = -0.5):
    """IOL power calculation (simplified SRK/T)."""
    avg_k = (k1 + k2) / 2
    # Simplified SRK/T approximation
    a_constant = 118.7
    iol_power = a_constant - (2.5 * al) - (0.9 * avg_k)

    return {
        "input": {"axial_length": al, "k1": k1, "k2": k2, "target_refraction": target},
        "result": {
            "iol_power": round(iol_power, 2),
            "formula": "SRK/T (simplified)",
            "disclaimer": "For educational purposes only. Use certified biometry software for clinical decisions.",
        },
    }


@router.get("/calculators/va-convert")
async def va_converter(snellen: str = "20/40"):
    """Visual acuity conversion."""
    parts = snellen.split("/")
    if len(parts) != 2:
        return {"error": "Format must be like 20/40"}

    numerator, denominator = int(parts[0]), int(parts[1])
    decimal_va = numerator / denominator
    logmar = round(-1 * __import__("math").log10(decimal_va), 2)

    return {
        "snellen": snellen,
        "decimal": round(decimal_va, 3),
        "logmar": logmar,
        "category": _classify_va(logmar),
    }


def _classify_va(logmar: float) -> str:
    if logmar <= 0.0:
        return "Normal (20/20 or better)"
    elif logmar <= 0.3:
        return "Mild vision loss"
    elif logmar <= 0.5:
        return "Moderate vision loss"
    elif logmar <= 1.0:
        return "Severe vision loss"
    else:
        return "Profound vision loss / Legal blindness"
