from app.schemas.item import Item, create_item
from app.repository.fileItem import FileCRUD


class ItemCRUD:
    # 데이터 저장 dictionary
    store: dict[int, str] = {}

    def get_item(self, key: int) -> Item:
        if key not in self.store:
            test = FileCRUD().get_item(key)
            item = create_item(key, test[key])
            return item
        item = create_item(key, self.store[key])
        return item

    def get_all_items(self) -> list[Item]:
        items: list[Item] = []
        for key in list(self.store.keys()):
            items.append(create_item(key, self.store[key]))
        return items

    def put_item(self, item: Item) -> Item:
        if item.key in self.store:
            return None
        self.store[item.key] = item.value
        FileCRUD().put_item(item)
        return item

    def update_item(self, item: Item) -> Item:
        if item.key not in self.store:
            return None
        self.store[item.key] = item.value
        FileCRUD().put_item(item)
        return item

    def delete_item(self, key: int) -> Item:
        if key not in self.store:
            return None
        item = create_item(key, self.store[key])
        del self.store[key]
        return item

    def delete_all_items(self) -> list[Item]:
        items = self.get_all_items()
        for key in list(self.store.keys()):
            del self.store[key]
        return items
