import os

from celery.result import AsyncResult
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from api.models import TaskTicket
from worker.tasks import ingest_task

router = APIRouter()


@router.post("/ingest", response_model=TaskTicket, status_code=202)
async def ingest(query: str):
    """Create celery ingest task. Return task_id to client in order to check status of task."""
    task = ingest_task.delay(query)
    return {"task_id": task.id, "status": "Processing"}


@router.get(
    "/ingest/result/{task_id}",
    response_model=TaskTicket,
    status_code=200,
    responses={
        404: {"description": "Task not found"},
        202: {"description": "Task still processing"},
    },
)
async def ingest_result(task_id: str):
    """Fetch result of ingest task."""
    task = AsyncResult(task_id)
    if not task.ready():
        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content={"task_id": task.id, "status": "Processing"},
        )
    result = task.get()
    return {"task_id": task.id, "status": "Success", "result": result}
