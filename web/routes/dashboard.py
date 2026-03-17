"""Dashboard API routes."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/stats")
async def get_dashboard_stats():
    """Get overview statistics for the Mission Control dashboard."""
    return {
        "total_exams_today": 47,
        "pending_cases": 3,
        "active_specialists": 4,
        "avg_quality_score": 89.2,
        "exams_this_month": 312,
        "reports_pending": 8,
    }
