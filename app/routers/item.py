from fastapi import APIRouter

from app.services.item import ItemService
from app.schemas.item import Item

from app.utils.serviceResult import handle_result

router = APIRouter(
    prefix="/item",
    tags=["item"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{key}", response_model=Item)
async def get_item(key: int):
    result = ItemService.get_item(key)
    return handle_result(result)
