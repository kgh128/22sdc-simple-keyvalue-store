from pydantic import BaseModel
from app.schemas.item import Item


class ServiceResult(BaseModel):
    description: str
    items: Item | list[Item] | None = None


def create_service_result(description: str, items: Item | list[Item] | None) -> ServiceResult:
    service_result = {
        "description": description,
        "items": items
    }
    return ServiceResult(**service_result)