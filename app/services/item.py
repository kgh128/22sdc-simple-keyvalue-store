from fastapi import HTTPException

from app.schemas.item import Item
# from app.utils.appExceptions import AppException
# from app.utils.serviceResult import ServiceResult

# 데이터 저장 dictionary
store = {1: "hello"}


class ItemService:
    # noinspection PyMethodMayBeStatic
    def get_item(key: int):
        if key not in store:
            raise HTTPException(status_code=404, detail="Item not found")

        item = {
            "description": "Get item",
            "key": key,
            "value": store[key]}
        return Item(**item)

    def put_item(item: Item):
        store[item.key] = item.value

        if item.key not in store:
            item.description = "Put item"
        item.description = "Update item"

        return item

    def delete_item(key: int):
        item = ItemService.get_item(key)
        item.description = "Delete item"
        del store[key]
        return item
