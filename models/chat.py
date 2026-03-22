"""Chat history model for persistent conversations."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index
from models.database import Base


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=True)
    role = Column(String, nullable=False)  # "user" | "assistant"
    content = Column(Text, nullable=False)
    model = Column(String, nullable=True)
    provider = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index("ix_chat_created_at", "created_at"),
        Index("ix_chat_doctor", "doctor_id"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "role": self.role,
            "content": self.content,
            "model": self.model,
            "provider": self.provider,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
