from fastapi import HTTPException

from app.repository.lruCache import LruCache
from app.schemas.item import Item
from app.schemas.responseDTO import ResponseDTO, create_response
from app.schemas.responseDTO import GetResponseDTO, create_get_response

CACHE = LruCache()


class ItemService:
    # noinspection PyMethodMayBeStatic
    def get_item(self, key: int) -> GetResponseDTO:
        item = CACHE.get_item(key)
        if not item:
            raise HTTPException(status_code=404, detail="해당 key가 존재하지 않아 value를 찾을 수 없습니다.")
        return create_get_response("Success - Get item.", item)

    # noinspection PyMethodMayBeStatic
    def get_all_items(self) -> GetResponseDTO:
        items = CACHE.get_all_items()
        if not items:
            raise HTTPException(status_code=404, detail="데이터베이스가 비어있습니다.")
        return create_get_response("Success - Get all items.", items)

    # noinspection PyMethodMayBeStatic
    def set_item(self, item: Item) -> ResponseDTO:
        item = CACHE.set_item(item)
        if not item:
            raise HTTPException(status_code=500, detail="데이터 저장에 실패하였습니다.")
        return create_response("Success - Set item.")

    # noinspection PyMethodMayBeStatic
    def delete_item(self, key: int) -> ResponseDTO:
        item = CACHE.delete_item(key)
        if not item:
            raise HTTPException(status_code=404, detail="해당 key가 존재하지 않아 value를 삭제할 수 없습니다.")
        return create_response("Success - Delete item.")

    # noinspection PyMethodMayBeStatic
    def delete_all_items(self) -> ResponseDTO:
        CACHE.delete_all_items()
        return create_response("Success - Delete all items.")
