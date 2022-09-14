from fastapi import HTTPException

from app.repository.keyList import KeyList
from app.repository.lruCache import LruCache
from app.repository.localFile import FileCRUD
from app.repository.S3Storage import S3Storage
from app.schemas.item import Item
from app.schemas.responseDTO import ResponseDTO, create_response
from app.schemas.responseDTO import GetResponseDTO, create_get_response

KEY_LIST = KeyList()
CACHE = LruCache()


class ItemService:
    # noinspection PyMethodMayBeStatic
    def get_item(self, key: int) -> GetResponseDTO:
        # key list에 존재하는 key인지 확인
        if not KEY_LIST.is_in_key_list(key):
            raise HTTPException(status_code=404, detail="해당 key가 존재하지 않아 value를 찾을 수 없습니다.")

        # 존재하는 key이면 저장되어 있는 위치에서 get
        location = KEY_LIST.get_location(key)

        if location == 'cache':
            item = CACHE.get_item(key)
            if item:
                return create_get_response("Success - Get item.", item)
            location = 'local'

        if location == 'local':
            item = FileCRUD().get_item(key)
            if item:
                CACHE.set_item(item)
                return create_get_response("Success - Get item.", item)
            location = 'S3'

        if location == 'S3':
            success_in_s3 = S3Storage().download_item(key)
            if success_in_s3:
                item = FileCRUD().get_item(key)
                CACHE.set_item(item)
                return create_get_response("Success - Get item.", item)

        # key는 key list에 있는데, 실제 데이터는 store에 없는 경우
        KEY_LIST.delete_key(key)
        raise HTTPException(status_code=404, detail="해당 key가 존재하지 않아 value를 찾을 수 없습니다.")

    # noinspection PyMethodMayBeStatic
    def get_all_items(self) -> GetResponseDTO:
        items = CACHE.get_all_items()
        if not items:
            raise HTTPException(status_code=404, detail="데이터베이스가 비어있습니다.")
        return create_get_response("Success - Get all items.", items)

    # noinspection PyMethodMayBeStatic
    def set_item(self, item: Item) -> ResponseDTO:
        # LRU Cache에 set
        CACHE.set_item(item)

        # Local File에 set
        success_in_local = FileCRUD().set_item(item)
        if not success_in_local:
            raise HTTPException(status_code=500, detail="데이터 저장에 실패하였습니다.")

        # S3 Storage에 upload
        success_in_s3 = S3Storage().upload_item(item)
        if not success_in_s3:
            raise HTTPException(status_code=500, detail="데이터 업로드에 실패하였습니다.")

        # 모든 store에 set 성공한 경우
        return create_response("Success - Set item.")

    # noinspection PyMethodMayBeStatic
    def delete_item(self, key: int) -> ResponseDTO:
        # LRU Cache에서 delete
        CACHE.delete_item(key)

        # Local File에서 delete
        success_in_local = FileCRUD().delete_item(key)

        # S3 Storage에서 delete
        success_in_s3 = S3Storage().delete_item(key)

        # 어느 store에서든 key가 존재하여 delete가 성공한 경우
        if success_in_local or success_in_s3:
            return create_response("Success - Delete item.")

        # 모든 store에 key가 존재하지 않아 delete를 실패한 경우
        raise HTTPException(status_code=404, detail="해당 key가 존재하지 않아 value를 삭제할 수 없습니다.")

    # noinspection PyMethodMayBeStatic
    def delete_all_items(self) -> ResponseDTO:
        CACHE.delete_all_items()
        return create_response("Success - Delete all items.")
