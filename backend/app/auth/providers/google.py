import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.config import settings
from app.models.user import User, UserStatus, UserRole
from app.core.security import create_access_token, create_refresh_token, get_password_hash
import structlog

logger = structlog.get_logger()

class GoogleOAuth:
    @staticmethod
    def get_auth_url():
        return f"https://accounts.google.com/o/oauth2/v2/auth?client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri={settings.API_URL}/api/v1/auth/oauth/google/callback&response_type=code&scope=openid email profile&access_type=offline"

    @staticmethod
    async def handle_callback(code: str, db: AsyncSession):
        async with httpx.AsyncClient() as client:
            token_resp = await client.post("https://oauth2.googleapis.com/token", data={
                "code": code, "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": f"{settings.API_URL}/api/v1/auth/oauth/google/callback",
                "grant_type": "authorization_code",
            })
            tokens = token_resp.json()
            user_resp = await client.get("https://www.googleapis.com/oauth2/v2/userinfo",
                headers={"Authorization": f"Bearer {tokens['access_token']}"})
            guser = user_resp.json()
            result = await db.execute(select(User).where(User.google_id == guser["id"]))
            user = result.scalar_one_or_none()
            if not user:
                result = await db.execute(select(User).where(User.email == guser["email"]))
                user = result.scalar_one_or_none()
                if user:
                    user.google_id = guser["id"]
                    user.email_verified = True
                else:
                    user = User(email=guser["email"], first_name=guser.get("given_name"),
                        last_name=guser.get("family_name"), display_name=guser.get("name"),
                        avatar_url=guser.get("picture"), google_id=guser["id"],
                        email_verified=True, status=UserStatus.ACTIVE, role=UserRole.USER,
                        hashed_password=get_password_hash(__import__('secrets').token_urlsafe(32)))
                    db.add(user)
            await db.commit(); await db.refresh(user)
            access = create_access_token({"sub": user.id, "email": user.email, "role": user.role.value})
            refresh = create_refresh_token({"sub": user.id})
            logger.info("google_oauth_login", user_id=user.id)
            return {"access_token": access, "refresh_token": refresh, "token_type": "bearer", "user": user}
