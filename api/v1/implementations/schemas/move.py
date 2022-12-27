from pydantic import BaseModel

class MoveAction(BaseModel):
    direction: str
    x: int
    y: int