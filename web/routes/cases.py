"""Second Opinion - Case management API routes."""

from fastapi import APIRouter
from typing import Optional

router = APIRouter()


@router.get("/")
async def list_cases(status: Optional[str] = None):
    """List second opinion cases."""
    # Demo data matching the user's mockup
    cases = [
        {
            "id": 1,
            "case_number": "#2847",
            "patient": {"age": 56, "gender": "F"},
            "requested_by": {"name": "Dr. Carlos Silva", "specialty": "Geral"},
            "assigned_to": {"name": "Dra. Ana Oliveira", "specialty": "Retina"},
            "status": "urgent",
            "urgency": "urgent",
            "created_at": "2024-11-28T14:30:00",
            "responses_count": 1,
        },
        {
            "id": 2,
            "case_number": "#2845",
            "patient": {"age": 68, "gender": "M"},
            "requested_by": {"name": "Dra. Maria Santos", "specialty": "Cornea"},
            "assigned_to": {"name": "Dr. Roberto Costa", "specialty": "Glaucoma"},
            "status": "in_analysis",
            "urgency": "normal",
            "created_at": "2024-11-28T10:15:00",
            "responses_count": 2,
        },
        {
            "id": 3,
            "case_number": "#2843",
            "patient": {"age": 42, "gender": "F"},
            "requested_by": {"name": "Dr. Paulo Mendes", "specialty": "Retina"},
            "assigned_to": {"name": "Dra. Maria Santos", "specialty": "Cornea"},
            "status": "pending",
            "urgency": "normal",
            "created_at": "2024-11-27T16:45:00",
            "responses_count": 0,
        },
    ]

    if status:
        cases = [c for c in cases if c["status"] == status]

    return {"cases": cases, "total": len(cases)}


@router.get("/specialists")
async def list_specialists():
    """List available specialists."""
    return {
        "specialists": [
            {"name": "Dra. Ana Oliveira", "specialty": "Retina", "active_cases": 3, "online": True, "initials": "DAO"},
            {"name": "Dr. Roberto Costa", "specialty": "Glaucoma", "active_cases": 2, "online": True, "initials": "DRC"},
            {"name": "Dra. Maria Santos", "specialty": "Cornea", "active_cases": 5, "online": False, "initials": "DMS"},
            {"name": "Dr. Paulo Mendes", "specialty": "Retina", "active_cases": 1, "online": True, "initials": "DPM"},
        ]
    }


@router.post("/")
async def create_case():
    """Create a new second opinion case."""
    return {"message": "Case created", "case_number": "#2848"}


@router.get("/{case_id}")
async def get_case(case_id: int):
    """Get case details."""
    return {"id": case_id, "case_number": f"#{2840 + case_id}"}


@router.post("/{case_id}/opinions")
async def submit_opinion(case_id: int):
    """Submit an opinion for a case."""
    return {"message": "Opinion submitted", "case_id": case_id}
