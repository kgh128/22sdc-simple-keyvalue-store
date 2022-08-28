from pydantic import BaseModel
from app.schemas.item import Item


class ServiceResult(BaseModel):
    description: str
    items: Item | list[Item] | None = None
