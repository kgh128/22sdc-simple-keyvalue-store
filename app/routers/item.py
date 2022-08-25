from fastapi import APIRouter, HTTPException
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
    if key not in store:
        raise HTTPException(status_code=404, detail="Item not found")
    item = {"key": key, "value": store[key]}
    return Item(**item)
