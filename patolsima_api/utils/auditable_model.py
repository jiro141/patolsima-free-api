from django.db import models

from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from softdelete.models import SoftDeleteObject


class AuditableModel(SoftDeleteObject, models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)

    updated_at = models.DateTimeField(auto_now=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)

    history = HistoricalRecords()
