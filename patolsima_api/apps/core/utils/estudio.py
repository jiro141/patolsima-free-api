from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction
from rest_framework.exceptions import NotFound
from typing import Dict, Any

from patolsima_api.apps.core.models import Estudio
from patolsima_api.apps.uploaded_file_management.models import UploadedFile
from patolsima_api.apps.uploaded_file_management.serializers import (
    UploadedFileSerializer,
)
from patolsima_api.apps.uploaded_file_management.utils.upload import upload_from_request
from patolsima_api.apps.uploaded_file_management.utils.delete import (
    delete_file_from_storage,
)


@transaction.atomic
def append_new_adjunto(estudio: Estudio, file: InMemoryUploadedFile) -> Dict[str, Any]:
    uploaded_file = upload_from_request(
        file, path_prefix=f"estudios/{estudio.id}/adjuntos"
    )
    estudio.adjuntos.add(uploaded_file)
    return UploadedFileSerializer(uploaded_file).data


@transaction.atomic
def remove_adjunto(estudio: Estudio, adjunto_id: int):
    try:
        adjunto = estudio.adjuntos.get(id=adjunto_id)
    except UploadedFile.DoesNotExist:
        raise NotFound(f"Adjunto {adjunto_id} not found")

    estudio.adjuntos.remove(adjunto)
    delete_file_from_storage(adjunto)
