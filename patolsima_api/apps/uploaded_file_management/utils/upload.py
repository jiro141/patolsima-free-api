from django.db import transaction
from django.conf import settings
from patolsima_api.apps.uploaded_file_management.models import UploadedFile
from patolsima_api.apps.uploaded_file_management.utils.storage_adapters import (
    get_default_storage_adapter,
)
from patolsima_api.apps.uploaded_file_management.utils.misc import generate_file_key


def upload_from_local_filesystem(
    file_path: str, bucket: str = settings.S3_DEFAULT_BUCKET, path_prefix: str = ""
) -> UploadedFile:
    storage_adapter = get_default_storage_adapter()
    with transaction.atomic():
        new_file = UploadedFile.objects.create(
            local_filepath=file_path,
            file_name=file_path.split("/")[-1],
            storage_unit=storage_adapter.storage_unit_identifier,
            size=0,
        )
        new_file.object_key = generate_file_key(new_file, path_prefix=path_prefix)
        new_file.bucket_name = bucket
        new_file.save()
        with open(file_path, "rb") as binary_file:
            storage_adapter.upload_file(binary_file, bucket, new_file.object_key)

    return new_file
