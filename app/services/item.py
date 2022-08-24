from app.main import store
from app.schemas.item import Item
from app.utils.appExceptions import AppException
from app.utils.serviceResult import ServiceResult


class ItemService:
    # noinspection PyMethodMayBeStatic
    def get_item(self, key: int) -> ServiceResult:
        if key in store:
            item = Item(key, store[key])
            return ServiceResult(item)
        return ServiceResult(AppException.ItemNotFound({"key": key}))
