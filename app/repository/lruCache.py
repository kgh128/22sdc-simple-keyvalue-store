from collections import OrderedDict

from app.schemas.item import Item, create_item
from app.repository.keyList import KeyList
from app.repository.localFile import FileCRUD

KEY_LIST = KeyList()
MAX_SIZE = 10000


class LruCache:
    cache: OrderedDict[int, str] = OrderedDict()

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
            pop_item = self.cache.popitem(last=False)
            KEY_LIST.set_key(pop_item[0], 'local')

        self.cache[item.key] = item.value
        KEY_LIST.set_key(item.key, 'cache')
        return None

    def delete_item(self, key: int) -> None:
        if key in self.cache:
            del self.cache[key]
        return None

    def delete_all_items(self):
        self.cache.clear()
        FileCRUD().delete_all_items()
