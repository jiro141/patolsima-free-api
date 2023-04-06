from parameterized import parameterized
from django.urls import include, path, reverse
from rest_framework.test import APIClient, APITestCase
from patolsima_api.apps.core.models import Muestra, FaseMuestra
from .mocks import create_estudio, create_muestra, authenticate


# Create your tests here.
class FaseMuestraTests(APITestCase):
    def setUp(self) -> None:
        self.estudio = create_estudio()
        self.muestra = create_muestra(self.estudio)
        self.user, self.token = authenticate(self.client)

    def test_muestra_change_estado_on_fase_muestra_creation(self):
        old_estado = self.muestra.estado
        new_fase = self.muestra.fases.create(
            muestra=self.muestra,
            notas="Fase triste",
            estado=Muestra.Estados.DESCRIPCION_MACROSCOPICA,
        )
        self.muestra.refresh_from_db()
        self.assertEqual(self.muestra.fases.count(), 2)
        self.assertNotEqual(self.muestra.estado, old_estado)
        self.assertEqual(self.muestra.estado, new_fase.estado)

    def test_get_fase_muestra(self):
        self.client.credentials()  # Clears credentials / Removes authentication HTTP headers
        new_fase = self.muestra.fases.create(
            muestra=self.muestra,
            notas="Fase triste",
            estado=Muestra.Estados.DESCRIPCION_MACROSCOPICA,
        )

        url = reverse("fase-muestra-detail", args=[new_fase.id])
        url2 = reverse("muestra-detail", args=[self.muestra.id])
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
        self.assertEqual(data["muestra"], self.muestra.id)
        self.assertEqual(data["id"], new_fase.id)
        self.assertEqual(data["notas"], new_fase.notas)
        self.assertEqual(data["estado"], new_fase.estado)

        r = self.client.get(url2)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data["id"], self.muestra.id)
        self.assertEqual(data["estado"], new_fase.estado)
        self.assertEqual(len(data["fases"]), 2)
        self.assertEqual(data["fases"][1]["id"], new_fase.id)

    @parameterized.expand(
        [(str(choice), choice[0]) for i, choice in enumerate(Muestra.Estados.choices)]
    )
    def test_post_fase_muestra(self, name, estado):
        count_fases_muestras = FaseMuestra.objects.count()
        count_fases_muestras_of_muestra = self.muestra.fases.count()

        self.client.credentials()  # Clears credentials / Removes authentication HTTP headers
        creation_data = {
            "muestra": self.muestra.id,
            "estado": estado,
            "notas": f"En {estado}",
        }
        url = reverse("fase-muestra-list")
        url2 = reverse("muestra-detail", args=[self.muestra.id])
        r = self.client.post(url, creation_data)
        self.assertEqual(
            r.status_code,
            403,
            "This request must be invalidated because the user is not logged in.",
        )

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        r = self.client.post(url, creation_data)
        r2 = self.client.get(url2)

        self.assertEqual(r.status_code, 201, "FaseMuestra must be created")
        self.assertEqual(r2.status_code, 200)
        data, data2 = r.json(), r2.json()
        self.assertEqual(FaseMuestra.objects.count(), (count_fases_muestras + 1))
        self.assertEqual(
            self.muestra.fases.count(), (count_fases_muestras_of_muestra + 1)
        )
        self.assertEqual(data["muestra"], self.muestra.id)
        self.assertEqual(data["estado"], estado)
        self.assertEqual(data2["estado"], estado)
        self.assertEqual(len(data2["fases"]), count_fases_muestras_of_muestra + 1)
        self.assertEqual(data2["fases"][-1]["id"], data["id"])

    def test_update_fase_muestra(self):
        self.client.credentials()  # Clears credentials / Removes authentication HTTP headers

        new_fase = self.muestra.fases.create(
            muestra=self.muestra,
            notas="Fase triste",
            estado=Muestra.Estados.DESCRIPCION_MACROSCOPICA,
        )

        update_data = {
            "id": new_fase.id,
            "muestra": self.muestra.id,
            "estado": Muestra.Estados.ALMACENAMIENTO,
            "notas": "fase feliz",
        }

        old_tm = self.muestra.tipo_de_muestra
        assert self.muestra.fases.count() == 2  # Only our testing records in DB

        url = reverse("fase-muestra-detail", args=[new_fase.id])
        r = self.client.put(url, update_data)
        self.assertEqual(
            r.status_code,
            403,
            "This request must be invalidated because the user is not logged in.",
        )

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        r = self.client.put(url, update_data)
        self.assertEqual(r.status_code, 200)
        data = r.json()
        assert self.muestra.fases.count() == 2  # Only our testing records in DB
        self.muestra.refresh_from_db()
        self.assertEqual(data["id"], new_fase.id)
        self.assertEqual(data["muestra"], self.muestra.id)
        self.assertEqual(data["estado"], update_data["estado"])
        self.assertEqual(
            self.muestra.estado, Muestra.Estados.DESCRIPCION_MACROSCOPICA
        )  # Estado of Muestra must not change if a FaseMuestra instance is changed

    def test_delete_fase_muestra(self):
        self.client.credentials()  # Clears credentials / Removes authentication HTTP headers
        self.assertEqual(Muestra.objects.count(), 1)
        url = reverse("fase-muestra-detail", args=[self.muestra.fases.first().id])
        r = self.client.delete(url)
        self.assertEqual(
            r.status_code,
            403,
            "This request must be invalidated because the user is not logged in.",
        )
        self.assertEqual(self.muestra.fases.count(), 1)  # Not deleted
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        r = self.client.delete(url)
        self.assertEqual(r.status_code, 204)  # 204 No Content is ok in this case
        self.assertEqual(self.muestra.fases.count(), 0)  # Successfuly deleted

    def test_get_list_muestra(self):
        self.client.credentials()  # Clears credentials / Removes authentication HTTP headers

        url = reverse("fase-muestra-list")
        r = self.client.get(url)
        self.assertEqual(
            r.status_code,
            403,
            "This request must be invalidated because the user is not logged in.",
        )

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        r = self.client.get(url)
        self.assertEqual(r.status_code, 405)  # this method must not be implemented
