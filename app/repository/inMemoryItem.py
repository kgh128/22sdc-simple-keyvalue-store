from app.schemas.item import Item, create_item
from app.repository.fileItem import FileCRUD


class ItemCRUD:
    # 데이터 저장 dictionary
    store: dict[int, str] = {}

    def get_item(self, key: int) -> Item:
        if key in self.store:
            return create_item(key, self.store[key])
        else:
            return FileCRUD().get_item(f'{key}.json')

    # noinspection PyMethodMayBeStatic
    def get_all_items(self) -> list[Item]:
        return FileCRUD().get_all_items()

    def set_item(self, item: Item):
        self.store[item.key] = item.value
        FileCRUD().set_item(item)

    def delete_item(self, key: int) -> bool:
        if key in self.store:
            del self.store[key]
            return True
        else:
            return FileCRUD().delete_item(f'{key}.json')

    def delete_all_items(self):
        for key in list(self.store.keys()):
            del self.store[key]
        FileCRUD().delete_all_items()
