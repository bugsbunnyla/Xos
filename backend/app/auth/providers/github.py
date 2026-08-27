import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.config import settings
from app.models.user import User, UserStatus, UserRole
from app.core.security import create_access_token, create_refresh_token, get_password_hash
import structlog

logger = structlog.get_logger()

class GitHubOAuth:
    @staticmethod
    def get_auth_url():
        return f"https://github.com/login/oauth/authorize?client_id={settings.GITHUB_CLIENT_ID}&redirect_uri={settings.API_URL}/api/v1/auth/oauth/github/callback&scope=user:email read:user"

    @staticmethod
    async def handle_callback(code: str, db: AsyncSession):
        async with httpx.AsyncClient() as client:
            token_resp = await client.post("https://github.com/login/oauth/access_token",
                data={"code": code, "client_id": settings.GITHUB_CLIENT_ID,
                    "client_secret": settings.GITHUB_CLIENT_SECRET,
                    "redirect_uri": f"{settings.API_URL}/api/v1/auth/oauth/github/callback"},
                headers={"Accept": "application/json"})
            tokens = token_resp.json()
            headers = {"Authorization": f"token {tokens['access_token']}"}
            user_resp = await client.get("https://api.github.com/user", headers=headers)
            guser = user_resp.json()
            email_resp = await client.get("https://api.github.com/user/emails", headers=headers)
            emails = email_resp.json()
            primary = next((e["email"] for e in emails if e["primary"]), emails[0]["email"])
            result = await db.execute(select(User).where(User.github_id == str(guser["id"])))
            user = result.scalar_one_or_none()
            if not user:
                result = await db.execute(select(User).where(User.email == primary))
                user = result.scalar_one_or_none()
                if user:
                    user.github_id = str(guser["id"])
                else:
                    user = User(email=primary, display_name=guser.get("name") or guser.get("login"),
                        avatar_url=guser.get("avatar_url"), github_id=str(guser["id"]),
                        status=UserStatus.ACTIVE, role=UserRole.USER,
                        hashed_password=get_password_hash(__import__('secrets').token_urlsafe(32)))
                    db.add(user)
            await db.commit(); await db.refresh(user)
            access = create_access_token({"sub": user.id, "email": user.email, "role": user.role.value})
            refresh = create_refresh_token({"sub": user.id})
            logger.info("github_oauth_login", user_id=user.id)
            return {"access_token": access, "refresh_token": refresh, "token_type": "bearer", "user": user}
