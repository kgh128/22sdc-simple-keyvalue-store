from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.schemas.item import Item

store = {1: "hello"}


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
