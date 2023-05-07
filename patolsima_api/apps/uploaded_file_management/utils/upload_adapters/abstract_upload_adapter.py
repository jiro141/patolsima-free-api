import abc
from patolsima_api.apps.uploaded_file_management.models import UploadedFile


class AbstractUploadAdapter(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def upload_file(self):
        pass
