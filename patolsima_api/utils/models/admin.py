from django.contrib import admin
from patolsima_api.utils.admin import date_to_admin_readable
from .auditable import AuditableMixin


class AuditableAdmin(admin.ModelAdmin):
    @admin.display(ordering="created_at", description="Creado el")
    def created_at_formatted(self, obj: AuditableMixin):
        return date_to_admin_readable(obj.created_at)

    @admin.display(ordering="updated_at", description="Actualizado el")
    def updated_at_formatted(self, obj: AuditableMixin):
        return date_to_admin_readable(obj.updated_at)
