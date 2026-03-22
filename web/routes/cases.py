"""Second Opinion - Case management API routes (real database)."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from models.database import get_db
from models.case import Case, CaseStatus, CaseUrgency, Specialty, Opinion, CaseMessage
from models.doctor import Doctor
from web.sanitize import sanitize_text

router = APIRouter()


# --- Pydantic schemas ---

class CaseCreate(BaseModel):
    patient_age: int
    patient_gender: str
    patient_history: Optional[str] = None
    chief_complaint: str
    hypothesis: Optional[str] = None
    exam_findings: Optional[str] = None
    urgency: str = "normal"
    specialty_requested: str = "general"
    requested_by_id: int
    assigned_to_id: Optional[int] = None


class OpinionCreate(BaseModel):
    doctor_id: int
    diagnosis: str
    recommendation: str
    confidence: Optional[float] = None
    references: Optional[str] = None
    ai_assisted: str = "N"


class MessageCreate(BaseModel):
    doctor_id: int
    content: str


class StatusUpdate(BaseModel):
    status: str


# --- Routes ---

@router.get("/")
async def list_cases(
    status: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db),
):
    """List second opinion cases with pagination."""
    # Cap limit to prevent loading entire DB
    limit = min(limit, 100)

    query = (
        select(Case)
        .options(
            selectinload(Case.requested_by),
            selectinload(Case.assigned_to),
            selectinload(Case.opinions),
        )
        .order_by(Case.created_at.desc())
    )

    if status:
        try:
            status_enum = CaseStatus(status)
            query = query.where(Case.status == status_enum)
        except ValueError:
            pass

    # Total count
    count_query = select(func.count()).select_from(Case)
    total = await db.scalar(count_query) or 0

    # Apply pagination
    query = query.limit(limit).offset(offset)
    result = await db.execute(query)
    cases = result.scalars().all()

    return {
        "cases": [_case_to_dict(c) for c in cases],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.get("/specialists")
async def list_specialists(db: AsyncSession = Depends(get_db)):
    """List available specialists with case counts."""
    result = await db.execute(
        select(Doctor).where(Doctor.is_active == True)
    )
    doctors = result.scalars().all()

    specialists = []
    for doc in doctors:
        # Count active cases
        count_result = await db.execute(
            select(func.count()).select_from(Case).where(
                Case.assigned_to_id == doc.id,
                Case.status.in_([CaseStatus.PENDING, CaseStatus.IN_ANALYSIS]),
            )
        )
        active_cases = count_result.scalar() or 0

        specialists.append({
            "id": doc.id,
            "name": doc.name,
            "specialty": doc.display_specialty,
            "active_cases": active_cases,
            "online": doc.is_online,
            "initials": doc.initials,
        })

    return {"specialists": specialists}


@router.post("/")
async def create_case(data: CaseCreate, db: AsyncSession = Depends(get_db)):
    """Create a new second opinion case."""
    # Auto-generate case number
    count_result = await db.execute(select(func.count()).select_from(Case))
    total = count_result.scalar() or 0
    case_number = f"#{2840 + total + 1}"

    try:
        urgency = CaseUrgency(data.urgency)
    except ValueError:
        urgency = CaseUrgency.NORMAL

    try:
        specialty = Specialty(data.specialty_requested)
    except ValueError:
        specialty = Specialty.GENERAL

    # Validate patient_age range
    if not (0 <= data.patient_age <= 120):
        raise HTTPException(status_code=400, detail="Idade deve estar entre 0 e 120")
    if data.patient_gender not in ("M", "F"):
        raise HTTPException(status_code=400, detail="Sexo deve ser M ou F")

    case = Case(
        case_number=case_number,
        patient_age=data.patient_age,
        patient_gender=data.patient_gender,
        patient_history=sanitize_text(data.patient_history) if data.patient_history else None,
        chief_complaint=sanitize_text(data.chief_complaint),
        hypothesis=sanitize_text(data.hypothesis) if data.hypothesis else None,
        exam_findings=sanitize_text(data.exam_findings) if data.exam_findings else None,
        urgency=urgency,
        status=CaseStatus.PENDING,
        specialty_requested=specialty,
        requested_by_id=data.requested_by_id,
        assigned_to_id=data.assigned_to_id,
    )
    db.add(case)
    await db.commit()
    await db.refresh(case)

    return {"message": "Caso criado", "case_number": case.case_number, "id": case.id}


@router.get("/{case_id}")
async def get_case(case_id: int, db: AsyncSession = Depends(get_db)):
    """Get full case details with opinions and messages."""
    result = await db.execute(
        select(Case)
        .options(
            selectinload(Case.requested_by),
            selectinload(Case.assigned_to),
            selectinload(Case.opinions).selectinload(Opinion.doctor),
            selectinload(Case.messages).selectinload(CaseMessage.doctor),
            selectinload(Case.images),
        )
        .where(Case.id == case_id)
    )
    case = result.scalars().first()
    if not case:
        raise HTTPException(status_code=404, detail="Caso não encontrado")

    return _case_detail_dict(case)


@router.post("/{case_id}/opinions")
async def submit_opinion(case_id: int, data: OpinionCreate, db: AsyncSession = Depends(get_db)):
    """Submit a specialist opinion for a case."""
    case = await db.get(Case, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Caso não encontrado")

    opinion = Opinion(
        case_id=case_id,
        doctor_id=data.doctor_id,
        diagnosis=sanitize_text(data.diagnosis),
        recommendation=sanitize_text(data.recommendation),
        confidence=data.confidence,
        references=data.references,
        ai_assisted=data.ai_assisted,
    )
    db.add(opinion)

    # Update case status
    if case.status == CaseStatus.PENDING:
        case.status = CaseStatus.IN_ANALYSIS

    await db.commit()
    return {"message": "Opinião registrada", "case_id": case_id, "opinion_id": opinion.id}


@router.post("/{case_id}/messages")
async def send_message(case_id: int, data: MessageCreate, db: AsyncSession = Depends(get_db)):
    """Send a message in a case discussion."""
    case = await db.get(Case, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Caso não encontrado")

    msg = CaseMessage(
        case_id=case_id,
        doctor_id=data.doctor_id,
        content=sanitize_text(data.content),
    )
    db.add(msg)
    await db.commit()
    return {"message": "Mensagem enviada", "id": msg.id}


@router.patch("/{case_id}/status")
async def update_case_status(case_id: int, data: StatusUpdate, db: AsyncSession = Depends(get_db)):
    """Update case status."""
    case = await db.get(Case, case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Caso não encontrado")

    try:
        case.status = CaseStatus(data.status)
    except ValueError:
        raise HTTPException(status_code=400, detail="Status inválido")

    if case.status == CaseStatus.COMPLETED:
        case.resolved_at = datetime.utcnow()

    await db.commit()
    return {"message": "Status atualizado", "status": case.status.value}


# --- Helpers ---

def _case_to_dict(case: Case) -> dict:
    return {
        "id": case.id,
        "case_number": case.case_number,
        "patient": {"age": case.patient_age, "gender": case.patient_gender},
        "chief_complaint": case.chief_complaint,
        "hypothesis": case.hypothesis,
        "requested_by": {
            "name": case.requested_by.name if case.requested_by else "—",
            "specialty": case.requested_by.display_specialty if case.requested_by else "—",
        },
        "assigned_to": {
            "name": case.assigned_to.name if case.assigned_to else "Não atribuído",
            "specialty": case.assigned_to.display_specialty if case.assigned_to else "—",
        },
        "status": case.status.value,
        "urgency": case.urgency.value,
        "specialty_requested": case.specialty_requested.value if case.specialty_requested else "general",
        "created_at": case.created_at.isoformat() if case.created_at else None,
        "responses_count": len(case.opinions) if case.opinions else 0,
    }


def _case_detail_dict(case: Case) -> dict:
    data = _case_to_dict(case)
    data["patient_history"] = case.patient_history
    data["exam_findings"] = case.exam_findings
    data["opinions"] = [
        {
            "id": op.id,
            "doctor": {"name": op.doctor.name, "specialty": op.doctor.display_specialty} if op.doctor else {},
            "diagnosis": op.diagnosis,
            "recommendation": op.recommendation,
            "confidence": op.confidence,
            "ai_assisted": op.ai_assisted,
            "created_at": op.created_at.isoformat() if op.created_at else None,
        }
        for op in (case.opinions or [])
    ]
    data["messages"] = [
        {
            "id": msg.id,
            "doctor": {"name": msg.doctor.name} if msg.doctor else {},
            "content": msg.content,
            "created_at": msg.created_at.isoformat() if msg.created_at else None,
        }
        for msg in (case.messages or [])
    ]
    data["images"] = [
        {
            "id": img.id,
            "image_type": img.image_type,
            "eye": img.eye,
            "description": img.description,
        }
        for img in (case.images or [])
    ]
    return data
