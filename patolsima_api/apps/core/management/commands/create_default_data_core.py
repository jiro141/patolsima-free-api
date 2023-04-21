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
        paciente1, paciente1_created = Paciente.objects.get_or_create(
            ci=1,
            defaults={
                "nombres": "paciente1",
                "apellidos": "apellido1",
                "fecha_nacimiento": date(1990, 1, 10),
                "email": "asd@asd.asd",
                "telefono_celular": "+581231234567",
            },
        )

        paciente2, paciente2_created = Paciente.objects.get_or_create(
            ci=2,
            defaults={
                "nombres": "paciente2",
                "apellidos": "apellido2",
                "fecha_nacimiento": date(1990, 1, 10),
                "email": "asd@asd.asd",
                "telefono_celular": "+581231234567",
            },
        )

        medico1, medico1_created = MedicoTratante.objects.get_or_create(
            ci=3,
            ncomed="kajshdg",
            defaults={
                "especialidad": "neurocirugia",
                "nombres": "medico1",
                "apellidos": "medicox",
                "email": "medico@medicoso.com",
                "telefono_celular": "+585555555555",
            },
        )

        patologo1, patologo1_created = Patologo.objects.get_or_create(
            ncomed="15263",
            defaults={
                "nombres": "Patologo",
                "apellidos": "Patolosico",
            },
        )

        estudio1, estudio1_created = Estudio.objects.get_or_create(
            paciente=paciente1,
            medico_tratante=medico1,
            patologo=patologo1,
            notas="El paciente jode mucho",
            urgente=False,
            tipo=Estudio.TipoEstudio.BIOPSIA,
        )

        estudio2, estudio2_created = Estudio.objects.get_or_create(
            paciente=paciente2,
            medico_tratante=medico1,
            patologo=patologo1,
            notas="El paciente jode mucho 2",
            envio_digital=True,
            urgente=True,
            tipo=Estudio.TipoEstudio.CITOLOGIA_ESPECIAL,
        )

        muestra1, muestra1_created = Muestra.objects.get_or_create(
            estudio=estudio1,
            tipo_de_muestra="Rodaja de nalga",
            defaults={
                "descripcion": "coloracion rosada",
                "notas": "no han pagado",
            },
        )

        muestra2, muestra2_created = Muestra.objects.get_or_create(
            estudio=estudio2,
            tipo_de_muestra="barro de la cara",
            defaults={
                "descripcion": "coloracion amarillenta",
                "notas": "no han pagado",
            },
        )

        muestra3, muestra3_created = Muestra.objects.get_or_create(
            estudio=estudio2,
            tipo_de_muestra="barro del cuello",
            defaults={
                "descripcion": "coloracion amarillenta",
                "notas": "no han pagado",
            },
        )

        # Para arreglar esto hay que crear una serie que cuente todos los a;os por tipo de estudio.
