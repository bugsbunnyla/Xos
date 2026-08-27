from fastapi import Depends, HTTPException, status
from functools import wraps
from app.models.user import User, UserRole

def require_role(allowed_roles: list):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user: User = None, **kwargs):
            if not current_user or current_user.role not in allowed_roles:
                raise HTTPException(status_code=403, detail="Insufficient permissions")
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator

require_admin = require_role([UserRole.ADMIN, UserRole.SUPER_ADMIN])
require_manager = require_role([UserRole.MANAGER, UserRole.ADMIN, UserRole.SUPER_ADMIN])
