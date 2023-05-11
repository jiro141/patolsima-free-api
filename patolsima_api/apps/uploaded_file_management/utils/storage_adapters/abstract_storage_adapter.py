import abc
from typing import Iterable, BinaryIO, Dict, Any
from patolsima_api.apps.uploaded_file_management.models import UploadedFile


class AbstractStorageUnitAdapter(abc.ABC):
    """
    This class acts as an interface that you can use to implement upload/download of files from different storage
    providers (local, S3, DigitalOcean, etc.)
    """

    storage_unit_identifier = None

    def __init__(self):
        pass

    @abc.abstractmethod
    def upload_file(
        self,
        file: BinaryIO,
        bucket: str,
        object_key: str,
        extra_args: Dict[str, Any] = None,
    ):
        """
        Saves the incoming file into the storage unit defined by each concrete class.
        :param file: Stream of bytes that implements the read() method at least.
        :param bucket: storage space or directory where the file is going to be saved
        :param object_key: new name for the object once's saved. It can contain only unscapped / chars.
        :param extra_args: some storage services (S3) allow to include extra searchable args to a file (tags, metadata, etc.)
        :return:
        """

    @abc.abstractmethod
    def get_file(self, bucket: str, object_key: str) -> BinaryIO:
        """
        Returns a binary stream that represents the file.
        :param bucket: storage space or directory where the file is saved
        :param object_key: name of the saved object
        :return: Returns a file-like object that you need to close afterwards using object.close() method.
        """

    @abc.abstractmethod
    def delete_file(self, bucket: str, object_key: str):
        """
        Deletes the file into the concrete storage unit.
        :param bucket:
        :param object_key:
        :return:
        """

    @classmethod
    def get_uri_for_file(cls, file: UploadedFile):
        raise NotImplementedError()
