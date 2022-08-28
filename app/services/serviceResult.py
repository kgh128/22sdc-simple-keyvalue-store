from app.schemas.item import Item
from app.schemas.serviceResult import ServiceResult


def create_service_result(description: str, items: Item | list[Item] | None):
    service_result = {
        "description": description,
        "items": items
    }
    return ServiceResult(**service_result)
