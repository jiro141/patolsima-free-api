from .paciente import Paciente
from .estudio import Estudio
from .medico_tratante import MedicoTratante
from .muestra import Muestra
from .patologo import Patologo
from .fase_muestra import FaseMuestra
from .informe import Informe, ResultadoInmunostoquimica

__all__ = [
    "Paciente",
    "Estudio",
    "MedicoTratante",
    "Muestra",
    "FaseMuestra",
    "Patologo",
    "Informe",
    "ResultadoInmunostoquimica",
]
