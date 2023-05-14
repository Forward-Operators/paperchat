import sentry_sdk
from api.api_v1.api import api_router
from core.config import settings
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

# sentry_sdk.init(dsn=settings.SENTRY_DSN, traces_sample_rate=0.7)

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.mount("/.well-known", StaticFiles(directory="./.well-known"), name="static")
app.include_router(api_router, prefix=settings.API_V1_STR)
