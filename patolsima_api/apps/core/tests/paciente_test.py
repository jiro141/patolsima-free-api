from datetime import datetime, date
from urllib.parse import urlencode
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.urls import include, path, reverse
from rest_framework.test import APIClient, APITestCase
from patolsima_api.apps.core.models import Paciente
from .mocks import create_paciente, authenticate


# Create your tests here.
class PacienteTests(APITestCase):
    def setUp(self) -> None:
        self.paciente = create_paciente()
        self.user, self.token = authenticate(self.client)

    def test_get_paciente(self):
        self.client.credentials()  # Clears credentials / Removes authentication HTTP headers

        url = reverse("paciente-detail", args=[self.paciente.id])
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
                "id": id,
                "ci": ci,
                "nombres": nombres,
                "apellidos": apellidos,
                "fecha_nacimiento": fecha_nacimiento,
            }:
                assert id == self.paciente.id
                assert ci == self.paciente.ci
                assert nombres == self.paciente.nombres
                assert apellidos == self.paciente.apellidos
                assert (
                    date.fromisoformat(fecha_nacimiento)
                    == self.paciente.fecha_nacimiento
                )
            case _:
                assert False, "Missing fields in payload"

    def test_post_paciente_fail_login(self):
        count_pacientes = Paciente.objects.count()
        self.client.credentials()  # Clears credentials / Removes authentication HTTP headers
        creation_data = {
            "ci": self.paciente.ci,
            "nombres": "test",
            "apellidos": "test apellidos",
            "fecha_nacimiento": "1995-01-01",
            "sexo": Paciente.Sexo.MASCULINO,
        }
        url = reverse("paciente-list")
        r = self.client.post(url, creation_data)
        self.assertEqual(
            r.status_code,
            403,
            "This request must be invalidated because the user is not logged in.",
        )

    def test_post_paciente_fail_creation_unique_contraint(self):
        count_pacientes = Paciente.objects.count()
        self.client.credentials()  # Clears credentials / Removes authentication HTTP headers
        creation_data = {
            "ci": self.paciente.ci,
            "nombres": "test",
            "apellidos": "test apellidos",
            "fecha_nacimiento": "1995-01-01",
            "sexo": Paciente.Sexo.MASCULINO,
        }
        url = reverse("paciente-list")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        r = self.client.post(url, creation_data)
        self.assertEqual(
            r.status_code,
            500,
            "The request must be rejected because the CI already exists.",
        )

    def test_post_paciente_success(self):
        count_pacientes = Paciente.objects.count()
        self.client.credentials()  # Clears credentials / Removes authentication HTTP headers
        creation_data = {
            "ci": str(int(self.paciente.ci) + 1),
            "nombres": "test",
            "apellidos": "test apellidos",
            "fecha_nacimiento": "1995-01-01",
            "sexo": Paciente.Sexo.MASCULINO,
        }
        url = reverse("paciente-list")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        r = self.client.post(url, creation_data)
        self.assertEqual(r.status_code, 201, "Paciente created")
        data = r.json()
        assert Paciente.objects.count() == (count_pacientes + 1)
        match data:
            case {
                "ci": ci,
                "nombres": nombres,
                "apellidos": apellidos,
                "fecha_nacimiento": fecha_nacimiento,
            }:
                assert ci == creation_data["ci"]
                assert nombres == creation_data["nombres"]
                assert apellidos == creation_data["apellidos"]
                assert fecha_nacimiento == creation_data["fecha_nacimiento"]
            case _:
                assert False, "Missing fields in payload"

    def test_update_paciente(self):
        self.client.credentials()  # Clears credentials / Removes authentication HTTP headers

        update_data = {
            "ci": self.paciente.ci,
            "nombres": "nuevonombre",
            "apellidos": self.paciente.apellidos,
        }
        old_name = self.paciente.nombres
        assert Paciente.objects.count() == 1  # Only our testing record in DB

        url = reverse("paciente-detail", args=[self.paciente.id])
        r = self.client.put(url, update_data)
        self.assertEqual(
            r.status_code,
            403,
            "This request must be invalidated because the user is not logged in.",
        )

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        r = self.client.put(url, update_data)
        self.assertEqual(r.status_code, 200)
        assert Paciente.objects.count() == 1  # Only our testing record in DB
        data = r.json()

        match data:
            case {
                "id": id,
                "ci": ci,
                "nombres": nombres,
                "apellidos": apellidos,
                "fecha_nacimiento": fecha_nacimiento,
            }:
                assert id == self.paciente.id
                assert ci == self.paciente.ci
                assert nombres != self.paciente.nombres
                assert nombres == update_data["nombres"]
                assert apellidos == self.paciente.apellidos
                assert (
                    date.fromisoformat(fecha_nacimiento)
                    == self.paciente.fecha_nacimiento
                )
            case _:
                assert False, "Missing fields in payload"

        instance = Paciente.objects.first()
        assert instance.nombres != old_name
        assert instance.nombres == update_data["nombres"]

    def test_delete_paciente(self):
        self.client.credentials()  # Clears credentials / Removes authentication HTTP headers
        assert Paciente.objects.count() == 1
        url = reverse("paciente-detail", args=[self.paciente.id])
        r = self.client.delete(url)
        self.assertEqual(
            r.status_code,
            403,
            "This request must be invalidated because the user is not logged in.",
        )
        assert Paciente.objects.count() == 1  # Not deleted
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        r = self.client.delete(url)
        self.assertEqual(r.status_code, 204)  # 204 No Content is ok in this case
        assert Paciente.objects.count() == 0  # Successfuly deleted

    def test_get_list_paciente(self):
        self.client.credentials()  # Clears credentials / Removes authentication HTTP headers

        url = reverse("paciente-list")
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
            [
                all(
                    map(
                        lambda x: x in result,
                        [
                            "id",
                            "ci",
                            "nombres",
                            "apellidos",
                            "email",
                            "telefono_celular",
                        ],
                    )
                )
                for result in data["results"]
            ]
        )

    def test_get_list_paciente_search_filter(self):
        def test_request(url, n_expected_records):
            self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
            r = self.client.get(url)
            self.assertEqual(r.status_code, 200)
            data = r.json()
            self.assertEqual(data["count"], n_expected_records, f"On request to {url}")
            self.assertEqual(
                len(data["results"]), n_expected_records, f"On request to {url}"
            )
            if n_expected_records:
                self.assertTrue(
                    all(
                        [
                            all(
                                map(
                                    lambda x: x in result,
                                    [
                                        "id",
                                        "ci",
                                        "nombres",
                                        "apellidos",
                                        "email",
                                        "telefono_celular",
                                    ],
                                )
                            )
                            for result in data["results"]
                        ]
                    ),
                    f"On request to {url}",
                )

        otro_paciente = create_paciente(
            nombres="bad", apellidos="bunny", email="otro_paciente@patolsima.com"
        )
        for url, n_expected_records in [
            (reverse("paciente-list") + "?" + urlencode({"search": "bad"}), 1),
            (reverse("paciente-list") + "?" + urlencode({"search": "bunny"}), 1),
            (
                reverse("paciente-list") + "?" + urlencode({"search": "bad bunny"}),
                1,
            ),
            (
                reverse("paciente-list") + "?" + urlencode({"search": "bat bunny"}),
                0,
            ),
            (
                reverse("paciente-list")
                + "?"
                + urlencode({"search": f"{otro_paciente.ci}"}),
                1,
            ),
            (
                reverse("paciente-list")
                + "?"
                + urlencode({"email": otro_paciente.email}),
                1,
            ),
            (
                reverse("paciente-list")
                + "?"
                + urlencode({"ci": f"{self.paciente.ci}"}),
                1,
            ),
            (
                reverse("paciente-list")
                + "?"
                + urlencode({"ci": f"{otro_paciente.ci}"}),
                1,
            ),
            (reverse("paciente-list"), 2),
        ]:
            test_request(url, n_expected_records)
