from collections import OrderedDict

from app.schemas.item import Item, create_item
from app.repository.keyList import KeyList

KEY_LIST = KeyList()
MAX_SIZE = 10000


class LruCache:
    cache: OrderedDict[int, str] = OrderedDict()

    def get_item(self, key: int) -> Item | None:
        if key in self.cache:
            self.cache.move_to_end(key)
            return create_item(key, self.cache[key])
        return None

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
