from datetime import datetime, date
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.urls import include, path, reverse
from rest_framework.test import APIClient, APITestCase
from patolsima_api.apps.core.models import Patologo


class PatologoTests(APITestCase):
    def setUp(self) -> None:
        self.patologo = Patologo.objects.create(
            nombres="patologo",
            apellidos="apellidos patologo",
            ncomed="12635",
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

    def test_get_patologo(self):
        self.client.credentials()  # Clears credentials / Removes authentication HTTP headers

        url = reverse("patologo-detail", args=[self.patologo.id])
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
                "id": patol_id,
                "ncomed": ncomed,
                "nombres": nombres,
                "apellidos": apellidos,
            }:
                assert patol_id == self.patologo.id
                assert nombres == self.patologo.nombres
                assert apellidos == self.patologo.apellidos
                assert ncomed == self.patologo.ncomed
            case _:
                assert False, "Missing fields in payload"

    def test_post_patologo(self):
        count_patologos = Patologo.objects.count()
        self.client.credentials()  # Clears credentials / Removes authentication HTTP headers
        creation_data = {
            "ncomed": self.patologo.ncomed,
            "nombres": "patologo test",
            "apellidos": "test apellidos",
        }
        url = reverse("patologo-list")
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
            405,
            "Method not allowed is the status required here",
        )

        assert Patologo.objects.count() == count_patologos

    def test_update_patologo(self):
        self.client.credentials()  # Clears credentials / Removes authentication HTTP headers

        update_data = {
            "id": self.patologo.id,
            "nombres": "nuevonombre",
            "apellidos": self.patologo.apellidos,
        }
        old_name = self.patologo.nombres
        assert Patologo.objects.count() == 1  # Only our testing record in DB

        url = reverse("patologo-detail", args=[self.patologo.id])
        r = self.client.put(url, update_data)
        self.assertEqual(
            r.status_code,
            403,
            "This request must be invalidated because the user is not logged in.",
        )

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        r = self.client.put(url, update_data)
        self.assertEqual(
            r.status_code,
            405,
            "Method not allowed is the status required here",
        )
        assert Patologo.objects.count() == 1  # Only our testing record in DB
        assert (
            Patologo.objects.first().nombres == old_name
        )  # Should not change given that the method is not allowed

    def test_delete_patologo(self):
        self.client.credentials()  # Clears credentials / Removes authentication HTTP headers
        assert Patologo.objects.count() == 1
        url = reverse("patologo-detail", args=[self.patologo.id])
        r = self.client.delete(url)
        self.assertEqual(
            r.status_code,
            403,
            "This request must be invalidated because the user is not logged in.",
        )
        assert Patologo.objects.count() == 1  # Not deleted
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        r = self.client.delete(url)
        self.assertEqual(
            r.status_code,
            405,
            "Method not allowed is the status required here",
        )  # 204 No Content is ok in this case
        assert (
            Patologo.objects.count() == 1
        )  # Delete not allowed so the number is constant

    def test_get_list_patologo(self):
        self.client.credentials()  # Clears credentials / Removes authentication HTTP headers

        url = reverse("patologo-list")
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
                ["id", "ncomed", "nombres", "apellidos"],
            )
        )
