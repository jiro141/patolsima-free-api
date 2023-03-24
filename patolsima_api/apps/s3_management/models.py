from django.db import models

# Create your models here.


class S3File(models.Model):
    nombre_archivo = models.CharField(max_length=512)
    size = models.IntegerField()  # bytes
    s3_object_id = models.CharField(max_length=256)
    s3_path = models.CharField(max_length=512)
    s3_bucket_name = models.CharField(max_length=256)
