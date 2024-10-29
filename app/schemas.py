from pydantic import BaseModel

class TodoUpdate(BaseModel):
    title: str
    description: str