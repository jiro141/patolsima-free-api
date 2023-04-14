from rest_framework import routers

from patolsima_api.apps.core.views import (
    PacienteViewSet,
    MedicoTratanteViewSet,
    PatologoViewSet,
    EstudioViewSet,
    MuestraViewSet,
    FaseMuestraViewSet,
    InformeViewSet,
    InformeGeneradoViewSet,
    ResultadoInmunostoquimicaViewSet,
)

router = routers.DefaultRouter()
router.register(r"pacientes", PacienteViewSet, basename="paciente")
router.register(r"medicos", MedicoTratanteViewSet, basename="medico")
router.register(r"patologos", PatologoViewSet, basename="patologo")
router.register(r"estudios", EstudioViewSet, basename="estudio")
router.register(r"muestras", MuestraViewSet, basename="muestra")
router.register(r"fasesmuestra", FaseMuestraViewSet, basename="fase-muestra")
router.register(r"informe", InformeViewSet, basename="informe")
router.register(
    r"informes-generado", InformeGeneradoViewSet, basename="informe-generado"
)
router.register(
    r"resultado-inmunostoquimica",
    ResultadoInmunostoquimicaViewSet,
    basename="resultados-inmunostoquimica",
)
urlpatterns = router.urls
# print(urlpatterns)
