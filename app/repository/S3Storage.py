import logging
from botocore.exceptions import ClientError

from app.config.s3Storage import s3_connection
from app.schemas.item import Item
from app.utils.fileUtils import get_path


class S3Storage:
    def __init__(self):
        self.s3 = s3_connection()
        self.bucket = 'simple-key-value-store'

    def download_item(self, key: int) -> bool:
        object_name = get_path(key)
        file_path = f'database/{object_name}'

        try:
            self.s3.download_file(self.bucket, object_name, file_path)
            return True

        except ClientError as e:
            logging.error(e)
            return False

    def upload_item(self, item: Item) -> bool:
        object_name = get_path(item)
        file_path = f'database/{object_name}'

        try:
            self.s3.upload_file(file_path, self.bucket, object_name)
            return True

        except ClientError as e:
            logging.error(e)
            return False

    def delete_item(self, key: int) -> bool:
        object_name = get_path(key)

        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket, Prefix=object_name, MaxKeys=1)
            if 'Contents' in response:
                self.s3.delete_object(Bucket=self.bucket, Key=object_name)
                return True
            return False

        except ClientError as e:
            logging.error(e)
            return False
