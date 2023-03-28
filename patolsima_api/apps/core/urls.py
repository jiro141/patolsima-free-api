from rest_framework import routers

from patolsima_api.apps.core.views import (
    PacienteViewSet,
    MedicoTratanteViewSet,
    PatologoViewSet,
    EstudioViewSet,
    MuestraViewSet,
)

router = routers.DefaultRouter()
router.register(r"pacientes", PacienteViewSet, basename="paciente")
router.register(r"medicos", MedicoTratanteViewSet, basename="medico")
router.register(r"patologos", PatologoViewSet, basename="patologo")
router.register(r"estudios", EstudioViewSet, basename="estudio")
router.register(r"muestras", MuestraViewSet, basename="muestra")
urlpatterns = router.urls
print(urlpatterns)
