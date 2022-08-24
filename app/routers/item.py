from fastapi import APIRouter
from pydantic import BaseModel, Field

store = {1: "hello"}


class Item(BaseModel):
    key: int
    value: str | None = Field(default=None, max_length=1024)


router = APIRouter(
    prefix="/item",
    tags=["item"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{key}", response_model=Item)
async def get_item(key: int):
    if key in store:
        item = {"key": key, "value": store[key]}
        item = Item(**item)
        return item
