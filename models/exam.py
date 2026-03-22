"""Exam records and analytics models."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Index
from models.database import Base


class ExamRecord(Base):
    __tablename__ = "exam_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    exam_type = Column(String(50), nullable=False)  # oct, fundoscopy, topography, visual_field, biometry
    patient_id = Column(String(100), nullable=True)  # anonymized
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=True)

    eye = Column(String(2))  # OD, OS, OU
    findings = Column(Text, nullable=True)
    quality_score = Column(Float, nullable=True)  # 0-100

    ai_analysis = Column(Text, nullable=True)
    ai_confidence = Column(Float, nullable=True)

    report_generated = Column(String(1), default="N")
    report_signed = Column(String(1), default="N")
    report_signed_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_exams_type", "exam_type"),
        Index("ix_exams_doctor", "doctor_id"),
        Index("ix_exams_created_at", "created_at"),
        Index("ix_exams_type_created", "exam_type", "created_at"),
    )


class AnalyticsSnapshot(Base):
    """Pre-computed analytics for the trends dashboard."""
    __tablename__ = "analytics_snapshots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    period_type = Column(String(10))  # day, week, month, quarter, year
    period_label = Column(String(20))  # "2024-11", "2024-W48", etc.
    exam_type = Column(String(50), nullable=True)  # null = all types
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=True)  # null = all doctors

    total_exams = Column(Integer, default=0)
    avg_quality_score = Column(Float, nullable=True)
    avg_report_time_hours = Column(Float, nullable=True)
    ai_assisted_count = Column(Integer, default=0)

    computed_at = Column(DateTime, default=datetime.utcnow)
