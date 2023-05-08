from typing import BinaryIO
import boto3

from .abstract_storage_adapter import AbstractStorageUnitAdapter


class S3StorageAdapter(AbstractStorageUnitAdapter):
    def __init__(self):
        super().__init__()
        self.s3_client = boto3.client("s3")

    def upload_file(self, file: BinaryIO, bucket: str, object_key: str):
        self.s3_client.upload_fileobj(file, bucket, object_key)  # Add extra args later

    def get_file(self, bucket: str, object_key: str) -> BinaryIO:
        return self.s3_client.get_object(Bucket=bucket, Key=object_key)["Body"]
