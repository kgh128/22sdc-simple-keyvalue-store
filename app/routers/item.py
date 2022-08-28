from fastapi import APIRouter

from app.schemas.item import Item
from app.schemas.serviceResult import ServiceResult
from app.services.item import ItemService

router = APIRouter(
    prefix="/items",
    tags=["item"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{key}", response_model=ServiceResult)
async def get_item(key: int):
    return ItemService().get_item(key)


@router.get("/", response_model=ServiceResult)
async def get_all_items():
    return ItemService().get_all_items()


@router.post("/", response_model=ServiceResult)
async def put_item(item: Item):
    return ItemService().put_item(item)


@router.put("/", response_model=ServiceResult)
async def update_item(item: Item):
    return ItemService().update_item(item)


@router.delete("/{key}", response_model=ServiceResult)
async def delete_item(key: int):
    return ItemService().delete_item(key)


@router.delete("/", response_model=ServiceResult)
async def delete_all_items():
    return ItemService().delete_all_items()
