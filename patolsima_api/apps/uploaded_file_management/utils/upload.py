import os
import contextlib
from django.db import transaction
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from patolsima_api.apps.uploaded_file_management.models import UploadedFile
from patolsima_api.apps.uploaded_file_management.utils.storage_adapters import (
    get_default_storage_adapter,
)
from patolsima_api.apps.uploaded_file_management.utils.misc import generate_file_key


def upload_from_local_filesystem(
    file_path: str,
    bucket: str = settings.S3_DEFAULT_BUCKET,
    path_prefix: str = "",
    content_type: str = None,
    delete_original_after_upload: bool = False,
) -> UploadedFile:
    if not os.path.isfile(file_path):
        raise ValueError("Path entered must be a file")

    storage_adapter = get_default_storage_adapter()
    with transaction.atomic():
        new_file = UploadedFile.objects.create(
            local_filepath=file_path,
            file_name=file_path.split("/")[-1],
            storage_unit=storage_adapter.storage_unit_identifier,
            size=os.path.getsize(file_path),
            content_type=content_type,
        )
        new_file.object_key = generate_file_key(new_file, path_prefix=path_prefix)
        new_file.bucket_name = bucket
        new_file.save()
        with open(file_path, "rb") as binary_file:
            storage_adapter.upload_file(
                binary_file,
                bucket=bucket,
                object_key=new_file.object_key,
                extra_args={},
            )

    if delete_original_after_upload:
        with contextlib.suppress(IOError, OSError):
            os.remove(file_path)

    return new_file


def upload_from_request(
    file_from_request: InMemoryUploadedFile,
    bucket: str = settings.S3_DEFAULT_BUCKET,
    path_prefix: str = "",
):
    storage_adapter = get_default_storage_adapter()
    with transaction.atomic():
        new_file = UploadedFile.objects.create(
            file_name=file_from_request.name,
            size=file_from_request.size,
            content_type=file_from_request.content_type,
            storage_unit=storage_adapter.storage_unit_identifier,
        )
        new_file.object_key = generate_file_key(new_file, path_prefix=path_prefix)
        new_file.bucket_name = bucket
        new_file.save()
        storage_adapter.upload_file(
            file_from_request.file,
            bucket=bucket,
            object_key=new_file.object_key,
            extra_args={},
        )
    return new_file
