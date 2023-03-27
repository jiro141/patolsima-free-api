from django.db import models
from datetime import date
from simple_history.models import HistoricalRecords
from patolsima_api.utils.models import NombreMixin, AuditableMixin
from patolsima_api.apps.s3_management.models import S3File


class Patologo(AuditableMixin, NombreMixin):
    ncomed = models.CharField(max_length=32, unique=True, null=True, blank=True)
    firma = models.ForeignKey(S3File, on_delete=models.DO_NOTHING, null=True)

    history = HistoricalRecords()
