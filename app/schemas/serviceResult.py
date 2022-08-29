from pydantic import BaseModel
from app.schemas.item import Item


class ServiceResult(BaseModel):
    items: Item | list[Item] | None = None


def create_service_result(items: Item | list[Item] | None) -> ServiceResult:
    service_result = {"items": items}
    return ServiceResult(**service_result)