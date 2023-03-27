from django.core.management.base import BaseCommand, CommandError
from patolsima_api.apps.core.models import Paciente


class Command(BaseCommand):
    help = "Genera la data por defecto para probar la API"

    def add_arguments(self, parser):
        parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        pass
