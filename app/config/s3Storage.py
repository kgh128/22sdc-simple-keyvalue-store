import boto3
import os
from dotenv import load_dotenv


def s3_connection():
    load_dotenv()

    try:
        s3 = boto3.client(
            service_name="s3",
            region_name=os.environ.get("S3_REGION_NAME"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        )
    except Exception as e:
        print(e)
    else:
        print("s3 bucket connected!")
        return s3
