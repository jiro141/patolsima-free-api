from typing import BinaryIO, Dict, Any
import boto3
from django.conf import settings
from patolsima_api.apps.uploaded_file_management.models import UploadedFile
from .abstract_storage_adapter import (
    AbstractStorageUnitAdapter,
    SingletonForStorageAdapter,
)


class S3StorageAdapter(
    AbstractStorageUnitAdapter, metaclass=SingletonForStorageAdapter
):
    storage_unit_identifier = UploadedFile.StorageUnit.AWS_S3

    def __init__(self):
        super().__init__()
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY,
        )

    def _check_bucket(self, bucket_name: str):
        if bucket_name not in settings.S3_BUCKETS:
            raise ValueError(f"Bucket {bucket_name} not in allowed buckets list.")

    def upload_file(
        self,
        file: BinaryIO,
        bucket: str,
        object_key: str,
        extra_args: Dict[str, Any] = None,
    ):
        if not extra_args:
            extra_args = dict()

        self._check_bucket(bucket)
        response = self.s3_client.upload_fileobj(
            Fileobj=file, Bucket=bucket, Key=object_key, ExtraArgs=extra_args
        )  # Add extra args later
        print(response)

    def get_file(self, bucket: str, object_key: str) -> BinaryIO:
        self._check_bucket(bucket)
        s3_object = self.s3_client.get_object(Bucket=bucket, Key=object_key)
        print(s3_object)
        return s3_object["Body"]

    def delete_file(self, bucket: str, object_key: str):
        # Falta a;adir el caso en el que el archivo no existe en S3
        response = self.s3_client.delete_object(Bucket=bucket, Key=object_key)
        print(response)

    @classmethod
    def get_uri_for_file(cls, file: UploadedFile):
        return "Not URI"
