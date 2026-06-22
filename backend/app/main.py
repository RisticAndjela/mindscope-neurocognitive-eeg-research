from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.core.cors import configure_cors
from app.core import logging as _logging  # noqa: F401

settings = get_settings()

fastapi_app = FastAPI(title=settings.app_name)

fastapi_app.include_router(api_router, prefix=settings.api_prefix)


@fastapi_app.get("/health")
async def health_check():
    return {"status": "ok", "service": settings.app_name}


app = configure_cors(fastapi_app, settings)
