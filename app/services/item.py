from fastapi import HTTPException

from app.repository.keyList import KeyList
from app.repository.lruCache import LruCache
from app.repository.localFile import FileCRUD
from app.repository.S3Storage import S3Storage
from app.schemas.item import Item
from app.schemas.responseDTO import ResponseDTO, create_response
from app.schemas.responseDTO import GetResponseDTO, create_get_response
from app.utils.resultCode import SuccessCode, FailCode
from app.utils.serviceResult import ServiceResult

KEY_LIST = KeyList()
CACHE = LruCache()


class ItemService:
    # noinspection PyMethodMayBeStatic
    def get_item(self, key: int) -> ServiceResult:
        # key list에 존재하는 key인지 확인
        if not KEY_LIST.is_in_key_list(key):
            return ServiceResult(FailCode.KEY_NOT_FOUND)

        # 존재하는 key이면 저장되어 있는 위치에서 get
        location = KEY_LIST.get_location(key)

        # LRU Cache에서 get
        if location == 'cache':
            item = CACHE.get_item(key)
            if item:
                return ServiceResult(SuccessCode.GET_SUCCESS, item)
            location = 'local'

        # Local File에서 get
        if location == 'local':
            item = FileCRUD().get_item(key)
            if item:
                CACHE.set_item(item)
                return ServiceResult(SuccessCode.GET_SUCCESS, item)
            location = 'S3'

        # S3 Storage에서 get
        if location == 'S3':
            success_in_s3 = S3Storage().download_item(key)
            if success_in_s3:
                item = FileCRUD().get_item(key)
                CACHE.set_item(item)
                return ServiceResult(SuccessCode.GET_SUCCESS, item)

        # key는 key list에 있는데, 실제 데이터는 store에 없는 경우
        KEY_LIST.delete_key(key)
        return ServiceResult(FailCode.KEY_NOT_FOUND)

    # noinspection PyMethodMayBeStatic
    def get_all_items(self) -> GetResponseDTO:
        items = CACHE.get_all_items()
        if not items:
            raise HTTPException(status_code=404, detail="데이터베이스가 비어있습니다.")
        return create_get_response("Success - Get all items.", items)

    # noinspection PyMethodMayBeStatic
    def set_item(self, item: Item) -> ServiceResult:
        # LRU Cache에 set
        CACHE.set_item(item)

        # Local File에 set
        success_in_local = FileCRUD().set_item(item)
        if not success_in_local:
            CACHE.delete_item(item.key)
            KEY_LIST.delete_key(item.key)
            return ServiceResult(FailCode.SAVE_LOCAL_FAIL)

        # S3 Storage에 upload
        success_in_s3 = S3Storage().upload_item(item)
        if not success_in_s3:
            CACHE.delete_item(item.key)
            KEY_LIST.delete_key(item.key)
            return ServiceResult(FailCode.UPLOAD_S3_FAIL)

        # 모든 store에 set 성공한 경우
        return ServiceResult(SuccessCode.SET_SUCCESS)

    # noinspection PyMethodMayBeStatic
    def delete_item(self, key: int) -> ServiceResult:
        # key list에 존재하는 key인지 확인
        if not KEY_LIST.is_in_key_list(key):
            return ServiceResult(FailCode.KEY_NOT_FOUND)

        # 존재하는 key이면 모든 store에서 delete

        # LRU Cache에서 delete
        CACHE.delete_item(key)

        # Local File에서 delete
        success_in_local = FileCRUD().delete_item(key)
        if not success_in_local:
            KEY_LIST.set_key(key, 'local')
            return ServiceResult(FailCode.DELETE_FAIL)

        # S3 Storage에서 delete
        success_in_s3 = S3Storage().delete_item(key)
        if not success_in_s3:
            KEY_LIST.set_key(key, 'S3')
            return ServiceResult(FailCode.DELETE_FAIL)

        # 모든 store에서 delete가 성공한 경우
        KEY_LIST.delete_key(key)
        return ServiceResult(SuccessCode.DELETE_SUCCESS)

    # noinspection PyMethodMayBeStatic
    def delete_all_items(self) -> ResponseDTO:
        CACHE.delete_all_items()
        return create_response("Success - Delete all items.")
