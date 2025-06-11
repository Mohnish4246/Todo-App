from pydantic import BaseModel
from typing import Optional

class Todo(BaseModel):
    title: str
    completed: bool = False
    due_date: Optional[str] = None  # e.g., "2025-06-10"
    tags: Optional[str] = None      # e.g., "work,urgent"
    