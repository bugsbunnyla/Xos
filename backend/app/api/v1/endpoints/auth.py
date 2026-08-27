from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta
import structlog

from app.db.session import get_db
from app.models.user import User, UserStatus, UserRole, UserSession
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token, decode_token
from app.core.config import settings
from app.auth.schemas import UserCreate, UserLogin, Token, UserResponse, PasswordReset, MFAVerify, OAuthCallback
from app.auth.providers.google import GoogleOAuth
from app.auth.providers.github import GitHubOAuth
from app.auth.providers.microsoft import MicrosoftOAuth

logger = structlog.get_logger()
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user or user.status != UserStatus.ACTIVE:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    if user_data.phone:
        result = await db.execute(select(User).where(User.phone == user_data.phone))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Phone already registered")
    user = User(email=user_data.email, phone=user_data.phone,
        hashed_password=get_password_hash(user_data.password),
        first_name=user_data.first_name, last_name=user_data.last_name,
        company_id=user_data.company_id, department=user_data.department,
        job_title=user_data.job_title, role=UserRole.USER, status=UserStatus.ACTIVE)
    db.add(user); await db.commit(); await db.refresh(user)
    logger.info("user_registered", user_id=user.id, email=user.email)
    return user

@router.post("/login", response_model=Token)
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if user.status != UserStatus.ACTIVE:
        raise HTTPException(status_code=403, detail="Account not active")
    import datetime
    user.last_login_at = datetime.datetime.utcnow()
    user.last_login_ip = request.client.host
    user.failed_login_attempts = 0
    access_token = create_access_token({"sub": user.id, "email": user.email, "role": user.role.value})
    refresh_token = create_refresh_token({"sub": user.id})
    session = UserSession(user_id=user.id, refresh_token=refresh_token,
        ip_address=request.client.host, user_agent=request.headers.get("user-agent"),
        expires_at=datetime.datetime.utcnow() + timedelta(days=7))
    db.add(session); await db.commit()
    logger.info("user_login", user_id=user.id, ip=request.client.host)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer",
        "expires_in": settings.JWT_EXPIRATION_HOURS * 3600, "user": user}

@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str, db: AsyncSession = Depends(get_db)):
    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    user_id = payload.get("sub")
    result = await db.execute(select(UserSession).where(
        UserSession.user_id == user_id, UserSession.refresh_token == refresh_token, UserSession.is_valid == True))
    session = result.scalar_one_or_none()
    if not session:
        raise HTTPException(status_code=401, detail="Session expired")
    import datetime
    if session.expires_at < datetime.datetime.utcnow():
        raise HTTPException(status_code=401, detail="Session expired")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    access_token = create_access_token({"sub": user.id, "email": user.email, "role": user.role.value})
    new_refresh = create_refresh_token({"sub": user.id})
    session.is_valid = False
    new_session = UserSession(user_id=user.id, refresh_token=new_refresh,
        expires_at=datetime.datetime.utcnow() + timedelta(days=7))
    db.add(new_session); await db.commit()
    return {"access_token": access_token, "refresh_token": new_refresh, "token_type": "bearer",
        "expires_in": settings.JWT_EXPIRATION_HOURS * 3600, "user": user}

@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = await db.execute(select(UserSession).where(
        UserSession.user_id == current_user.id, UserSession.is_valid == True))
    for session in result.scalars():
        session.is_valid = False
    await db.commit()
    logger.info("user_logout", user_id=current_user.id)
    return {"detail": "Successfully logged out"}

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@router.put("/me")
async def update_me(user_update: dict, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    for key, value in user_update.items():
        if hasattr(current_user, key) and key not in ["id", "hashed_password", "role"]:
            setattr(current_user, key, value)
    await db.commit(); await db.refresh(current_user)
    return current_user

@router.get("/oauth/google")
async def google_auth():
    return {"auth_url": GoogleOAuth.get_auth_url()}

@router.get("/oauth/google/callback")
async def google_callback(code: str, db: AsyncSession = Depends(get_db)):
    return await GoogleOAuth.handle_callback(code, db)

@router.get("/oauth/github")
async def github_auth():
    return {"auth_url": GitHubOAuth.get_auth_url()}

@router.get("/oauth/github/callback")
async def github_callback(code: str, db: AsyncSession = Depends(get_db)):
    return await GitHubOAuth.handle_callback(code, db)

@router.get("/oauth/microsoft")
async def microsoft_auth():
    return {"auth_url": MicrosoftOAuth.get_auth_url()}

@router.get("/oauth/microsoft/callback")
async def microsoft_callback(code: str, db: AsyncSession = Depends(get_db)):
    return await MicrosoftOAuth.handle_callback(code, db)

@router.post("/mfa/enable")
async def enable_mfa(current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    import pyotp
    secret = pyotp.random_base32()
    current_user.mfa_secret = secret
    await db.commit()
    uri = pyotp.totp.TOTP(secret).provisioning_uri(name=current_user.email, issuer_name="PhD Xpert Solver")
    return {"secret": secret, "qr_uri": uri}

@router.post("/mfa/verify")
async def verify_mfa(data: MFAVerify, current_user: User = Depends(get_current_active_user), db: AsyncSession = Depends(get_db)):
    import pyotp
    totp = pyotp.TOTP(current_user.mfa_secret)
    if totp.verify(data.code):
        current_user.mfa_enabled = True
        await db.commit()
        return {"detail": "MFA enabled successfully"}
    raise HTTPException(status_code=400, detail="Invalid MFA code")
