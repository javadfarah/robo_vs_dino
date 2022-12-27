from typing import Optional
from settings import redis_instance
from redis_om import (
    EmbeddedJsonModel,
    JsonModel,
    Field,
    Migrator,
    get_redis_connection
)


class LandField(JsonModel):
    x: str = Field(index=True)
    y: str = Field(index=True)
    id: str = Field(index=True)
    content: Optional[str] = Field(index=True)