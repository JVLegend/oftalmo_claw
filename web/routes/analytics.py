"""Trends & Analytics API routes."""

from fastapi import APIRouter
from typing import Optional

router = APIRouter()


@router.get("/trends")
async def get_trends(period: str = "month"):
    """Get volume and quality trends over time."""
    # Demo data matching the user's mockup
    return {
        "period": period,
        "data": [
            {"label": "Jul", "volume": 145, "quality_score": 85.2},
            {"label": "Ago", "volume": 178, "quality_score": 86.1},
            {"label": "Set", "volume": 203, "quality_score": 87.8},
            {"label": "Out", "volume": 247, "quality_score": 88.5},
            {"label": "Nov", "volume": 289, "quality_score": 89.2},
            {"label": "Dez", "volume": 312, "quality_score": 90.1},
        ],
    }


@router.get("/by-exam-type")
async def get_by_exam_type():
    """Get performance breakdown by exam type."""
    return {
        "exam_types": [
            {"type": "Fundoscopia", "count": 542, "quality_score": 91.2},
            {"type": "OCT", "count": 389, "quality_score": 88.7},
            {"type": "Campimetria", "count": 276, "quality_score": 85.4},
            {"type": "Topografia", "count": 198, "quality_score": 90.3},
            {"type": "Biometria", "count": 167, "quality_score": 92.1},
            {"type": "Retinografia", "count": 134, "quality_score": 87.9},
        ],
    }


@router.get("/rankings")
async def get_operator_rankings():
    """Get operator performance rankings."""
    return {
        "rankings": [
            {"rank": 1, "name": "Dr. Carlos Silva", "exams": 234, "quality_score": 92.1, "trend": "+5.2%"},
            {"rank": 2, "name": "Dra. Ana Oliveira", "exams": 198, "quality_score": 91.8, "trend": "+3.1%"},
            {"rank": 3, "name": "Dr. Roberto Costa", "exams": 176, "quality_score": 90.5, "trend": "+2.8%"},
            {"rank": 4, "name": "Dra. Maria Santos", "exams": 165, "quality_score": 89.7, "trend": "+4.5%"},
            {"rank": 5, "name": "Dr. Paulo Mendes", "exams": 143, "quality_score": 88.2, "trend": "+1.9%"},
        ],
    }


@router.get("/summary")
async def get_summary():
    """Get summary metrics."""
    return {
        "total_exams_ytd": 1706,
        "active_users": 12,
        "avg_report_time_hours": 2.4,
        "second_opinion_pending": 3,
        "second_opinion_resolved": 47,
        "top_pathology": "Retinopatia Diabetica",
        "growth_rate": "+8.3%",
    }
