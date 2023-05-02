import os

from core.config import settings
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import BaseModel
from resources.arxiv import chat

router = APIRouter()


@router.post("/ask")
async def ingest(query: str = Body(...)):
    answer = chat(query)
    return answer
