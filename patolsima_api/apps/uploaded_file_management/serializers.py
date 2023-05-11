from rest_framework import serializers
from .models import UploadedFile


class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = [
            "id",
            "uuid",
            "file_name",
            "local_filepath",
            "storage_unit",
            "size",
            "content_type",
        ]
