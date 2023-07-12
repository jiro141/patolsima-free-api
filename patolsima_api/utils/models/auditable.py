from django.db import models
from django.db import transaction
from django.db import models

# from django.contrib.auth.models import User
from softdelete.models import SoftDeleteObject

from patolsima_api.utils.admin import date_to_admin_readable


class AuditableMixin(SoftDeleteObject, models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    # created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)

    updated_at = models.DateTimeField(auto_now=True)
    # updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)

    class Meta:
        abstract = True

    @property
    def created_at_human_readable(self):
        return date_to_admin_readable(self.created_at)

    @property
    def updated_at_human_readable(self):
        return date_to_admin_readable(self.updated_at)

    @property
    def deleted_at_human_readable(self):
        return date_to_admin_readable(self.deleted_at)


class ArchivableMixing(models.Model):
    archived = models.BooleanField(default=False)

    class Meta:
        abstract = True

    @transaction.atomic
    def archive(self, save_=True):
        """
        Sets archived=True and saves
        :return: If successful then the instance will be archived after this step
        """
        if self.archived:
            return

        self.archived = True
        if save_:
            self.save()
