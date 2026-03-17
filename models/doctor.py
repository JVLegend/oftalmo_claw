"""Doctor / Specialist model."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum
from models.database import Base
from models.case import Specialty


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    crm = Column(String(20), nullable=True)
    specialty = Column(SQLEnum(Specialty), default=Specialty.GENERAL)
    institution = Column(String(200), nullable=True)
    avatar_url = Column(String(500), nullable=True)

    is_active = Column(Boolean, default=True)
    is_online = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

    password_hash = Column(String(200), nullable=False, default="demo")

    created_at = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)

    @property
    def initials(self):
        parts = self.name.split()
        if len(parts) >= 2:
            return (parts[0][0] + parts[-1][0]).upper()
        return self.name[:2].upper()

    @property
    def display_specialty(self):
        labels = {
            "retina": "Retina",
            "glaucoma": "Glaucoma",
            "cornea": "Córnea",
            "refractive": "Refrativa",
            "oculoplastics": "Oculoplástica",
            "strabismus": "Estrabismo",
            "neuro_ophthalmology": "Neuro-Oftalmo",
            "pediatric": "Pediátrica",
            "uveitis": "Uveíte",
            "general": "Geral",
        }
        return labels.get(self.specialty.value if self.specialty else "general", "Geral")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "crm": self.crm,
            "specialty": self.display_specialty,
            "initials": self.initials,
            "is_online": self.is_online,
            "is_active": self.is_active,
        }
