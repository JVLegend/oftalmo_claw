"""Dashboard API routes (real database)."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timedelta

from models.database import get_db
from models.case import Case, CaseStatus
from models.doctor import Doctor
from models.exam import ExamRecord

router = APIRouter()


@router.get("/stats")
async def get_dashboard_stats(db: AsyncSession = Depends(get_db)):
    """Get overview statistics from real database."""
    now = datetime.utcnow()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Exams today
    exams_today = await db.scalar(
        select(func.count()).select_from(ExamRecord)
        .where(ExamRecord.created_at >= today_start)
    ) or 0

    # Pending cases
    pending_cases = await db.scalar(
        select(func.count()).select_from(Case)
        .where(Case.status.in_([CaseStatus.PENDING, CaseStatus.IN_ANALYSIS]))
    ) or 0

    # Active specialists (online)
    active_specialists = await db.scalar(
        select(func.count()).select_from(Doctor)
        .where(Doctor.is_active == True, Doctor.is_online == True)
    ) or 0

    # Average quality score (last 30 days)
    avg_quality = await db.scalar(
        select(func.avg(ExamRecord.quality_score))
        .where(ExamRecord.created_at >= now - timedelta(days=30))
    )
    avg_quality = round(avg_quality, 1) if avg_quality else 0.0

    # Exams this month
    exams_month = await db.scalar(
        select(func.count()).select_from(ExamRecord)
        .where(ExamRecord.created_at >= month_start)
    ) or 0

    # Reports pending signature
    reports_pending = await db.scalar(
        select(func.count()).select_from(ExamRecord)
        .where(
            ExamRecord.report_generated == "Y",
            ExamRecord.report_signed == "N",
        )
    ) or 0

    return {
        "total_exams_today": exams_today,
        "pending_cases": pending_cases,
        "active_specialists": active_specialists,
        "avg_quality_score": avg_quality,
        "exams_this_month": exams_month,
        "reports_pending": reports_pending,
    }
