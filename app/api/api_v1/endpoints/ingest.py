import os

from core.config import settings
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

router = APIRouter()


@router.post("/ingest")
async def ingest(query: str):
    # placeholder, will be replaced with actual ingest code
    # probably with a call to a celery task as it takes a while
    return status.HTTP_200_OK
