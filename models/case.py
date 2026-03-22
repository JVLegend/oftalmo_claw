"""Second Opinion - Case and Opinion models."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship
from models.database import Base
import enum


class CaseStatus(str, enum.Enum):
    PENDING = "pending"
    IN_ANALYSIS = "in_analysis"
    COMPLETED = "completed"
    URGENT = "urgent"


class CaseUrgency(str, enum.Enum):
    NORMAL = "normal"
    URGENT = "urgent"
    EMERGENCY = "emergency"


class Specialty(str, enum.Enum):
    RETINA = "retina"
    GLAUCOMA = "glaucoma"
    CORNEA = "cornea"
    REFRACTIVE = "refractive"
    OCULOPLASTICS = "oculoplastics"
    STRABISMUS = "strabismus"
    NEURO_OPHTHALMOLOGY = "neuro_ophthalmology"
    PEDIATRIC = "pediatric"
    UVEITIS = "uveitis"
    GENERAL = "general"


class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, autoincrement=True)
    case_number = Column(String(20), unique=True, nullable=False)
    patient_age = Column(Integer)
    patient_gender = Column(String(1))  # M/F
    patient_history = Column(Text)
    chief_complaint = Column(Text)
    hypothesis = Column(Text)
    exam_findings = Column(Text)

    urgency = Column(SQLEnum(CaseUrgency), default=CaseUrgency.NORMAL)
    status = Column(SQLEnum(CaseStatus), default=CaseStatus.PENDING)
    specialty_requested = Column(SQLEnum(Specialty), default=Specialty.GENERAL)

    requested_by_id = Column(Integer, ForeignKey("doctors.id"))
    assigned_to_id = Column(Integer, ForeignKey("doctors.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    __table_args__ = (
        Index("ix_cases_status", "status"),
        Index("ix_cases_urgency", "urgency"),
        Index("ix_cases_created_at", "created_at"),
        Index("ix_cases_requested_by", "requested_by_id"),
        Index("ix_cases_assigned_to", "assigned_to_id"),
    )

    requested_by = relationship("Doctor", foreign_keys=[requested_by_id], backref="requested_cases")
    assigned_to = relationship("Doctor", foreign_keys=[assigned_to_id], backref="assigned_cases")
    opinions = relationship("Opinion", back_populates="case", cascade="all, delete-orphan")
    images = relationship("CaseImage", back_populates="case", cascade="all, delete-orphan")
    messages = relationship("CaseMessage", back_populates="case", cascade="all, delete-orphan")


class CaseImage(Base):
    __tablename__ = "case_images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    image_type = Column(String(50))  # oct, fundoscopy, topography, visual_field
    file_path = Column(String(500))
    description = Column(Text, nullable=True)
    eye = Column(String(2))  # OD, OS, OU
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    case = relationship("Case", back_populates="images")


class Opinion(Base):
    __tablename__ = "opinions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    diagnosis = Column(Text)
    recommendation = Column(Text)
    confidence = Column(Float, nullable=True)  # 0.0 to 1.0
    references = Column(Text, nullable=True)
    ai_assisted = Column(String(1), default="N")  # Y/N
    created_at = Column(DateTime, default=datetime.utcnow)

    case = relationship("Case", back_populates="opinions")
    doctor = relationship("Doctor", backref="opinions")


class CaseMessage(Base):
    __tablename__ = "case_messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    case = relationship("Case", back_populates="messages")
    doctor = relationship("Doctor", backref="messages")
