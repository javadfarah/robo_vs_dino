from pydantic import BaseModel


class InsertAction(BaseModel):
    position: str
    content: str
