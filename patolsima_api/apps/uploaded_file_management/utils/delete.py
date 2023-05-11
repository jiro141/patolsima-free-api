from django.db import transaction
from patolsima_api.apps.uploaded_file_management.models import UploadedFile
from patolsima_api.apps.uploaded_file_management.utils.storage_adapters import (
    get_default_storage_adapter,
)


@transaction.atomic
def delete_file_from_storage(instance: UploadedFile):
    storage_adapter = get_default_storage_adapter()
    storage_adapter.delete_file(instance.bucket_name, instance.object_key)
    instance.delete()
