from datetime import datetime, date
from urllib.parse import urlencode
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.urls import include, path, reverse
from rest_framework.test import APIClient, APITestCase
from patolsima_api.apps.core.models import Paciente, Muestra, Estudio
from .mocks import (
    create_estudio,
    create_muestra,
    create_patologo,
    create_paciente,
    create_medico_tratante,
    authenticate,
)


# Create your tests here.
class EstudioTests(APITestCase):
    def setUp(self) -> None:
        self.estudio = create_estudio()
        self.muestra_1_estudio = create_muestra(self.estudio)
        self.muestra_2_estudio = create_muestra(self.estudio)
        self.muestra_2_estudio.estado = Muestra.Estados.DIAGNOSTICO_MICROSCOPICO
        self.muestra_2_estudio.save()
        self.user, self.token = authenticate(self.client)

    def test_get_estudio(self):
        self.client.credentials()  # Clears credentials / Removes authentication HTTP headers

        url = reverse("estudio-detail", args=[self.estudio.id])
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
                "paciente": paciente,
                "medico_tratante": medico_tratante,
                "patologo": patologo,
                "muestras": muestras,
                "tipo": tipo_estudio,
            }:
                self.assertEqual(id, self.estudio.id)
                self.assertEqual(paciente["ci"], self.estudio.paciente.ci)
                self.assertEqual(medico_tratante["id"], self.estudio.medico_tratante.id)
                self.assertEqual(patologo["id"], self.estudio.patologo.id)
                self.assertEqual(len(muestras), 2)
                id_muestras = [r["id"] for r in muestras]
                self.assertIn(self.muestra_1_estudio.id, id_muestras)
                self.assertIn(self.muestra_2_estudio.id, id_muestras)
                self.assertEqual(tipo_estudio, self.estudio.tipo)
            case _:
                assert False, "Missing fields in payload"

    def test_post_estudio(self):
        count_estudios = Estudio.objects.count()
        self.client.credentials()  # Clears credentials / Removes authentication HTTP headers
        new_paciente, new_medico, new_patologo = (
            create_paciente(),
            create_medico_tratante(),
            create_patologo(),
        )
        creation_data = {
            "paciente_ci": new_paciente.ci,
            "medico_tratante_id": new_medico.id,
            "patologo_id": new_patologo.id,
            "notas": "Esto es una nota",
            "urgente": True,
            "envio_digital": True,
            "tipo": Estudio.TipoEstudio.CITOLOGIA_ESPECIAL,
        }
        url = reverse("estudio-list")
        r = self.client.post(url, creation_data)
        self.assertEqual(
            r.status_code,
            403,
            "This request must be invalidated because the user is not logged in.",
        )
        self.assertEqual(Estudio.objects.count(), count_estudios)

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        r = self.client.post(url, creation_data)
        self.assertEqual(r.status_code, 201, "Estudio created")
        data = r.json()
        self.assertEqual(Estudio.objects.count(), (count_estudios + 1))
        match data:
            case {
                "paciente": paciente,
                "medico_tratante": medico_tratante,
                "patologo": patologo,
                "tipo": tipo,
                "urgente": urgente,
                "envio_digital": envio_digital,
                "muestras": muestras,
            }:
                self.assertEquals(paciente["ci"], creation_data["paciente_ci"])
                self.assertEquals(paciente["ci"], new_paciente.ci)
                self.assertEquals(
                    medico_tratante["id"], creation_data["medico_tratante_id"]
                )
                self.assertEquals(medico_tratante["id"], new_medico.id)
                self.assertEquals(patologo["id"], creation_data["patologo_id"])
                self.assertEquals(patologo["id"], new_patologo.id)
                self.assertEqual(tipo, creation_data["tipo"])
                self.assertEqual(urgente, creation_data["urgente"])
                self.assertEqual(envio_digital, creation_data["envio_digital"])
                self.assertEqual(
                    len(muestras), 0, "At this stage the samples haven't been added"
                )
            case _:
                assert False, "Missing fields in payload"

    def test_update_estudio(self):
        self.client.credentials()  # Clears credentials / Removes authentication HTTP headers

        update_data = {
            "paciente_ci": self.estudio.paciente.ci,
            "medico_tratante_id": self.estudio.medico_tratante.id,
            "patologo_id": self.estudio.patologo.id,
            "notas": "Otra nota",
        }
        old_notas = self.estudio.notas
        assert Estudio.objects.count() == 1  # Only our testing record in DB

        url = reverse("estudio-detail", args=[self.estudio.id])
        r = self.client.put(url, update_data)
        self.assertEqual(
            r.status_code,
            403,
            "This request must be invalidated because the user is not logged in.",
        )

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        r = self.client.put(url, update_data)
        self.assertEqual(r.status_code, 200)
        assert Estudio.objects.count() == 1  # Only our testing record in DB
        data = r.json()

        match data:
            case {
                "paciente": paciente,
                "medico_tratante": medico_tratante,
                "patologo": patologo,
                "tipo": tipo,
                "urgente": urgente,
                "envio_digital": envio_digital,
                "muestras": muestras,
            }:
                self.assertEquals(paciente["ci"], self.estudio.paciente.ci)
                self.assertEquals(
                    medico_tratante["id"], self.estudio.medico_tratante.id
                )
                self.assertEquals(patologo["id"], self.estudio.patologo.id)
            case _:
                assert False, "Missing fields in payload"

        instance = Estudio.objects.first()
        assert instance.notas != old_notas
        assert instance.notas == update_data["notas"]

    def test_delete_estudio(self):
        self.client.credentials()  # Clears credentials / Removes authentication HTTP headers
        assert Estudio.objects.count() == 1
        url = reverse("estudio-detail", args=[self.estudio.id])
        r = self.client.delete(url)
        self.assertEqual(
            r.status_code,
            403,
            "This request must be invalidated because the user is not logged in.",
        )
        assert Estudio.objects.count() == 1  # Not deleted
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)
        r = self.client.delete(url)
        self.assertEqual(r.status_code, 204)  # 204 No Content is ok in this case
        assert Estudio.objects.count() == 0  # Successfuly deleted

    def test_get_list_estudio(self):
        self.client.credentials()  # Clears credentials / Removes authentication HTTP headers

        url = reverse("estudio-list")
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
        assert Estudio.objects.count()
        assert data["count"] == 1
        assert len(data["results"]) == 1
        from pprint import pprint

        pprint(data["results"])
        self.assertTrue(
            all(
                [
                    all(
                        map(
                            lambda x: x in result,
                            [
                                "id",
                                "paciente",
                                "medico_tratante",
                                "patologo",
                                "tipo",
                                "prioridad",
                            ],
                        )
                    )
                    for result in data["results"]
                ]
            ),
            f"On request to {url}",
        )

    def test_get_list_estudio_search_filter(self):
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
                                        "paciente",
                                        "medico_tratante",
                                        "patologo",
                                        "tipo",
                                        "prioridad",
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
        otro_estudio = create_estudio()
        assert Estudio.objects.count() == 2
        for url, n_expected_records in [
            (reverse("estudio-list") + "?" + urlencode({"search": "bad"}), 1),
            (reverse("estudio-list") + "?" + urlencode({"search": "bunny"}), 1),
            (
                reverse("estudio-list") + "?" + urlencode({"search": "bad bunny"}),
                1,
            ),
            (
                reverse("estudio-list") + "?" + urlencode({"search": "bat bunny"}),
                0,
            ),
            (
                reverse("estudio-list")
                + "?"
                + urlencode({"search": f"{otro_estudio.paciente.ci}"}),
                1,
            ),
            (
                reverse("estudio-list")
                + "?"
                + urlencode({"paciente": f"{otro_estudio.paciente.ci}"}),
                1,
            ),
            (
                reverse("estudio-list")
                + "?"
                + urlencode({"codigo": f"{self.estudio.codigo}"}),
                1,
            ),
            (
                reverse("estudio-list")
                + "?"
                + urlencode({"codigo": f"{otro_estudio.codigo}"}),
                1,
            ),
            (
                reverse("estudio-list")
                + "?"
                + urlencode({"tipo": f"{otro_estudio.tipo}"}),
                1,
            ),
            (reverse("estudio-list"), 2),
        ]:
            test_request(url, n_expected_records)
