from fastapi import HTTPException

from app.repository.lruCache import LruCache
from app.schemas.item import Item
from app.schemas.serviceResult import ServiceResult, create_service_result

CACHE = LruCache()


class ItemService:
    # noinspection PyMethodMayBeStatic
    def get_item(self, key: int) -> ServiceResult:
        item = CACHE.get_item(key)
        if not item:
            raise HTTPException(status_code=404, detail="해당 key가 존재하지 않아 value를 찾을 수 없습니다.")
        return create_service_result(item)

    # noinspection PyMethodMayBeStatic
    def get_all_items(self) -> ServiceResult:
        items = CACHE.get_all_items()
        return create_service_result(items)

    # noinspection PyMethodMayBeStatic
    def set_item(self, item: Item):
        item = CACHE.set_item(item)
        if not item:
            raise HTTPException(status_code=500, detail="데이터 저장에 실패하였습니다.")

    # noinspection PyMethodMayBeStatic
    def delete_item(self, key: int):
        item = CACHE.delete_item(key)
        if not item:
            raise HTTPException(status_code=404, detail="해당 key가 존재하지 않아 value를 삭제할 수 없습니다.")

    # noinspection PyMethodMayBeStatic
    def delete_all_items(self):
        CACHE.delete_all_items()
