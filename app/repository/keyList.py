import os

from app.config.s3Storage import s3_connection


class KeyList:
    key_list: dict[int, str] = dict()

    def __init__(self):
        s3 = s3_connection()
        paginator = s3.get_paginator('list_objects_v2')

        bucket = 'simple-key-value-store'
        response_iterator = paginator.paginate(Bucket=bucket)

        for page in response_iterator:
            for content in page['Contents']:
                if not content['Key'].endswith('/'):
                    file_name = os.path.split(content['Key'])[1]
                    key = int(os.path.splitext(file_name)[0])
                    self.key_list[key] = 'S3'

    def is_in_key_list(self, key: int) -> bool:
        if key in self.key_list:
            return True
        return False

    def get_all_keys(self) -> list[int]:
        return list(self.key_list.keys())

    def set_key(self, key: int, location: str) -> None:
        self.key_list[key] = location
        return None

    def delete_key(self, key: int) -> None:
        if key in self.key_list:
            del self.key_list[key]
        return None

    def get_location(self, key: int) -> str:
        return self.key_list[key]
