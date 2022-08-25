from pydantic import BaseModel, Field


class Item(BaseModel):
    key: int
    value: str | None = Field(default=None, max_length=1024)
