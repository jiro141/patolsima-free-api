from rest_framework import serializers
from .models import UploadedFile


class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = [
            "nombre_archivo",
            "size",
            "s3_object_id",
            "s3_path",
            "s3_bucket_name",
        ]
