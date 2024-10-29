from datetime import date
from pydantic import BaseModel
from typing import Optional, List

class TodoUpdate(BaseModel):
    title: str
    description: Optional[str] = None
    datetime: Optional[date] = None
    tags: Optional[str] = None