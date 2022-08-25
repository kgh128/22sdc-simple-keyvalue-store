from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.schemas.item import Item
from app.services.item import ItemService


router = APIRouter(
    prefix="/item",
    tags=["item"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{key}", response_model=Item)
async def get_item(key: int):
    return ItemService.get_item(key)
