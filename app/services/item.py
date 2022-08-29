from fastapi import HTTPException

from app.schemas.item import Item
from app.schemas.serviceResult import ServiceResult, create_service_result

from app.repository.inMemoryItem import ItemCRUD


class ItemService:
    # noinspection PyMethodMayBeStatic
    def get_item(self, key: int) -> ServiceResult:
        item = ItemCRUD().get_item(key)
        if not item:
            raise HTTPException(status_code=404, detail="해당 key가 존재하지 않아 value를 찾을 수 없습니다.")
        return create_service_result(item)

    # noinspection PyMethodMayBeStatic
    def get_all_items(self) -> ServiceResult:
        items = ItemCRUD().get_all_items()
        return create_service_result(items)

    # noinspection PyMethodMayBeStatic
    def set_item(self, item: Item):
        ItemCRUD().set_item(item)

    # noinspection PyMethodMayBeStatic
    def delete_item(self, key: int):
        item = ItemCRUD().delete_item(key)
        if not item:
            raise HTTPException(status_code=404, detail="해당 key가 존재하지 않아 value를 삭제할 수 없습니다.")

    # noinspection PyMethodMayBeStatic
    def delete_all_items(self):
        ItemCRUD().delete_all_items()
