import os
from typing import BinaryIO, Dict, Any
from django.conf import settings
from .abstract_storage_adapter import AbstractStorageUnitAdapter
from patolsima_api.apps.uploaded_file_management.models import UploadedFile


class LocalFileSystemStorageAdapter(AbstractStorageUnitAdapter):
    storage_unit_identifier = UploadedFile.StorageUnit.LOCAL_STORAGE

    def upload_file(
        self,
        file: BinaryIO,
        bucket: str,
        object_key: str,
        extra_args: Dict[str, Any] = None,
    ):
        bucket_path = f"{settings.S3_LOCALE_PATH}/{bucket}"

        if not os.path.isdir(bucket_path):
            os.makedirs(bucket_path)

        if "/" in object_key and not os.path.isdir(
            sub_directory := f"{bucket_path}/{object_key.rsplit('/', maxsplit=1)[0]}"
        ):
            os.makedirs(sub_directory)

        with open(f"{bucket_path}/{object_key}", "wb") as destination_file:
            while bytes_ := file.read(settings.DEFAULT_BINARY_STREAMS_CHUNK_SIZE):
                destination_file.write(bytes_)

    def get_file(self, bucket: str, object_key: str) -> BinaryIO:
        object_path = f"{settings.S3_LOCALE_PATH}/{bucket}/{object_key}"
        return open(object_path, "rb")

    def delete_file(self, bucket: str, object_key: str):
        os.remove(f"{settings.S3_LOCALE_PATH}/{bucket}/{object_key}")
