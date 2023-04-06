from functools import reduce
from random import randint
from datetime import datetime, date
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.urls import include, path, reverse
from rest_framework.test import APIClient, APITestCase
from patolsima_api.apps.core.models import Muestra, Estudio
from .mocks import create_estudio, create_muestra, authenticate


# Create your tests here.
class MuestraTests(APITestCase):
    def setUp(self) -> None:
        self.estudio = create_estudio()
        self.muestra = create_muestra(self.estudio)
        self.user, self.token = authenticate(self.client)

    def test_get_muestra(self):
        self.client.credentials()  # Clears credentials / Removes authentication HTTP headers

        url = reverse("muestra-detail", args=[self.muestra.id])
        r = self.client.get(url)
        self.assertEqual(
            r.status_code,
            403,
            "This request must be invalidated because the user is not logged in.",
        )

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        assert data["estudio"] == self.estudio.id

    def test_post_muestra(self):
        count_muestras = Muestra.objects.count()
        count_muestras_estudio = self.estudio.muestras.count()

        self.client.credentials()  # Clears credentials / Removes authentication HTTP headers
        creation_data = {
            "estudio": self.estudio.id,
            "tipo_de_muestra": "Rodaja de nalga Postman",
            "descripcion": "coloracion rosada",
            "notas": "no han pagado kueg de 1 mes",
        }
        url = reverse("muestra-list")
        r = self.client.post(url, creation_data)
        self.assertEqual(
            r.status_code,
            403,
            "This request must be invalidated because the user is not logged in.",
        )

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        r = self.client.post(url, creation_data)
        self.assertEqual(r.status_code, 201, "Muestra must be created")
        data = r.json()
        self.assertEqual(Muestra.objects.count(), (count_muestras + 1))
        self.assertEqual(self.estudio.muestras.count(), (count_muestras_estudio + 1))
        match data:
            case {
                "estudio": estudio,
                "tipo_de_muestra": tipo_de_muestra,
                "descripcion": descripcion,
                "notas": notas,
                "estado": estado,
            }:
                assert estudio == creation_data["estudio"]
                assert tipo_de_muestra == creation_data["tipo_de_muestra"]
                assert descripcion == creation_data["descripcion"]
                assert notas == creation_data["notas"]
                assert estado == Muestra.Estados.RECIBIDA
            case _:
                assert False, "Missing fields in payload"

    def test_update_muestra(self):
        self.client.credentials()  # Clears credentials / Removes authentication HTTP headers

        update_data = {
            "id": self.muestra.id,
            "estudio": self.muestra.estudio_id,
            "tipo_de_muestra": "nuevotipo",
            "estado": Muestra.Estados.ALMACENAMIENTO,
        }
        old_tm = self.muestra.tipo_de_muestra
        assert Muestra.objects.count() == 1  # Only our testing record in DB

        url = reverse("muestra-detail", args=[self.muestra.id])
        r = self.client.put(url, update_data)
        self.assertEqual(
            r.status_code,
            403,
            "This request must be invalidated because the user is not logged in.",
        )

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        r = self.client.put(url, update_data)
        print(r.data)
        self.assertEqual(r.status_code, 200)
        assert Muestra.objects.count() == 1  # Only our testing record in DB
        data = r.json()

        match data:
            case {
                "id": id,
                "estudio": estudio,
                "tipo_de_muestra": tipo_de_muestra,
                "descripcion": descripcion,
                "notas": notas,
                "estado": estado,
            }:
                assert id == self.muestra.id
                assert estudio == self.muestra.estudio.id
                assert tipo_de_muestra != self.muestra.tipo_de_muestra
                assert tipo_de_muestra == update_data["tipo_de_muestra"]
                assert descripcion == self.muestra.descripcion
                assert notas == self.muestra.notas
                assert estado == Muestra.Estados.ALMACENAMIENTO
            case _:
                assert False, "Missing fields in payload"

        instance = Muestra.objects.first()
        assert instance.tipo_de_muestra != old_tm
        assert instance.tipo_de_muestra == update_data["tipo_de_muestra"]
        assert instance.estado == Muestra.Estados.ALMACENAMIENTO

    def test_delete_muestra(self):
        self.client.credentials()  # Clears credentials / Removes authentication HTTP headers
        self.assertEqual(Muestra.objects.count(), 1)
        url = reverse("muestra-detail", args=[self.muestra.id])
        r = self.client.delete(url)
        self.assertEqual(
            r.status_code,
            403,
            "This request must be invalidated because the user is not logged in.",
        )
        self.assertEqual(Muestra.objects.count(), 1)  # Not deleted
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        r = self.client.delete(url)
        self.assertEqual(r.status_code, 204)  # 204 No Content is ok in this case
        self.assertEqual(Muestra.objects.count(), 0)  # Successfuly deleted

    def test_get_list_muestra(self):
        self.client.credentials()  # Clears credentials / Removes authentication HTTP headers

        url = reverse("muestra-list")
        r = self.client.get(url)
        self.assertEqual(
            r.status_code,
            403,
            "This request must be invalidated because the user is not logged in.",
        )

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        assert data["count"] == 1
        assert len(data["results"]) == 1
        assert all(
            map(
                lambda x: x in data["results"][0],
                [
                    "id",
                    "estudio",
                    "tipo_de_muestra",
                    "descripcion",
                    "notas",
                ],
            )
        )
