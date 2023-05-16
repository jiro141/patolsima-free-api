from uuid import uuid4
from django.db import models
from patolsima_api.utils.models import AuditableMixin

# Create your models here.


def get_uuid_for_new_file() -> str:
    return str(uuid4())


class UploadedFile(AuditableMixin):
    class StorageUnit(models.TextChoices):
        AWS_S3 = "AWS_S3"
        LOCAL_STORAGE = "LOCAL_STORAGE"

    uuid = models.CharField(
        max_length=36, unique=True, db_index=True, default=get_uuid_for_new_file
    )
    file_name = models.CharField(max_length=512)
    local_filepath = models.CharField(max_length=512, null=True, blank=True)
    storage_unit = models.CharField(
        max_length=16, choices=StorageUnit.choices, default=StorageUnit.LOCAL_STORAGE
    )
    size = models.IntegerField()  # bytes
    content_type = models.CharField(max_length=64, null=True, blank=True)
    object_key = models.CharField(max_length=512, null=True, blank=True)
    bucket_name = models.CharField(max_length=256, null=True, blank=True)

    last_time_requested = models.DateTimeField(null=True, blank=True)

    @property
    def file_extension(self):
        return self.file_name.split(".")[-1]

    @property
    def uri(self):
        from patolsima_api.apps.uploaded_file_management.utils.storage_adapters import (
            get_uri_from_storage_adapter,
        )

        return get_uri_from_storage_adapter(self)
