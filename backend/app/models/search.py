from sqlalchemy import Column, String, Text, JSON, DateTime, ForeignKey, Float, Integer, Enum
from sqlalchemy.orm import relationship
import uuid
import enum
from app.models.base import Base, TimestampMixin

class SearchType(str, enum.Enum):
    WEB = "web"
    OSINT = "osint"
    AI = "ai"
    HYBRID = "hybrid"
    VECTOR = "vector"
    GRAPH = "graph"
    ENTERPRISE = "enterprise"

class SearchQuery(Base, TimestampMixin):
    __tablename__ = "search_queries"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    query_text = Column(Text, nullable=False)
    search_type = Column(Enum(SearchType), default=SearchType.HYBRID)
    user_context = Column(JSON, default=dict)
    company_context = Column(JSON, default=dict)
    session_context = Column(JSON, default=dict)
    results_count = Column(Integer, default=0)
    results_summary = Column(JSON, default=list)
    ai_summary = Column(Text, nullable=True)
    execution_time_ms = Column(Float, default=0.0)
    sources_used = Column(JSON, default=list)
    user_rating = Column(Integer, nullable=True)
    user_feedback = Column(Text, nullable=True)
    user = relationship("User", back_populates="search_queries")

class SearchIndex(Base, TimestampMixin):
    __tablename__ = "search_indices"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    url = Column(String(2000), nullable=False)
    title = Column(String(500), nullable=True)
    content = Column(Text, nullable=True)
    content_hash = Column(String(64), nullable=True, index=True)
    domain = Column(String(255), nullable=True, index=True)
    source_type = Column(String(50), nullable=True)
    language = Column(String(10), nullable=True)
    embedding = Column(JSON, nullable=True)
    embedding_model = Column(String(100), nullable=True)
    osint_tags = Column(JSON, default=list)
    risk_score = Column(Float, default=0.0)
    crawl_count = Column(Integer, default=1)
    last_crawled_at = Column(DateTime(timezone=True))
    backlinks = relationship("Backlink", foreign_keys="Backlink.target_id", back_populates="target")
