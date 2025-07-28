from pydantic import BaseModel, Field
from datetime import datetime

class Todo(BaseModel):
    title: str
    description: str
    is_completed: bool = False
    is_deleted: bool = False
    created_on: int = Field(default_factory=lambda: int(datetime.timestamp(datetime.now())))
    updated_at: int = Field(default_factory=lambda: int(datetime.timestamp(datetime.now())))