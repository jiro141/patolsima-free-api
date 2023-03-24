from rest_framework import routers

from patolsima_api.apps.core.views import PacienteViewSet

router = routers.DefaultRouter()
router.register(r"pacientes", PacienteViewSet, basename="paciente")
urlpatterns = router.urls
print(urlpatterns)
