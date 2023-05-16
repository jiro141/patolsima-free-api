from .paciente import *
from .patologo import *
from .medico_tratante import *
from .estudio import *
from .muestra import *
from .fase_muestra import *
from .informe import *

__all__ = [
    PacienteSerializer,
    PacienteListSerializer,
    PatologoSerializer,
    PatologoListSerializer,
    MedicoTratanteListSerializer,
    MedicoTratanteSerializer,
    EstudioSerializer,
    EstudioListSerializer,
    EstudioCreateSerializer,
    EstudioUpdateSerializer,
    ArchivoAdjuntoEstudio,
    MuestraSerializer,
    MuestraListSerializer,
    FaseMuestraSerializer,
    InformeSerializer,
    InformeListSerializer,
    ResultadoInmunostoquimica,
]
