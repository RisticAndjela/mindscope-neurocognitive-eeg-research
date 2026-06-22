from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import get_settings
from app.core.cors import configure_cors

settings = get_settings()

app = FastAPI(title=settings.app_name)
configure_cors(app, settings)

app.include_router(api_router, prefix=settings.api_prefix)


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": settings.app_name}
