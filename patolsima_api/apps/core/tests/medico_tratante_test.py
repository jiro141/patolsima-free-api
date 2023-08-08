from datetime import datetime, date
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from urllib.parse import urlencode
from django.urls import include, path, reverse
from rest_framework.test import APIClient, APITestCase
from patolsima_api.apps.core.models import MedicoTratante
from .mocks import create_medico_tratante, authenticate


# Create your tests here.
class MedicoTratanteTests(APITestCase):
    def setUp(self) -> None:
        self.medico_tratante = create_medico_tratante()
        self.user, self.token = authenticate(self.client)

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

    def test_post_medico_no_authentication_failed(self):
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

    def test_post_medico_unique_constraint_failure(self):
        count_medicos = MedicoTratante.objects.count()
        self.client.credentials()  # Clears credentials / Removes authentication HTTP headers
        creation_data = {
            "ncomed": self.medico_tratante.ncomed,
            "nombres": "medico test",
            "apellidos": "test apellidos",
            "especialidad": "mondacologia",
        }
        url = reverse("medico-list")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        r = self.client.post(url, creation_data)
        self.assertEqual(
            r.status_code,
            500,
            "The request must be rejected because the NCOMED already exists.",
        )

    def test_post_medico_success(self):
        count_medicos = MedicoTratante.objects.count()
        self.client.credentials()  # Clears credentials / Removes authentication HTTP headers
        creation_data = {
            "ncomed": "0000",
            "nombres": "medico test",
            "apellidos": "test apellidos",
            "especialidad": "mondacologia",
        }
        url = reverse("medico-list")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
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
            "ci": "123",
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
            [
                all(
                    map(
                        lambda x: x in result,
                        [
                            "id",
                            "ncomed",
                            "nombres",
                            "apellidos",
                            "especialidad",
                        ],
                    )
                )
                for result in data["results"]
            ]
        )

    def test_get_list_medico_tratante_search_filter(self):
        def test_request(url, n_expected_records):
            self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
            r = self.client.get(url)
            self.assertEqual(r.status_code, 200)
            data = r.json()
            self.assertEqual(data["count"], n_expected_records, url)
            self.assertEqual(len(data["results"]), n_expected_records, url)
            if n_expected_records:
                assert all(
                    [
                        all(
                            map(
                                lambda x: x in result,
                                [
                                    "id",
                                    "ncomed",
                                    "nombres",
                                    "apellidos",
                                    "especialidad",
                                ],
                            )
                        )
                        for result in data["results"]
                    ]
                )

        otro_medico = create_medico_tratante(
            nombres="bad", apellidos="bunny", ncomed="987", especialidad="neurocirugia"
        )
        for url, n_expected_records in [
            (reverse("medico-list") + "?" + urlencode({"search": "bad"}), 1),
            (reverse("medico-list") + "?" + urlencode({"search": "bunny"}), 1),
            (
                reverse("medico-list") + "?" + urlencode({"search": "bad bunny"}),
                1,
            ),
            (
                reverse("medico-list") + "?" + urlencode({"search": "bat bunny"}),
                0,
            ),
            (
                reverse("medico-list")
                + "?"
                + urlencode({"search": otro_medico.ncomed}),
                1,
            ),
            (reverse("medico-list") + "?" + urlencode({"search": "neuro"}), 1),
            (reverse("medico-list") + "?" + urlencode({"search": "neurocirugia"}), 1),
            (reverse("medico-list"), 2),
        ]:
            test_request(url, n_expected_records)
