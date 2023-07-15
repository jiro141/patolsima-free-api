import uuid
from datetime import datetime
from django.shortcuts import render
from django.utils.timezone import make_aware
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError, NotFound
from patolsima_api.apps.uploaded_file_management.models import UploadedFile
from patolsima_api.apps.uploaded_file_management.utils.storage_adapters import (
    get_uri_from_storage_adapter,
)
from patolsima_api.utils.uuid import is_valid_uuid


class RedirectToResource(APIView):
    permission_classes = [
        AllowAny,
    ]

    def get(self, request, format=None, **kwargs):
        file_uuid = kwargs["file_uuid"]
        if not (isinstance(file_uuid, str) and is_valid_uuid(file_uuid)):
            raise ValidationError("Wrong value for file identificator")

        file = UploadedFile.objects.filter(uuid=file_uuid).first()
        if not file:
            return NotFound("File not found")
        resource_presigned_url = get_uri_from_storage_adapter(file)
        file.last_time_requested = make_aware(datetime.now())
        file.save()
        return HttpResponseRedirect(redirect_to=resource_presigned_url)
