from datetime import datetime, date
from random import randint
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


def create_paciente(
    ci=None,
    nombres="paciente",
    apellidos="apellidos paciente",
    fecha_nacimiento=date(1990, 1, 1),
    **kwargs
):
    if not ci:
        ci = randint(1, 40000000)
    return Paciente.objects.create(
        ci=str(ci),
        nombres=nombres,
        apellidos=apellidos,
        fecha_nacimiento=fecha_nacimiento,
        **kwargs
    )


def create_patologo(nombres="patologo", apellidos="apellidos patologo", ncomed=None):
    if not ncomed:
        ncomed = str(randint(1000, 10000))
    return Patologo.objects.create(
        nombres=nombres,
        apellidos=apellidos,
        ncomed=ncomed,
    )


def create_medico_tratante(
    ci=None,
    nombres="medico",
    apellidos="apellidos medico",
    ncomed=None,
    especialidad="mondacologia",
):
    if not ncomed:
        ncomed = str(randint(1000, 10000))
    if not ci:
        ci = randint(1000000, 30000000)
    return MedicoTratante.objects.create(
        ci=str(ci),
        nombres=nombres,
        apellidos=apellidos,
        ncomed=ncomed,
        especialidad=especialidad,
    )


def create_estudio(
    paciente=None, medico=None, patologo=None, tipo_estudio=None, **kwargs
):
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
        **kwargs
    )


def create_muestra(
    estudio,
    tipo_de_muestra="carne de vaca",
    descripcion="carne de lomo",
    notas="huele como piche",
    **kwargs
):
    return Muestra.objects.create(
        estudio=estudio,
        tipo_de_muestra=tipo_de_muestra,
        descripcion=descripcion,
        notas=notas,
        **kwargs
    )


def add_fase_muestra(muestra, estado, descripcion):
    pass
