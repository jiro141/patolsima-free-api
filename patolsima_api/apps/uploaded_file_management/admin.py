from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from patolsima_api.utils.admin import date_to_admin_readable
from patolsima_api.apps.uploaded_file_management.models import UploadedFile


class UploadedFileAdmin(SimpleHistoryAdmin):
    list_display = (
        "uuid",
        "file_name",
        "size",
        "content_type",
        "storage_unit",
        "last_time_requested_hr",
    )
    search_fields = ("uuid", "file_name")
    list_filter = (
        "storage_unit",
        "bucket_name",
        "created_at",
        "updated_at",
        "content_type",
    )

    @admin.display(ordering="last_time_requested", description="Last Time Requested")
    def last_time_requested_hr(self, obj: UploadedFile):
        return date_to_admin_readable(obj.last_time_requested)


admin.site.register(UploadedFile, UploadedFileAdmin)
