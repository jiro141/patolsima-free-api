import pytz
from datetime import datetime
from typing import BinaryIO, Dict, Any
import boto3
from django.conf import settings
from patolsima_api.apps.uploaded_file_management.models import UploadedFile
from .abstract_storage_adapter import (
    AbstractStorageUnitAdapter,
    SingletonForStorageAdapter,
)


class S3StorageAdapter(
    AbstractStorageUnitAdapter, metaclass=SingletonForStorageAdapter
):
    storage_unit_identifier = UploadedFile.StorageUnit.AWS_S3

    def __init__(self):
        super().__init__()
        self.session = None
        self.s3_client = None
        self.session_expiration = None
        self._get_s3_client()

    def _get_s3_client(self):
        if not self.session:
            self.session = boto3.Session(
                aws_access_key_id=settings.AWS_ACCESS_KEY,
                aws_secret_access_key=settings.AWS_SECRET_KEY,
            )

        sts = self.session.client("sts")
        role_response = sts.assume_role(
            RoleArn="arn:aws:iam::735019439051:role/PatolsimaAdmin",
            RoleSessionName="patolsima-s3-session",
        )
        self.session_expiration = role_response["Credentials"]["Expiration"]
        session_as_patolsima = boto3.Session(
            aws_access_key_id=role_response["Credentials"]["AccessKeyId"],
            aws_secret_access_key=role_response["Credentials"]["SecretAccessKey"],
            aws_session_token=role_response["Credentials"]["SessionToken"],
        )

        self.s3_client = session_as_patolsima.client("s3")

    def _check_session_expiration(self):
        if (
            self.session_expiration
            and pytz.utc.localize(datetime.now()) < self.session_expiration
        ):
            return

        self._get_s3_client()

    def _check_bucket(self, bucket_name: str):
        if bucket_name not in settings.S3_BUCKETS:
            raise ValueError(f"Bucket {bucket_name} not in allowed buckets list.")

    def upload_file(
        self,
        file: BinaryIO,
        bucket: str,
        object_key: str,
        extra_args: Dict[str, Any] = None,
    ):
        self._check_session_expiration()
        self._check_bucket(bucket)
        if not extra_args:
            extra_args = dict()

        response = self.s3_client.upload_fileobj(
            Fileobj=file, Bucket=bucket, Key=object_key, ExtraArgs=extra_args
        )  # Add extra args later

    def get_file(self, bucket: str, object_key: str) -> BinaryIO:
        self._check_session_expiration()
        self._check_bucket(bucket)
        s3_object = self.s3_client.get_object(Bucket=bucket, Key=object_key)
        print(s3_object)
        return s3_object["Body"]

    def delete_file(self, bucket: str, object_key: str):
        # Falta a;adir el caso en el que el archivo no existe en S3
        self._check_session_expiration()
        self._check_bucket(bucket)
        response = self.s3_client.delete_object(Bucket=bucket, Key=object_key)

    def get_uri_for_file(self, file: UploadedFile):
        self._check_session_expiration()
        return "Not URI"
