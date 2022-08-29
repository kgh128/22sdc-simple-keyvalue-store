import json
import os

from app.schemas.item import Item, create_item
from app.utils.jsonUtils import ItemToJson


class FileCRUD:
    # noinspection PyMethodMayBeStatic
    def get_item(self, file_name: str) -> Item:
        try:
            with open(f'database/{file_name}', 'r') as file:
                item = json.load(file)
                return create_item(item["key"], item["value"])
        except FileNotFoundError:
            return None

    def get_all_items(self) -> list[Item]:
        items: list[Item] = []
        for file_name in os.listdir("database"):
            items.append(self.get_item(file_name))
        return items

    # noinspection PyMethodMayBeStatic
    def set_item(self, item):
        with open(f'database/{item.key}.json', 'w') as file:
            json.dump(item, file, cls=ItemToJson)

    # noinspection PyMethodMayBeStatic
    def delete_item(self, file_name: str) -> bool:
        try:
            os.remove(f'database/{file_name}')
            return True
        except FileNotFoundError:
            return False

    def delete_all_items(self):
        for file_name in os.listdir("database"):
            self.delete_item(file_name)
