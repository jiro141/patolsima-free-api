from datetime import datetime, date
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.urls import include, path, reverse
from rest_framework.test import APIClient, APITestCase
from patolsima_api.apps.core.models import MedicoTratante


# Create your tests here.
class MedicoTratanteTests(APITestCase):
    def setUp(self) -> None:
        self.medico_tratante = MedicoTratante.objects.create(
            ci=1,
            nombres="medico",
            apellidos="apellidos medico",
            ncomed="12635",
            especialidad="mondacologia",
        )
        self.UserModel = get_user_model()
        self.user = self.UserModel.objects.create(
            username="asd",
            email="asd@asd.asd",
            first_name="ASD",
            last_name="asd",
            password=make_password("asd"),
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )
        self.token = self.client.post(
            reverse("login"),
            {"username": self.user.username, "password": "asd"},
            format="json",
        ).json()["access"]

    def test_get_medico(self):
        self.client.credentials()  # Clears credentials / Removes authentication HTTP headers

        url = reverse("medico-detail", args=[self.medico_tratante.id])
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
        match data:
            case {
                "id": mid,
                "ncomed": ncomed,
                "ci": ci,
                "nombres": nombres,
                "apellidos": apellidos,
            }:
                assert ci == self.medico_tratante.ci
                assert nombres == self.medico_tratante.nombres
                assert apellidos == self.medico_tratante.apellidos
                assert mid == self.medico_tratante.id
                assert ncomed == self.medico_tratante.ncomed
            case _:
                assert False, "Missing fields in payload"

    def test_post_medico(self):
        count_medicos = MedicoTratante.objects.count()
        self.client.credentials()  # Clears credentials / Removes authentication HTTP headers
        creation_data = {
            "ncomed": self.medico_tratante.ncomed,
            "nombres": "medico test",
            "apellidos": "test apellidos",
            "especialidad": "mondacologia",
        }
        url = reverse("medico-list")

        r = self.client.post(url, creation_data)
        self.assertEqual(
            r.status_code,
            403,
            "This request must be invalidated because the user is not logged in.",
        )

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        r = self.client.post(url, creation_data)
        self.assertEqual(
            r.status_code,
            400,
            "The request must be rejected because the NCOMED already exists.",
        )

        creation_data["ncomed"] = "0000"
        r = self.client.post(url, creation_data)
        self.assertEqual(r.status_code, 201, "Medico created")
        data = r.json()
        assert MedicoTratante.objects.count() == (count_medicos + 1)
        match data:
            case {
                "ci": ci,
                "nombres": nombres,
                "apellidos": apellidos,
                "ncomed": ncomed,
            }:
                assert ci == None
                assert nombres == creation_data["nombres"]
                assert apellidos == creation_data["apellidos"]
                assert ncomed == creation_data["ncomed"]
            case _:
                assert False, "Missing fields in payload"

    def test_update_medico(self):
        self.client.credentials()  # Clears credentials / Removes authentication HTTP headers

        update_data = {
            "ci": 123,
            "nombres": "nuevonombre",
            "apellidos": self.medico_tratante.apellidos,
        }
        old_name = self.medico_tratante.nombres
        assert MedicoTratante.objects.count() == 1  # Only our testing record in DB

        url = reverse("medico-detail", args=[self.medico_tratante.id])
        r = self.client.put(url, update_data)
        self.assertEqual(
            r.status_code,
            403,
            "This request must be invalidated because the user is not logged in.",
        )

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        r = self.client.put(url, update_data)
        self.assertEqual(r.status_code, 200)
        assert MedicoTratante.objects.count() == 1  # Only our testing record in DB
        data = r.json()

        match data:
            case {
                "ci": ci,
                "nombres": nombres,
                "apellidos": apellidos,
                "ncomed": ncomed,
            }:
                self.assertEqual(ci, update_data["ci"])
                self.assertNotEqual(nombres, self.medico_tratante.nombres)
                self.assertEqual(nombres, update_data["nombres"])
                self.assertEqual(apellidos, self.medico_tratante.apellidos)
                self.assertEqual(ncomed, self.medico_tratante.ncomed)
            case _:
                assert False, "Missing fields in payload"

        instance = MedicoTratante.objects.first()
        assert instance.nombres != old_name
        assert instance.nombres == update_data["nombres"]
        assert instance.ci is not None

    def test_delete_medico(self):
        self.client.credentials()  # Clears credentials / Removes authentication HTTP headers
        assert MedicoTratante.objects.count() == 1
        url = reverse("medico-detail", args=[self.medico_tratante.id])
        r = self.client.delete(url)
        self.assertEqual(
            r.status_code,
            403,
            "This request must be invalidated because the user is not logged in.",
        )
        assert MedicoTratante.objects.count() == 1  # Not deleted
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        r = self.client.delete(url)
        self.assertEqual(r.status_code, 204)  # 204 No Content is ok in this case
        assert MedicoTratante.objects.count() == 0  # Successfuly deleted

    def test_get_list_medico(self):
        self.client.credentials()  # Clears credentials / Removes authentication HTTP headers

        url = reverse("medico-list")
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
                    "ncomed",
                    "nombres",
                    "apellidos",
                    "especialidad",
                ],
            )
        )
