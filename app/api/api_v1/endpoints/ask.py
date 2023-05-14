import os

from core.config import settings
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import BaseModel
from resources.arxiv import chat


class Query(BaseModel):
    question: str


router = APIRouter()


@router.post("/ask")
async def ask(query: Query):
    print(query.question)
    answer = chat(query.question)
    return answer
