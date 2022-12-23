from typing import Optional

from redis_om import (
    EmbeddedJsonModel,
    JsonModel,
    Field,
    Migrator,
)


class Creature(EmbeddedJsonModel):
    name: str


class LandField(JsonModel):
    x: str = Field(index=True)
    y: str = Field(index=True)
    pk: str = Field(index=True)
    content: Optional[Creature] = None
