from collections import OrderedDict

from app.schemas.item import Item, create_item
from app.repository.localFile import FileCRUD

MAX_SIZE = 10000


class LruCache:
    cache: OrderedDict[int, str]

    def __init__(self):
        self.cache = OrderedDict()

    def get_item(self, key: int) -> Item | None:
        if key in self.cache:
            self.cache.move_to_end(key)
            return create_item(key, self.cache[key])
        return None

    # noinspection PyMethodMayBeStatic
    def get_all_items(self) -> list[Item]:
        items: list[Item] = []
        keys_in_cache = list(self.cache.keys())

        for key in keys_in_cache:
            item = create_item(key, self.cache[key])
            items.append(item)

        items.extend(FileCRUD().get_all_items(keys_in_cache))
        return items

    def set_item(self, item: Item) -> None:
        if item.key in self.cache:
            self.cache.move_to_end(item.key)

        if len(self.cache) == MAX_SIZE:
            self.cache.popitem(last=False)

        self.cache[item.key] = item.value
        return None

    def delete_item(self, key: int) -> None:
        if key in self.cache:
            del self.cache[key]
        return None

    def delete_all_items(self):
        self.cache.clear()
        FileCRUD().delete_all_items()
