from datetime import datetime, date
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.urls import include, path, reverse
from patolsima_api.apps.core.models import (
    Muestra,
    Estudio,
    Paciente,
    MedicoTratante,
    Patologo,
)


def authenticate(client):
    UserModel = get_user_model()
    user = UserModel.objects.create(
        username="asd",
        email="asd@asd.asd",
        first_name="ASD",
        last_name="asd",
        password=make_password("asd"),
        is_active=True,
        is_staff=True,
        is_superuser=True,
    )
    token = client.post(
        reverse("login"),
        {"username": user.username, "password": "asd"},
        format="json",
    ).json()["access"]

    return user, token


def create_paciente():
    return Paciente.objects.create(
        ci=1,
        nombres="paciente",
        apellidos="apellidos paciente",
        fecha_nacimiento=date(1990, 1, 1),
    )


def create_patologo():
    return Patologo.objects.create(
        nombres="patologo",
        apellidos="apellidos patologo",
        ncomed="12635",
    )


def create_medico_tratante():
    return MedicoTratante.objects.create(
        ci=1,
        nombres="medico",
        apellidos="apellidos medico",
        ncomed="12635",
        especialidad="mondacologia",
    )


def create_estudio(paciente=None, medico=None, patologo=None, tipo_estudio=None):
    if not paciente:
        paciente = create_paciente()

    if not medico:
        medico = create_medico_tratante()

    if not patologo:
        patologo = create_patologo()

    if not tipo_estudio:
        tipo_estudio = Estudio.TipoEstudio.BIOPSIA

    return Estudio.objects.create(
        paciente=paciente,
        medico_tratante=medico,
        patologo=patologo,
        notas="Este pedazo de carne esta picha",
        tipo=tipo_estudio,
    )


def create_muestra(estudio):
    return Muestra.objects.create(
        estudio=estudio,
        tipo_de_muestra="carne de vaca",
        descripcion="carne de lomo",
        notas="huele como piche",
    )
