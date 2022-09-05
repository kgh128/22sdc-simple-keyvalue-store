import logging
from botocore.exceptions import ClientError

from app.config.s3Storage import s3_connection
from app.utils.fileUtils import get_path


class S3Storage:
    def __init__(self):
        self.s3 = s3_connection()
        self.bucket = 'simple-key-value-store'

    def download_item(self, key):
        object_name = get_path(key)
        file_path = f'database/{object_name}'

        try:
            self.s3.download_file(self.bucket, object_name, file_path)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def upload_item(self, item):
        object_name = get_path(item)
        file_path = f'database/{object_name}'

        try:
            self.s3.upload_file(file_path, self.bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True
