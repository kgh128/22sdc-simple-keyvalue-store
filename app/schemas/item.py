from pydantic import BaseModel, Field


class Item(BaseModel):
    key: int
    value: str | None = Field(default=None, max_length=1024)


def create_item(key: int, value: str | None = None) -> Item:
    item = {
        "key": key,
        "value": value
    }
    return Item(**item)
