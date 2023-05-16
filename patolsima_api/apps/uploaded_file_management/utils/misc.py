import hashlib
import uuid
from patolsima_api.apps.uploaded_file_management.models import UploadedFile


def generate_file_key(file_obj: UploadedFile, path_prefix: str):
    not_prefixed_key = f"{hashlib.md5(uuid.UUID(file_obj.uuid).bytes).hexdigest()}.{file_obj.file_extension}"
    return f"{path_prefix}/{not_prefixed_key}" if path_prefix else not_prefixed_key
