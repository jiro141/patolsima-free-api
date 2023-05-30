from django.conf import settings
from patolsima_api.apps.uploaded_file_management.models import UploadedFile
from .local_filesystem import LocalFileSystemStorageAdapter
from .aws_s3 import S3StorageAdapter


def get_default_storage_adapter():
    if not (settings.AWS_ACCESS_KEY and settings.AWS_SECRET_KEY):
        return LocalFileSystemStorageAdapter()

    return S3StorageAdapter()


def get_uri_from_storage_adapter(file: UploadedFile):
    if file.storage_unit == UploadedFile.StorageUnit.LOCAL_STORAGE:
        return LocalFileSystemStorageAdapter.get_uri_for_file(file)

    return S3StorageAdapter.get_uri_for_file(file)


__all__ = [get_default_storage_adapter, get_uri_from_storage_adapter]
