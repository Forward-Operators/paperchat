from fastapi import APIRouter

from api.api_v1.endpoints import ask, ingest

api_router = APIRouter()
api_router.include_router(ingest.router)
api_router.include_router(ask.router)
