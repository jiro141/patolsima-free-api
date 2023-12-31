from uuid import uuid4
from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords
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
    extra = models.JSONField(blank=True, null=True)

    last_time_requested = models.DateTimeField(null=True, blank=True)
    history = HistoricalRecords()

    @property
    def file_extension(self) -> str:
        return self.file_name.split(".")[-1]

    @property
    def uri(self) -> str:
        return f"{settings.API_HOST}/v1/filesmanagement/file/{self.uuid}/"

    def __str__(self) -> str:
        return self.file_name
