from fastapi import HTTPException

from app.schemas.item import Item
from app.schemas.serviceResult import ServiceResult

from app.repository.inMemoryItem import ItemCRUD

from app.services.serviceResult import create_service_result


class ItemService:
    # noinspection PyMethodMayBeStatic
    def get_item(self, key: int) -> ServiceResult:
        item = ItemCRUD().get_item(key)
        if not item:
            raise HTTPException(status_code=404, detail="해당 key가 존재하지 않아 value를 찾을 수 없습니다.")
        return create_service_result("Get Item", item)

    # noinspection PyMethodMayBeStatic
    def get_all_items(self) -> ServiceResult:
        items = ItemCRUD().get_all_items()
        return create_service_result("Get all Items", items)

    # noinspection PyMethodMayBeStatic
    def put_item(self, item: Item) -> ServiceResult:
        item = ItemCRUD().put_item(item)
        if not item:
            raise HTTPException(status_code=422, detail="해당 key가 이미 존재하여 value를 새로 입력할 수 없습니다.")
        return create_service_result("Put Item", item)

    # noinspection PyMethodMayBeStatic
    def update_item(self, item: Item) -> ServiceResult:
        item = ItemCRUD().update_item(item)
        if not item:
            raise HTTPException(status_code=404, detail="해당 key가 존재하지 않아 value를 업데이트 할 수 없습니다.")
        return create_service_result("Update Item", item)

    # noinspection PyMethodMayBeStatic
    def delete_item(self, key: int) -> ServiceResult:
        item = ItemCRUD().delete_item(key)
        if not item:
            raise HTTPException(status_code=404, detail="해당 key가 존재하지 않아 value를 삭제할 수 없습니다.")
        return create_service_result("Delete Item", item)

    # noinspection PyMethodMayBeStatic
    def delete_all_items(self) -> ServiceResult:
        items = ItemCRUD().delete_all_items()
        return create_service_result("Delete all items", items)
