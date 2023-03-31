from rest_framework import serializers
from .models import S3File


class S3FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = S3File
        fields = [
            "nombre_archivo",
            "size",
            "s3_object_id",
            "s3_path",
            "s3_bucket_name",
        ]
