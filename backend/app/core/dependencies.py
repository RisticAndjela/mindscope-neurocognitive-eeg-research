from dataclasses import dataclass, field
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.core.security import InvalidTokenError, PyJWKClientError, verify_supabase_jwt
from app.db.session import get_db_session


bearer_scheme = HTTPBearer(auto_error=False)


@dataclass(slots=True)
class CurrentUser:
    id: UUID
    email: str | None
    role: str | None
    claims: dict[str, object] = field(default_factory=dict)


def get_app_settings() -> Settings:
    return get_settings()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    settings: Settings = Depends(get_app_settings),
) -> CurrentUser:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")

    if not settings.supabase_url or not settings.supabase_jwks_url:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Auth is not configured")

    token = credentials.credentials

    try:
        payload = verify_supabase_jwt(token, settings)
    except (InvalidTokenError, PyJWKClientError) as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token") from exc

    subject = payload.get("sub")
    if not subject:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing subject")

    try:
        parsed_user_id = UUID(str(subject))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token") from exc

    email = payload.get("email")
    role = payload.get("role")

    return CurrentUser(
        id=parsed_user_id,
        email=str(email) if isinstance(email, str) else None,
        role=str(role) if isinstance(role, str) else None,
        claims=dict(payload),
    )


async def require_research_user(
    current_user: CurrentUser = Depends(get_current_user),
    session: AsyncSession = Depends(get_db_session),
) -> CurrentUser:
    query = text(
        """
        select id, email, role::text as role
        from public.profiles
        where id = :user_id
        """
    )
    result = await session.execute(query, {"user_id": str(current_user.id)})
    row = result.mappings().first()

    if row is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Profile not found")

    if row["role"] != "research":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Research access required")

    return CurrentUser(
        id=current_user.id,
        email=current_user.email or row["email"],
        role=row["role"],
        claims=current_user.claims,
    )
