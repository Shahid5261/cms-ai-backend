from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.database import Base


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)

    customer_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    product = Column(String(100), nullable=False)
    complaint = Column(Text, nullable=False)

    complaint_summary = Column(Text, nullable=True)
    category = Column(String(100), nullable=True)
    severity = Column(String(50), nullable=True)
    root_cause = Column(Text, nullable=True)
    capa = Column(Text, nullable=True)
    suggested_response = Column(Text, nullable=True)

    status = Column(String(50), default="Pending")

    created_at = Column(DateTime, default=datetime.utcnow)