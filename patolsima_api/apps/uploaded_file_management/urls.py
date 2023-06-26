from django.urls import path, include
from patolsima_api.apps.uploaded_file_management.views import RedirectToResource

urlpatterns = [
    path(
        "file/<file_uuid>/",
        RedirectToResource.as_view(),
        name="redirect-to-file",
    ),
]
