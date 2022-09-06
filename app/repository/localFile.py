import json
import os

from app.schemas.item import Item, create_item
from app.utils.jsonUtils import ItemToJson
from app.utils.fileUtils import get_path


class FileCRUD:
    def get_item(self, key: int) -> Item | None:
        file_path = f'database/{get_path(key)}'

        try:
            if os.path.getsize(file_path) == 0:
                self.delete_item(key)
                return None

            with open(file_path, 'r') as file:
                item = json.load(file)
                return create_item(item["key"], item["value"])

        except (OSError, ValueError):
            return None

    def get_all_items(self, keys_in_cache: list[int]) -> list[Item]:
        items: list[Item] = []

        for (path, dirs, files) in os.walk("database"):
            for file_name in files:
                key = int(os.path.splitext(file_name)[0])

                if key not in keys_in_cache:
                    item = self.get_item(key)

                    if item:
                        items.append(item)
        return items

    # noinspection PyMethodMayBeStatic
    def set_item(self, item: Item) -> bool:
        file_path = f'database/{get_path(item.key)}'

        try:
            with open(file_path, 'w') as file:
                json.dump(item, file, cls=ItemToJson)
            return True

        except (OSError, ValueError):
            return False

    # noinspection PyMethodMayBeStatic
    def delete_item(self, key: int) -> bool:
        file_path = f'database/{get_path(key)}'

        try:
            os.remove(file_path)
            return True

        except (OSError, ValueError):
            return False

    # noinspection PyMethodMayBeStatic
    def delete_all_items(self) -> None:
        for (path, dirs, files) in os.walk("database"):
            for file_name in files:
                file_path = os.path.join(path, file_name)
                os.remove(file_path)
