import json

from app.schemas.item import Item, create_item
from app.utils.jsonUtils import ItemToJson


class FileCRUD:
    # noinspection PyMethodMayBeStatic
    def get_item(self, key) -> Item:
        with open(f'database/data{key}.json', 'r') as file:
            item = json.load(file)
            return create_item(item.key, item.value)

    # noinspection PyMethodMayBeStatic
    def put_item(self, item) -> None:
        with open(f'database/data{item.key}.json', 'w') as file:
            json.dump(item, file, cls=ItemToJson)
        return None
