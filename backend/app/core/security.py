from functools import lru_cache

import jwt
from jwt import InvalidTokenError, PyJWKClient
from jwt.exceptions import PyJWKClientError

from app.core.config import Settings, get_settings


@lru_cache
def get_jwks_client(jwks_url: str) -> PyJWKClient:
    return PyJWKClient(jwks_url)


def verify_supabase_jwt(token: str, settings: Settings) -> dict[str, object]:
    signing_key = get_jwks_client(settings.supabase_jwks_url).get_signing_key_from_jwt(token)

    return jwt.decode(
        token,
        signing_key.key,
        algorithms=["RS256", "ES256"],
        audience=settings.supabase_jwt_audience,
        issuer=settings.supabase_issuer,
    )


def verify_supabase_jwt_with_settings(token: str) -> dict[str, object]:
    settings = get_settings()
    return verify_supabase_jwt(token, settings)


__all__ = [
    "InvalidTokenError",
    "PyJWKClientError",
    "verify_supabase_jwt",
    "verify_supabase_jwt_with_settings",
]
