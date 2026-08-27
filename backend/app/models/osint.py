from sqlalchemy import Column, String, Text, JSON, DateTime, ForeignKey, Float, Integer, Enum
from sqlalchemy.orm import relationship
import uuid
import enum
from app.models.base import Base, TimestampMixin

class OSINTReportStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"

class OSINTReport(Base, TimestampMixin):
    __tablename__ = "osint_reports"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    target = Column(String(500), nullable=False)
    target_type = Column(String(50), nullable=False)
    status = Column(Enum(OSINTReportStatus), default=OSINTReportStatus.PENDING)
    progress = Column(Float, default=0.0)
    modules = Column(JSON, default=list)
    findings = Column(JSON, default=list)
    risk_assessment = Column(JSON, default=dict)
    graph_nodes = Column(JSON, default=list)
    graph_edges = Column(JSON, default=list)
    ai_summary = Column(Text, nullable=True)
    ai_recommendations = Column(JSON, default=list)
    pdf_url = Column(String(500), nullable=True)
    json_export = Column(JSON, nullable=True)
    user = relationship("User", back_populates="osint_reports")

class Backlink(Base, TimestampMixin):
    __tablename__ = "backlinks"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    source_id = Column(String(36), ForeignKey("search_indices.id"), nullable=False)
    target_id = Column(String(36), ForeignKey("search_indices.id"), nullable=False)
    anchor_text = Column(String(500), nullable=True)
    link_type = Column(String(50), default="dofollow")
    target = relationship("SearchIndex", foreign_keys=[target_id], back_populates="backlinks")
