import asyncio
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import async_session
from app.models.user import User, Company, UserRole, UserStatus
from app.core.security import get_password_hash

async def seed():
    async with async_session() as db:
        # Create demo company
        company = Company(
            id=str(uuid.uuid4()),
            name="Acme Intelligence Corp",
            slug="acme-intel",
            domain="acme-intel.com",
            industry="Cybersecurity",
            size="50-200",
        )
        db.add(company)

        # Create admin user
        admin = User(
            id=str(uuid.uuid4()),
            email="admin@acme-intel.com",
            hashed_password=get_password_hash("admin123"),
            first_name="Admin",
            last_name="User",
            company_id=company.id,
            department="Security",
            job_title="CISO",
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE,
            email_verified=True,
        )
        db.add(admin)

        # Create analyst user
        analyst = User(
            id=str(uuid.uuid4()),
            email="analyst@acme-intel.com",
            hashed_password=get_password_hash("analyst123"),
            first_name="Sarah",
            last_name="Chen",
            company_id=company.id,
            department="Threat Intel",
            job_title="Senior Analyst",
            role=UserRole.ANALYST,
            status=UserStatus.ACTIVE,
            email_verified=True,
            preferences={"industry": "cybersecurity", "preferred_domain": "acme-intel.com"},
        )
        db.add(analyst)

        await db.commit()
        print("Database seeded successfully!")
        print("  Admin: admin@acme-intel.com / admin123")
        print("  Analyst: analyst@acme-intel.com / analyst123")

if __name__ == "__main__":
    asyncio.run(seed())
