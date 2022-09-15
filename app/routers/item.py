from fastapi import APIRouter, HTTPException

from app.schemas.item import Item
from app.schemas.responseDTO import ResponseDTO, create_response
from app.schemas.responseDTO import GetResponseDTO, create_get_response
from app.services.item import ItemService
from app.utils.resultCode import SuccessCode, FailCode

router = APIRouter(
    prefix="/items",
    tags=["item"],
    responses={404: {"description": "Not found"}},
)


@router.get("/{key}", response_model=GetResponseDTO)
async def get_item(key: int):
    service_result = ItemService().get_item(key)

    if service_result.code == FailCode.KEY_NOT_FOUND:
        raise HTTPException(status_code=404, detail="해당 key가 존재하지 않아 value를 찾을 수 없습니다.")
    if service_result.code == SuccessCode.GET_SUCCESS:
        return create_get_response("Success - Get item.", service_result.items)


@router.get("/", response_model=GetResponseDTO)
async def get_all_items():
    service_result = ItemService().get_all_items()

    return create_get_response("Success - Get all items.", service_result.items)


@router.post("/", response_model=ResponseDTO)
async def set_item(item: Item):
    service_result = ItemService().set_item(item)

    if service_result.code == FailCode.SAVE_LOCAL_FAIL:
        raise HTTPException(status_code=500, detail="데이터 저장에 실패하였습니다.")
    if service_result.code == FailCode.UPLOAD_S3_FAIL:
        raise HTTPException(status_code=500, detail="데이터 업로드에 실패하였습니다.")
    if service_result.code == SuccessCode.SET_SUCCESS:
        return create_response("Success - Set item.")


@router.delete("/{key}", response_model=ResponseDTO)
async def delete_item(key: int):
    service_result = ItemService().delete_item(key)

    if service_result.code == FailCode.KEY_NOT_FOUND:
        raise HTTPException(status_code=404, detail="해당 key가 존재하지 않아 value를 삭제할 수 없습니다.")
    if service_result.code == FailCode.DELETE_FAIL:
        raise HTTPException(status_code=500, detail="데이터 삭제에 실패하였습니다.")
    if service_result.code == SuccessCode.DELETE_SUCCESS:
        return create_response("Success - Delete item.")


@router.delete("/", response_model=ResponseDTO)
async def delete_all_items():
    service_result = ItemService().delete_all_items()

    if service_result.code == FailCode.DELETE_ALL_FAIL:
        raise HTTPException(status_code=500, detail="데이터 전체 삭제에 실패하였습니다.")
    if service_result.code == SuccessCode.DELETE_ALL_SUCCESS:
        return create_response("Success - Delete all items.")
