from pydantic import BaseModel
from app.schemas.item import Item


class ResponseDTO(BaseModel):
    description: str


def create_response(description: str) -> ResponseDTO:
    response = {
        "description": description
    }
    return ResponseDTO(**response)


class GetResponseDTO(ResponseDTO):
    items: Item | list[Item] | None = None


def create_get_response(description: str, items: Item | list[Item] | None) -> GetResponseDTO:
    get_response = {
        "description": description,
        "items": items
    }
    return GetResponseDTO(**get_response)