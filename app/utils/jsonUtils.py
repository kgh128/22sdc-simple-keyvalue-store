import json
from app.schemas.item import Item


class ItemToJson(json.JSONEncoder):
    def default(self, obj: Item):
        if isinstance(obj, Item):
            return {"key": obj.key, "value": obj.value}
        return json.JSONEncoder.default(self, obj)
