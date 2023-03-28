from .paciente import *
from .patologo import *
from .medico_tratante import *
from .estudio import *
from .muestra import *

__all__ = [
    PacienteSerializer,
    PacienteListSerializer,
    PatologoSerializer,
    PatologoListSerializer,
    MedicoTratanteListSerializer,
    MedicoTratanteSerializer,
    EstudioSerializer,
    EstudioListSerializer,
    MuestraSerializer,
]
