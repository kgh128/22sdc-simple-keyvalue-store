import os

from app.config.s3Storage import s3_connection


class KeyList:
    key_list: dict[int, str]

    def __init__(self):
        self.key_list = dict()

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

    def get_location(self, key: int) -> str:
        return self.key_list[key]

    def set_location(self, key: int, location: str) -> None:
        self.key_list[key] = location
