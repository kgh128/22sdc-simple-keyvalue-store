from collections import OrderedDict

from app.schemas.item import Item, create_item
from app.repository.fileItem import FileCRUD

MAX_SIZE = 128


class LruCache:
    dir_name: str
    cache: OrderedDict[int, str]

    def __init__(self, cache_num):
        self.dir_name = f'DB{cache_num}'
        self.cache = OrderedDict()

    def get_item(self, key: int) -> Item:
        if key in self.cache:
            self.cache.move_to_end(key)
            return create_item(key, self.cache[key])

        if len(self.cache) == MAX_SIZE:
            self.cache.popitem(last=False)

        item = FileCRUD().get_item(self.dir_name, f'{key}.json')
        self.cache[key] = item.value
        return item

    # noinspection PyMethodMayBeStatic
    def get_all_items(self) -> list[Item]:
        return FileCRUD().get_all_items()

    # noinspection PyMethodMayBeStatic
    def set_item(self, item: Item):
        FileCRUD().set_item(self.dir_name, item)

    def delete_item(self, key: int) -> bool:
        if key in self.cache:
            del self.cache[key]
        return FileCRUD().delete_item(self.dir_name, f'{key}.json')

    def delete_all_items(self):
        self.cache.clear()
        FileCRUD().delete_all_items()
