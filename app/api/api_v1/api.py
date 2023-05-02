from api.api_v1.endpoints import ask, ingest
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(ingest.router)
api_router.include_router(ask.router)
