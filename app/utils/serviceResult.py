from app. schemas.item import Item
from app.utils.resultCode import SuccessCode, FailCode


class ServiceResult(object):
    def __init__(self, code: SuccessCode | FailCode, items: Item | list[Item] | None = None):
        if isinstance(code, FailCode):
            self.success = False
            self.code = code
            self.items = None
        else:
            self.success = True
            self.code = code
            self.items = items
