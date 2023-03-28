from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from datetime import date
from patolsima_api.apps.core.models import (
    Paciente,
    MedicoTratante,
    Estudio,
    Muestra,
    Patologo,
)


class Command(BaseCommand):
    help = "Genera la data por defecto para probar la API"

    def add_arguments(self, parser):
        pass

    @transaction.atomic
    def handle(self, *args, **options):
        paciente1 = Paciente.objects.create(
            ci=1,
            nombres="paciente1",
            apellidos="apellido1",
            fecha_nacimiento=date(1990, 1, 10),
            email="asd@asd.asd",
            telefono_celular="+581231234567",
        )

        paciente2 = Paciente.objects.create(
            ci=2,
            nombres="paciente2",
            apellidos="apellido2",
            fecha_nacimiento=date(1990, 1, 10),
            email="asd@asd.asd",
            telefono_celular="+581231234567",
        )

        medico1 = MedicoTratante.objects.create(
            ci=3,
            ncomed="kajshdg",
            especialidad="neurocirugia",
            nombres="medico1",
            apellidos="medicox",
            email="medico@medicoso.com",
            telefono_celular="+585555555555",
        )

        patologo1 = Patologo.objects.create(
            nombres="Patologo", apellidos="Patolosico", ncomed="15263"
        )

        estudio1 = Estudio.objects.create(
            paciente=paciente1,
            medico_tratante=medico1,
            patologo=patologo1,
            codigo="ashkgd",
            notas="El paciente jode mucho",
            prioridad=Estudio.Prioridad.MEDIA,
            tipo=Estudio.TipoEstudio.BIOPSIA,
        )

        estudio2 = Estudio.objects.create(
            paciente=paciente2,
            medico_tratante=medico1,
            patologo=patologo1,
            codigo="ashkgd2",
            notas="El paciente jode mucho 2",
            prioridad=Estudio.Prioridad.ALTA,
            tipo=Estudio.TipoEstudio.CITOLOGIA,
        )

        muestra1 = Muestra.objects.create(
            estudio=estudio1,
            tipo_de_muestra="Rodaja de nalga",
            descripcion="coloracion rosada",
            notas="no han pagado",
        )

        muestra2 = Muestra.objects.create(
            estudio=estudio2,
            tipo_de_muestra="barro de la cara",
            descripcion="coloracion amarillenta",
            notas="no han pagado",
        )

        muestra3 = Muestra.objects.create(
            estudio=estudio2,
            tipo_de_muestra="barro del cuello",
            descripcion="coloracion amarillenta",
            notas="no han pagado",
        )
