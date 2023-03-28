from .paciente import PacienteViewSet
from .estudio import EstudioViewSet
from .muestra import MuestraViewSet
from .patologo import PatologoViewSet
from .medico_tratante import MedicoTratanteViewSet

__all__ = [
    PacienteViewSet,
    EstudioViewSet,
    MuestraViewSet,
    PatologoViewSet,
    MedicoTratanteViewSet,
]
