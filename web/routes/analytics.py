"""Trends & Analytics API routes (real database)."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, extract
from datetime import datetime, timedelta

from models.database import get_db
from models.exam import ExamRecord
from models.case import Case, CaseStatus
from models.doctor import Doctor

router = APIRouter()

MONTH_LABELS = {
    1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr", 5: "Mai", 6: "Jun",
    7: "Jul", 8: "Ago", 9: "Set", 10: "Out", 11: "Nov", 12: "Dez",
}

EXAM_TYPE_LABELS = {
    "fundoscopia": "Fundoscopia",
    "oct": "OCT",
    "campimetria": "Campimetria",
    "topografia": "Topografia",
    "biometria": "Biometria",
    "retinografia": "Retinografia",
}


@router.get("/trends")
async def get_trends(period: str = "month", db: AsyncSession = Depends(get_db)):
    """Get volume and quality trends from real exam data."""
    now = datetime.utcnow()
    six_months_ago = now - timedelta(days=180)

    result = await db.execute(
        select(
            extract("year", ExamRecord.created_at).label("year"),
            extract("month", ExamRecord.created_at).label("month"),
            func.count().label("volume"),
            func.round(func.avg(ExamRecord.quality_score), 1).label("quality_score"),
        )
        .where(ExamRecord.created_at >= six_months_ago)
        .group_by("year", "month")
        .order_by("year", "month")
    )
    rows = result.all()

    data = []
    for row in rows:
        month_num = int(row.month)
        label = MONTH_LABELS.get(month_num, str(month_num))
        data.append({
            "label": label,
            "volume": row.volume,
            "quality_score": float(row.quality_score) if row.quality_score else 0,
        })

    return {"period": period, "data": data}


@router.get("/by-exam-type")
async def get_by_exam_type(db: AsyncSession = Depends(get_db)):
    """Get performance breakdown by exam type from real data."""
    result = await db.execute(
        select(
            ExamRecord.exam_type,
            func.count().label("count"),
            func.round(func.avg(ExamRecord.quality_score), 1).label("quality_score"),
        )
        .group_by(ExamRecord.exam_type)
        .order_by(func.count().desc())
    )
    rows = result.all()

    exam_types = []
    for row in rows:
        exam_types.append({
            "type": EXAM_TYPE_LABELS.get(row.exam_type, row.exam_type.capitalize()),
            "count": row.count,
            "quality_score": float(row.quality_score) if row.quality_score else 0,
        })

    return {"exam_types": exam_types}


@router.get("/rankings")
async def get_operator_rankings(db: AsyncSession = Depends(get_db)):
    """Get operator performance rankings from real data."""
    result = await db.execute(
        select(
            Doctor.id,
            Doctor.name,
            func.count(ExamRecord.id).label("exams"),
            func.round(func.avg(ExamRecord.quality_score), 1).label("quality_score"),
        )
        .join(ExamRecord, ExamRecord.doctor_id == Doctor.id)
        .group_by(Doctor.id, Doctor.name)
        .order_by(func.avg(ExamRecord.quality_score).desc())
    )
    rows = result.all()

    rankings = []
    for rank, row in enumerate(rows, 1):
        rankings.append({
            "rank": rank,
            "name": row.name,
            "exams": row.exams,
            "quality_score": float(row.quality_score) if row.quality_score else 0,
        })

    return {"rankings": rankings}


@router.get("/summary")
async def get_summary(db: AsyncSession = Depends(get_db)):
    """Get summary metrics from real data."""
    total_exams = await db.scalar(
        select(func.count()).select_from(ExamRecord)
    ) or 0

    active_users = await db.scalar(
        select(func.count()).select_from(Doctor).where(Doctor.is_active == True)
    ) or 0

    pending = await db.scalar(
        select(func.count()).select_from(Case)
        .where(Case.status.in_([CaseStatus.PENDING, CaseStatus.IN_ANALYSIS]))
    ) or 0

    resolved = await db.scalar(
        select(func.count()).select_from(Case)
        .where(Case.status == CaseStatus.COMPLETED)
    ) or 0

    # Most common exam type
    top_exam_result = await db.execute(
        select(ExamRecord.exam_type, func.count().label("cnt"))
        .group_by(ExamRecord.exam_type)
        .order_by(func.count().desc())
        .limit(1)
    )
    top_exam_row = top_exam_result.first()
    top_exam = EXAM_TYPE_LABELS.get(
        top_exam_row.exam_type, top_exam_row.exam_type.capitalize()
    ) if top_exam_row else "—"

    return {
        "total_exams_ytd": total_exams,
        "active_users": active_users,
        "second_opinion_pending": pending,
        "second_opinion_resolved": resolved,
        "top_exam_type": top_exam,
    }
