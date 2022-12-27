from pydantic import BaseModel


class AttackAction(BaseModel):
    x: int
    y: int
