from fastapi import APIRouter

from app.schemas.item import Item
from app.services.item import ItemService

router = APIRouter(
    prefix="/item",
    tags=["item"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{key}", response_model=Item)
async def get_item(key: int):
    return ItemService().get_item(key)


@router.post("/", response_model=Item)
async def put_item(item: Item):
    return ItemService().put_item(item)


@router.put("/", response_model=Item)
async def update_item(item: Item):
    return ItemService().update_item(item)


@router.delete("/{key}", response_model=Item)
async def delete_item(key: int):
    return ItemService().delete_item(key)
