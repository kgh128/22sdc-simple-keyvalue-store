from pydantic import BaseModel, Field


class Item(BaseModel):
    description: str | None = None
    key: int
    value: str | None = Field(default=None, max_length=1024)
