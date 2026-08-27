import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.config import settings
from app.models.user import User, UserStatus, UserRole
from app.core.security import create_access_token, create_refresh_token, get_password_hash
import structlog

logger = structlog.get_logger()

class MicrosoftOAuth:
    @staticmethod
    def get_auth_url():
        return f"https://login.microsoftonline.com/common/oauth2/v2.0/authorize?client_id={settings.MICROSOFT_CLIENT_ID}&redirect_uri={settings.API_URL}/api/v1/auth/oauth/microsoft/callback&response_type=code&scope=openid email profile User.Read"

    @staticmethod
    async def handle_callback(code: str, db: AsyncSession):
        async with httpx.AsyncClient() as client:
            token_resp = await client.post("https://login.microsoftonline.com/common/oauth2/v2.0/token",
                data={"code": code, "client_id": settings.MICROSOFT_CLIENT_ID,
                    "client_secret": settings.MICROSOFT_CLIENT_SECRET,
                    "redirect_uri": f"{settings.API_URL}/api/v1/auth/oauth/microsoft/callback",
                    "grant_type": "authorization_code"})
            tokens = token_resp.json()
            user_resp = await client.get("https://graph.microsoft.com/v1.0/me",
                headers={"Authorization": f"Bearer {tokens['access_token']}"})
            muser = user_resp.json()
            result = await db.execute(select(User).where(User.microsoft_id == muser["id"]))
            user = result.scalar_one_or_none()
            if not user:
                result = await db.execute(select(User).where(User.email == muser["mail"]))
                user = result.scalar_one_or_none()
                if user:
                    user.microsoft_id = muser["id"]
                else:
                    user = User(email=muser["mail"], first_name=muser.get("givenName"),
                        last_name=muser.get("surname"), display_name=muser.get("displayName"),
                        microsoft_id=muser["id"], status=UserStatus.ACTIVE, role=UserRole.USER,
                        hashed_password=get_password_hash(__import__('secrets').token_urlsafe(32)))
                    db.add(user)
            await db.commit(); await db.refresh(user)
            access = create_access_token({"sub": user.id, "email": user.email, "role": user.role.value})
            refresh = create_refresh_token({"sub": user.id})
            logger.info("microsoft_oauth_login", user_id=user.id)
            return {"access_token": access, "refresh_token": refresh, "token_type": "bearer", "user": user}
