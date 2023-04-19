from pydantic import BaseModel


class TaskTicket(BaseModel):
    """ID and status for the async tasks"""

    task_id: str
    status: str
