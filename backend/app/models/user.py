from sqlalchemy import Column, String, Boolean, DateTime, Text, JSON, ForeignKey, Integer, Enum
from sqlalchemy.orm import relationship
import uuid
import enum
from app.models.base import Base, TimestampMixin

class UserRole(str, enum.Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    MANAGER = "manager"
    ANALYST = "analyst"
    USER = "user"
    GUEST = "guest"

class UserStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"
    DELETED = "deleted"

class User(Base, TimestampMixin):
    __tablename__ = "users"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, index=True, nullable=False)
    phone = Column(String(50), unique=True, index=True, nullable=True)
    hashed_password = Column(String(255), nullable=True)
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    display_name = Column(String(200), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=True)
    department = Column(String(100), nullable=True)
    job_title = Column(String(100), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    status = Column(Enum(UserStatus), default=UserStatus.PENDING, nullable=False)
    email_verified = Column(Boolean, default=False)
    phone_verified = Column(Boolean, default=False)
    identity_verified = Column(Boolean, default=False)
    mfa_enabled = Column(Boolean, default=False)
    mfa_secret = Column(String(255), nullable=True)
    webauthn_enabled = Column(Boolean, default=False)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    last_login_ip = Column(String(45), nullable=True)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime(timezone=True), nullable=True)
    preferences = Column(JSON, default=dict)
    search_history = Column(JSON, default=list)
    saved_queries = Column(JSON, default=list)
    google_id = Column(String(255), nullable=True, index=True)
    github_id = Column(String(255), nullable=True, index=True)
    microsoft_id = Column(String(255), nullable=True, index=True)
    saml_subject = Column(String(255), nullable=True, index=True)
    subscription_tier = Column(String(50), default="free")
    subscription_expires_at = Column(DateTime(timezone=True), nullable=True)
    api_quota_remaining = Column(Integer, default=1000)
    api_quota_total = Column(Integer, default=1000)
    company = relationship("Company", back_populates="users")
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")
    osint_reports = relationship("OSINTReport", back_populates="user")
    search_queries = relationship("SearchQuery", back_populates="user")
    team_memberships = relationship("TeamMember", back_populates="user")

    @property
    def full_name(self):
        return f"{self.first_name or ''} {self.last_name or ''}".strip() or self.display_name or self.email
    @property
    def is_active(self):
        return self.status == UserStatus.ACTIVE
    @property
    def is_admin(self):
        return self.role in [UserRole.ADMIN, UserRole.SUPER_ADMIN]

class Company(Base, TimestampMixin):
    __tablename__ = "companies"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, index=True, nullable=False)
    domain = Column(String(255), unique=True, nullable=True)
    logo_url = Column(String(500), nullable=True)
    industry = Column(String(100), nullable=True)
    size = Column(String(50), nullable=True)
    website = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    billing_email = Column(String(255), nullable=True)
    billing_address = Column(JSON, nullable=True)
    stripe_customer_id = Column(String(255), nullable=True)
    stripe_subscription_id = Column(String(255), nullable=True)
    settings = Column(JSON, default=dict)
    allowed_domains = Column(JSON, default=list)
    sso_enabled = Column(Boolean, default=False)
    sso_provider = Column(String(50), nullable=True)
    users = relationship("User", back_populates="company")
    teams = relationship("Team", back_populates="company")

class Team(Base, TimestampMixin):
    __tablename__ = "teams"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    company_id = Column(String(36), ForeignKey("companies.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    company = relationship("Company", back_populates="teams")
    members = relationship("TeamMember", back_populates="team")

class TeamMember(Base, TimestampMixin):
    __tablename__ = "team_members"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    team_id = Column(String(36), ForeignKey("teams.id"), nullable=False)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    role = Column(String(50), default="member")
    team = relationship("Team", back_populates="members")
    user = relationship("User", back_populates="team_memberships")

class UserSession(Base, TimestampMixin):
    __tablename__ = "user_sessions"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    refresh_token = Column(String(500), nullable=False)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_valid = Column(Boolean, default=True)
    user = relationship("User", back_populates="sessions")
