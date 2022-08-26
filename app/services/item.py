from fastapi import HTTPException

from app.schemas.item import Item


class ItemService:
    # noinspection PyMethodMayBeStatic
    def get_item(self, key: int) -> Item:
        item = ItemCRUD().get_item(key)
        if not item:
            raise HTTPException(status_code=404, detail="해당 key가 존재하지 않아 value를 찾을 수 없습니다.")
        return item

    # noinspection PyMethodMayBeStatic
    def put_item(self, item: Item) -> Item:
        item = ItemCRUD().put_item(item)
        if not item:
            raise HTTPException(status_code=422, detail="해당 key가 이미 존재하여 value를 새로 입력할 수 없습니다.")
        return item

    # noinspection PyMethodMayBeStatic
    def update_item(self, item: Item) -> Item:
        item = ItemCRUD().update_item(item)
        if not item:
            raise HTTPException(status_code=404, detail="해당 key가 존재하지 않아 value를 업데이트 할 수 없습니다.")
        return item

    # noinspection PyMethodMayBeStatic
    def delete_item(self, key: int) -> Item:
        item = ItemCRUD().delete_item(key)
        if not item:
            raise HTTPException(status_code=404, detail="해당 key가 존재하지 않아 value를 삭제할 수 없습니다.")
        return item


class ItemCRUD:
    # 데이터 저장 dictionary
    store: dict[int, str] = {}

    # noinspection PyMethodMayBeStatic
    def create_item(self, description: str, key: int, value: str):
        item = {"description": description,
                "key": key,
                "value": value}
        return Item(**item)

    def get_item(self, key: int):
        if key not in self.store:
            return None
        item = self.create_item("Get item", key, self.store[key])
        return item

    def put_item(self, item: Item):
        if item.key in self.store:
            return None
        item = self.create_item("Put item", item.key, item.value)
        self.store[item.key] = item.value
        return item

    def update_item(self, item: Item):
        if item.key not in self.store:
            return None
        item = self.create_item("Update item", item.key, item.value)
        self.store[item.key] = item.value
        return item

    def delete_item(self, key: int):
        if key not in self.store:
            return None
        item = self.create_item("Delete item", key, self.store[key])
        del self.store[key]
        return item
