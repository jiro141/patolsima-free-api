from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.db import transaction
from datetime import date, datetime
from decimal import Decimal
import random

from patolsima_api.apps.core.models import (
    Paciente,
    MedicoTratante,
    Patologo,
    Estudio,
    Muestra,
    FaseMuestra,
    Informe,
    ResultadoInmunostoquimica,
)
from patolsima_api.apps.facturacion.models import (
    Cliente,
    Orden,
    ItemOrden,
    Pago,
    Factura,
    Recibo,
    CambioUSDBS,
)
from patolsima_api.apps.facturacion.models.recibo_y_factura import (
    NotasCredito,
    NotasDebito,
    FacturaOffset,
)
from patolsima_api.apps.facturacion.models.transaccion import Transaccion
from patolsima_api.apps.uploaded_file_management.models import UploadedFile


class Command(BaseCommand):
    help = "Pobla la base de datos con datos de prueba completos para todas las secciones"

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Elimina todos los datos antes de crear nuevos",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["flush"]:
            self.stdout.write("Eliminando datos existentes...")
            self._flush_data()

        self.stdout.write("Iniciando poblacion de datos de prueba...")

        # 1. Crear usuario y grupos
        self._create_users_and_groups()

        # 2. Crear archivos de prueba (UploadedFile)
        files = self._create_uploaded_files()

        # 3. Crear tipo de cambio
        cambio = self._create_cambio_dolar()

        # 4. Crear pacientes
        pacientes = self._create_pacientes()

        # 5. Crear medicos tratantes
        medicos = self._create_medicos()

        # 6. Crear patologos (asociados a usuarios)
        patologos = self._create_patologos()

        # 7. Crear estudios
        estudios = self._create_estudios(pacientes, medicos, patologos)

        # 8. Crear muestras (auto-crea FaseMuestra por signal)
        muestras = self._create_muestras(estudios)

        # 9. Crear informes
        informes = self._create_informes(estudios, files)

        # 10. Crear resultados de inmunostoquimica
        self._create_resultados_inmunostoquimica(informes)

        # 11. Crear clientes
        clientes = self._create_clientes()

        # 12. Crear ordenes
        ordenes = self._create_ordenes(clientes, estudios)

        # 13. Crear items de orden
        self._create_items_orden(ordenes, estudios)

        # 14. Crear pagos
        pagos = self._create_pagos(ordenes)

        # 15. Crear facturas
        self._create_facturas(ordenes, files)

        # 16. Crear recibos
        self._create_recibos(ordenes, files)

        # 17. Crear notas de credito y debito
        self._create_notas(ordenes, files)

        # 18. Crear transacciones
        self._create_transacciones(clientes)

        # 19. Crear offsets
        self._create_offsets()

        self.stdout.write(self.style.SUCCESS("Datos de prueba creados exitosamente!"))
        self._print_summary()

    def _flush_data(self):
        """Elimina todos los datos de prueba"""
        Transaccion.objects.all().delete()
        NotasDebito.objects.all().delete()
        NotasCredito.objects.all().delete()
        Recibo.objects.all().delete()
        Factura.objects.all().delete()
        Pago.objects.all().delete()
        ItemOrden.objects.all().delete()
        Orden.objects.all().delete()
        ResultadoInmunostoquimica.objects.all().delete()
        Informe.objects.all().delete()
        FaseMuestra.objects.all().delete()
        Muestra.objects.all().delete()
        Estudio.objects.all().delete()
        Patologo.objects.all().delete()
        MedicoTratante.objects.all().delete()
        Paciente.objects.all().delete()
        Cliente.objects.all().delete()
        CambioUSDBS.objects.all().delete()
        UploadedFile.objects.all().delete()
        FacturaOffset.objects.all().delete()
        self.stdout.write("Datos eliminados.")

    def _create_users_and_groups(self):
        """Crea usuarios y grupos de prueba"""
        self.stdout.write("Creando usuarios y grupos...")

        # Crear grupos
        grupos_nombres = ["admin", "patologo", "recepcion", "facturacion"]
        grupos = {}
        for nombre in grupos_nombres:
            grupo, _ = Group.objects.get_or_create(name=nombre)
            grupos[nombre] = grupo

        # Crear superusuario
        if not User.objects.filter(username="admin").exists():
            admin = User.objects.create_superuser(
                username="admin",
                email="admin@patolsima.com",
                password="admin123",
                first_name="Admin",
                last_name="Sistema",
            )
            admin.groups.add(grupos["admin"])
        else:
            admin = User.objects.get(username="admin")

        # Crear usuario patologo
        if not User.objects.filter(username="dr_martinez").exists():
            user_patologo = User.objects.create_user(
                username="dr_martinez",
                email="martinez@patolsima.com",
                password="patologo123",
                first_name="Carlos",
                last_name="Martinez",
            )
            user_patologo.groups.add(grupos["patologo"])
        else:
            user_patologo = User.objects.get(username="dr_martinez")

        # Crear usuario recepcion
        if not User.objects.filter(username="recepcion1").exists():
            user_recepcion = User.objects.create_user(
                username="recepcion1",
                email="recepcion@patolsima.com",
                password="recepcion123",
                first_name="Maria",
                last_name="Gonzalez",
            )
            user_recepcion.groups.add(grupos["recepcion"])

        # Crear usuario facturacion
        if not User.objects.filter(username="facturacion1").exists():
            user_facturacion = User.objects.create_user(
                username="facturacion1",
                email="facturacion@patolsima.com",
                password="facturacion123",
                first_name="Pedro",
                last_name="Lopez",
            )
            user_facturacion.groups.add(grupos["facturacion"])

        self.stdout.write(f"  Usuarios creados: admin, dr_martinez, recepcion1, facturacion1")
        return admin, user_patologo

    def _create_uploaded_files(self):
        """Crea archivos de prueba"""
        self.stdout.write("Creando archivos de prueba...")
        archivos = []
        nombres_archivos = [
            ("informe_001.pdf", "application/pdf", 1024),
            ("imagen_microscopio.jpg", "image/jpeg", 2048),
            ("resultado_laboratorio.pdf", "application/pdf", 512),
            ("foto_biopsia.png", "image/png", 3072),
            ("doc_adjunto.docx", "application/msword", 256),
            ("factura_001.pdf", "application/pdf", 1024),
            ("factura_002.pdf", "application/pdf", 1024),
            ("recibo_001.pdf", "application/pdf", 512),
            ("recibo_002.pdf", "application/pdf", 512),
            ("nota_001.pdf", "application/pdf", 256),
            ("nota_002.pdf", "application/pdf", 256),
        ]

        for nombre, tipo, size in nombres_archivos:
            archivo, _ = UploadedFile.objects.get_or_create(
                file_name=nombre,
                defaults={
                    "size": size,
                    "content_type": tipo,
                    "storage_unit": "LOCAL_STORAGE",
                },
            )
            archivos.append(archivo)

        self.stdout.write(f"  Archivos creados: {len(archivos)}")
        return archivos

    def _create_cambio_dolar(self):
        """Crea tipo de cambio USD/BS"""
        self.stdout.write("Creando tipo de cambio USD/BS...")
        cambio, _ = CambioUSDBS.objects.get_or_create(
            bs_e=Decimal("36.50"),
            defaults={},
        )
        self.stdout.write(f"  Tipo de cambio: 1 USD = {cambio.bs_e} BS")
        return cambio

    def _create_pacientes(self):
        """Crea pacientes de prueba"""
        self.stdout.write("Creando pacientes...")
        pacientes_data = [
            {
                "ci": "V-12345678",
                "nombres": "Juan Carlos",
                "apellidos": "Perez Rodriguez",
                "fecha_nacimiento": date(1985, 3, 15),
                "sexo": "MASCULINO",
                "email": "juan.perez@email.com",
                "telefono_celular": "+584121234567",
                "direccion": "Av. Libertador, Caracas",
            },
            {
                "ci": "V-23456789",
                "nombres": "Maria Fernanda",
                "apellidos": "Lopez Garcia",
                "fecha_nacimiento": date(1990, 7, 22),
                "sexo": "FEMENINO",
                "email": "maria.lopez@email.com",
                "telefono_celular": "+584149876543",
                "direccion": "Calle Principal, Valencia",
            },
            {
                "ci": "V-34567890",
                "nombres": "Pedro Antonio",
                "apellidos": "Sanchez Martinez",
                "fecha_nacimiento": date(1978, 11, 5),
                "sexo": "MASCULINO",
                "email": "pedro.sanchez@email.com",
                "telefono_celular": "+584245551234",
                "direccion": "Urb. El Parque, Maracay",
            },
            {
                "ci": "V-45678901",
                "nombres": "Ana Patricia",
                "apellidos": "Rodriguez Fernandez",
                "fecha_nacimiento": date(1995, 1, 30),
                "sexo": "FEMENINO",
                "email": "ana.rodriguez@email.com",
                "telefono_celular": "+584127778899",
                "direccion": "Res. Las Flores, Barquisimeto",
            },
            {
                "ci": "V-56789012",
                "nombres": "Luis Eduardo",
                "apellidos": "Gomez Hernandez",
                "fecha_nacimiento": date(1982, 6, 18),
                "sexo": "MASCULINO",
                "email": "luis.gomez@email.com",
                "telefono_celular": "+584163334455",
                "direccion": "Av. Principal, Merida",
            },
        ]

        pacientes = []
        for data in pacientes_data:
            paciente, _ = Paciente.objects.get_or_create(
                ci=data["ci"],
                defaults=data,
            )
            pacientes.append(paciente)

        self.stdout.write(f"  Pacientes creados: {len(pacientes)}")
        return pacientes

    def _create_medicos(self):
        """Crea medicos tratantes de prueba"""
        self.stdout.write("Creando medicos tratantes...")
        medicos_data = [
            {
                "ci": "V-11111111",
                "nombres": "Roberto",
                "apellidos": "Garcia Lopez",
                "ncomed": "MED-001",
                "especialidad": "Cirugia General",
                "email": "roberto.garcia@clinica.com",
                "telefono_celular": "+584121111111",
            },
            {
                "ci": "V-22222222",
                "nombres": "Carmen",
                "apellidos": "Torres Ruiz",
                "ncomed": "MED-002",
                "especialidad": "Ginecologia",
                "email": "carmen.torres@clinica.com",
                "telefono_celular": "+584142222222",
            },
            {
                "ci": "V-33333333",
                "nombres": "Fernando",
                "apellidos": "Diaz Moreno",
                "ncomed": "MED-003",
                "especialidad": "Dermatologia",
                "email": "fernando.diaz@clinica.com",
                "telefono_celular": "+584243333333",
            },
            {
                "ci": "V-44444444",
                "nombres": "Isabel",
                "apellidos": "Morales Castro",
                "ncomed": "MED-004",
                "especialidad": "Oncologia",
                "email": "isabel.morales@clinica.com",
                "telefono_celular": "+584124444444",
            },
        ]

        medicos = []
        for data in medicos_data:
            medico, _ = MedicoTratante.objects.get_or_create(
                ci=data["ci"],
                ncomed=data["ncomed"],
                defaults=data,
            )
            medicos.append(medico)

        self.stdout.write(f"  Medicos creados: {len(medicos)}")
        return medicos

    def _create_patologos(self):
        """Crea patologos de prueba (asociados a usuarios)"""
        self.stdout.write("Creando patologos...")

        user_patologo = User.objects.get(username="dr_martinez")

        patologos_data = [
            {
                "nombres": "Carlos",
                "apellidos": "Martinez",
                "ncomed": "PAT-001",
                "user": user_patologo,
            },
            {
                "nombres": "Laura",
                "apellidos": "Fernandez",
                "ncomed": "PAT-002",
                "user": None,
            },
        ]

        patologos = []
        for data in patologos_data:
            user = data.pop("user")
            patologo, _ = Patologo.objects.get_or_create(
                ncomed=data["ncomed"],
                defaults={**data, "user": user},
            )
            patologos.append(patologo)

        self.stdout.write(f"  Patologos creados: {len(patologos)}")
        return patologos

    def _create_estudios(self, pacientes, medicos, patologos):
        """Crea estudios de prueba"""
        self.stdout.write("Creando estudios...")
        estudios_data = [
            {
                "paciente": pacientes[0],
                "medico_tratante": medicos[0],
                "patologo": patologos[0],
                "notas": "Biopsia de tejido cutaneo, lesiones sospechosas",
                "urgente": True,
                "tipo": "BIOPSIA",
            },
            {
                "paciente": pacientes[1],
                "medico_tratante": medicos[1],
                "patologo": patologos[0],
                "notas": "Citologia ginecologica de rutina",
                "urgente": False,
                "tipo": "CITOLOGIA_GINECOLOGICA",
            },
            {
                "paciente": pacientes[2],
                "medico_tratante": medicos[2],
                "patologo": patologos[1],
                "notas": "Biopsia para estudio de melanoma",
                "urgente": True,
                "tipo": "BIOPSIA",
            },
            {
                "paciente": pacientes[3],
                "medico_tratante": medicos[3],
                "patologo": patologos[0],
                "notas": "Citologia especial - estudo de celulas atipicas",
                "urgente": False,
                "tipo": "CITOLOGIA_ESPECIAL",
            },
            {
                "paciente": pacientes[4],
                "medico_tratante": medicos[0],
                "patologo": patologos[1],
                "notas": "Inmunohistoquimica para confirmar diagnostico",
                "urgente": False,
                "tipo": "INMUNOHISTOQUIMICA",
            },
        ]

        estudios = []
        for data in estudios_data:
            estudio, _ = Estudio.objects.get_or_create(
                paciente=data["paciente"],
                notas=data["notas"],
                defaults=data,
            )
            estudios.append(estudio)

        self.stdout.write(f"  Estudios creados: {len(estudios)}")
        return estudios

    def _create_muestras(self, estudios):
        """Crea muestras de prueba (auto-crea FaseMuestra por signal)"""
        self.stdout.write("Creando muestras...")
        muestras_data = [
            {
                "estudio": estudios[0],
                "tipo_de_muestra": "Biopsia cutanea",
                "descripcion": "Fragmento de tejido de 2x1 cm",
                "estado": "RECIBIDA",
            },
            {
                "estudio": estudios[1],
                "tipo_de_muestra": "Citologia cervico-vaginal",
                "descripcion": "Muestra de exocervix",
                "estado": "COLORACION",
            },
            {
                "estudio": estudios[2],
                "tipo_de_muestra": "Biopsia de piel",
                "descripcion": "Lesion pigmented de 0.5 cm",
                "estado": "DESHIDRATACION",
            },
            {
                "estudio": estudios[3],
                "tipo_de_muestra": "Citologia especial",
                "descripcion": "Muestra de liquido ascitico",
                "estado": "INCLUSION_EN_PARAFINA",
            },
            {
                "estudio": estudios[4],
                "tipo_de_muestra": "Tejido para IHQ",
                "descripcion": "Bloque de tejido fijado en formalina",
                "estado": "CORTE_MICROTOMO",
            },
            {
                "estudio": estudios[0],
                "tipo_de_muestra": "Segunda biopsia",
                "descripcion": "Fragmento adicional del mismo sitio",
                "estado": "RECIBIDA",
            },
        ]

        muestras = []
        for data in muestras_data:
            # Evitar duplicados
            if not Muestra.objects.filter(
                estudio=data["estudio"],
                tipo_de_muestra=data["tipo_de_muestra"],
            ).exists():
                muestra = Muestra.objects.create(**data)
                muestras.append(muestra)
            else:
                muestras.append(
                    Muestra.objects.get(
                        estudio=data["estudio"],
                        tipo_de_muestra=data["tipo_de_muestra"],
                    )
                )

        self.stdout.write(f"  Muestras creadas: {len(muestras)}")
        self.stdout.write(f"  FasesMuestra auto-creadas: {len(muestras)} (por signal)")
        return muestras

    def _create_informes(self, estudios, archivos):
        """Crea informes de prueba"""
        self.stdout.write("Creando informes...")
        informes_data = [
            {
                "estudio": estudios[0],
                "descripcion_macroscopica": "Fragmento de tejido cutaneo de coloracion variable, con areas de pigmentacion oscura",
                "descripcion_microscopica": "Se observa proliferation de melanocitos atipicos con patron de crecimiento anomalo",
                "muestra_recibida": "Biopsia cutanea en formol al 10%",
                "diagnostico": "Melanoma cutaneo de tipo superficial extenso",
                "notas": "Se recomienda margen quirurgico amplio",
                "completado": True,
                "aprobado": True,
            },
            {
                "estudio": estudios[1],
                "descripcion_macroscopica": "Muestra liquida centrifugada, deposito celuloso",
                "descripcion_microscopica": "Celiteglandular con celulas escamosas superficiales",
                "muestra_recibida": "Citologia en base liquida",
                "diagnostico": "Citologia negativa para lesion intraepitelial",
                "notas": "Control en 12 meses",
                "completado": True,
                "aprobado": False,
            },
            {
                "estudio": estudios[2],
                "descripcion_macroscopica": "Lesion pigmentada de 5mm con bordes irregulares",
                "descripcion_microscopica": "Nidos de melanocitos atipicos en la union dermo-epidermica",
                "muestra_recibida": "Biopsia por punch de 4mm",
                "diagnostico": "Nevo displasico vs Melanoma in situ",
                "notas": "Se requiere estudio adicional",
                "completado": False,
                "aprobado": False,
            },
        ]

        informes = []
        for data in informes_data:
            if not Informe.objects.filter(estudio=data["estudio"]).exists():
                informe = Informe.objects.create(**data)
                informes.append(informe)
            else:
                informes.append(Informe.objects.get(estudio=data["estudio"]))

        self.stdout.write(f"  Informes creados: {len(informes)}")
        return informes

    def _create_resultados_inmunostoquimica(self, informes):
        """Crea resultados de inmunostoquimica para informes de tipo INMUNOSTOQUIMICA"""
        self.stdout.write("Creando resultados de inmunostoquimica...")

        # Solo crear para informes que tengan estudios de tipo INMUNOSTOQUIMICA
        count = 0
        for informe in informes:
            if informe.estudio.tipo == "INMUNOSTOQUIMICA":
                if not ResultadoInmunostoquimica.objects.filter(
                    informe=informe
                ).exists():
                    ResultadoInmunostoquimica.objects.create(
                        informe=informe,
                        procedimiento="Hematoxilina-Eosina",
                        reaccion="Positiva para citokeratinas",
                        diagnostico_observaciones="Patron compatible con carcinoma",
                    )
                    count += 1

        self.stdout.write(f"  Resultados IHQ creados: {count}")

    def _create_clientes(self):
        """Crea clientes de prueba"""
        self.stdout.write("Creando clientes...")
        clientes_data = [
            {
                "razon_social": "Clinica Santa Maria C.A.",
                "ci_rif": "J-40123456-7",
                "email": "clinica@santamaria.com",
                "telefono_celular": "+584125551234",
                "direccion": "Av. Principal, Caracas",
            },
            {
                "razon_social": "Laboratorio Clinico Valencia",
                "ci_rif": "J-30987654-3",
                "email": "lab@labvalencia.com",
                "telefono_celular": "+584146667788",
                "direccion": "Calle 5, Valencia",
            },
            {
                "razon_social": "Centro Medico Maracay",
                "ci_rif": "J-29876543-2",
                "email": "centro@medimaracay.com",
                "telefono_celular": "+584248889900",
                "direccion": "Av. Bolivar, Maracay",
            },
            {
                "razon_social": "Paciente Particular",
                "ci_rif": "V-12345678",
                "email": "juan.perez@email.com",
                "telefono_celular": "+584121234567",
                "direccion": "Av. Libertador, Caracas",
            },
        ]

        clientes = []
        for data in clientes_data:
            cliente, _ = Cliente.objects.get_or_create(
                ci_rif=data["ci_rif"],
                defaults=data,
            )
            clientes.append(cliente)

        self.stdout.write(f"  Clientes creados: {len(clientes)}")
        return clientes

    def _create_ordenes(self, clientes, estudios):
        """Crea ordenes de prueba"""
        self.stdout.write("Creando ordenes...")
        ordenes = []

        # Orden 1 - Clinica Santa Maria - 2 estudios
        orden1, _ = Orden.objects.get_or_create(
            cliente=clientes[0],
            confirmada=True,
        )
        ordenes.append(orden1)

        # Orden 2 - Laboratorio Valencia - 1 estudio
        orden2, _ = Orden.objects.get_or_create(
            cliente=clientes[1],
            confirmada=True,
        )
        ordenes.append(orden2)

        # Orden 3 - Centro Medico - 1 estudio (sin confirmar)
        orden3, _ = Orden.objects.get_or_create(
            cliente=clientes[2],
            confirmada=False,
        )
        ordenes.append(orden3)

        # Orden 4 - Particular - 1 estudio
        orden4, _ = Orden.objects.get_or_create(
            cliente=clientes[3],
            confirmada=True,
        )
        ordenes.append(orden4)

        self.stdout.write(f"  Ordenes creadas: {len(ordenes)}")
        return ordenes

    def _create_items_orden(self, ordenes, estudios):
        """Crea items de orden de prueba"""
        self.stdout.write("Creando items de orden...")
        items_data = [
            {"orden": ordenes[0], "estudio": estudios[0], "monto_usd": Decimal("150.00")},
            {"orden": ordenes[0], "estudio": estudios[1], "monto_usd": Decimal("80.00")},
            {"orden": ordenes[1], "estudio": estudios[2], "monto_usd": Decimal("200.00")},
            {"orden": ordenes[2], "estudio": estudios[3], "monto_usd": Decimal("120.00")},
            {"orden": ordenes[3], "estudio": estudios[4], "monto_usd": Decimal("250.00")},
        ]

        items = []
        for data in items_data:
            if not ItemOrden.objects.filter(
                orden=data["orden"], estudio=data["estudio"]
            ).exists():
                item = ItemOrden.objects.create(**data)
                items.append(item)

        self.stdout.write(f"  Items de orden creados: {len(items)}")
        return items

    def _create_pagos(self, ordenes):
        """Crea pagos de prueba"""
        self.stdout.write("Creando pagos...")
        pagos = []

        # Pago para orden 1 (total 230 USD)
        pago1, _ = Pago.objects.get_or_create(
            orden=ordenes[0],
            monto_usd=Decimal("230.00"),
            defaults={"detalle": "Pago completo orden Clinica Santa Maria"},
        )
        pagos.append(pago1)

        # Pago parcial para orden 2 (total 200 USD, paga 100)
        pago2, _ = Pago.objects.get_or_create(
            orden=ordenes[1],
            monto_usd=Decimal("100.00"),
            defaults={"detalle": "Anticipo Laboratorio Valencia"},
        )
        pagos.append(pago2)

        # Pago para orden 4 (total 250 USD)
        pago3, _ = Pago.objects.get_or_create(
            orden=ordenes[3],
            monto_usd=Decimal("250.00"),
            defaults={"detalle": "Pago completo paciente particular"},
        )
        pagos.append(pago3)

        self.stdout.write(f"  Pagos creados: {len(pagos)}")
        return pagos

    def _create_facturas(self, ordenes, archivos):
        """Crea facturas de prueba"""
        self.stdout.write("Creando facturas...")
        facturas = []

        # Factura para orden 1
        if not Factura.objects.filter(orden=ordenes[0]).exists():
            factura1 = Factura.objects.create(
                orden=ordenes[0],
                n_factura=1001,
                monto=Decimal("230.00"),
                s3_file=archivos[0],
            )
            facturas.append(factura1)

        # Factura para orden 4
        if not Factura.objects.filter(orden=ordenes[3]).exists():
            factura2 = Factura.objects.create(
                orden=ordenes[3],
                n_factura=1002,
                monto=Decimal("250.00"),
                s3_file=archivos[3],
            )
            facturas.append(factura2)

        self.stdout.write(f"  Facturas creadas: {len(facturas)}")
        return facturas

    def _create_recibos(self, ordenes, archivos):
        """Crea recibos de prueba"""
        self.stdout.write("Creando recibos...")
        recibos = []

        # Recibo para orden 1
        if not Recibo.objects.filter(orden=ordenes[0]).exists():
            recibo1 = Recibo.objects.create(
                orden=ordenes[0],
                s3_file=archivos[7],
            )
            recibos.append(recibo1)

        # Recibo para orden 2
        if not Recibo.objects.filter(orden=ordenes[1]).exists():
            recibo2 = Recibo.objects.create(
                orden=ordenes[1],
                s3_file=archivos[8],
            )
            recibos.append(recibo2)

        self.stdout.write(f"  Recibos creados: {len(recibos)}")
        return recibos

    def _create_notas(self, ordenes, archivos):
        """Crea notas de credito y debito de prueba"""
        self.stdout.write("Creando notas de credito y debito...")

        # Nota de debito para orden 3
        if not NotasDebito.objects.filter(orden=ordenes[2]).exists():
            NotasDebito.objects.create(
                orden=ordenes[2],
                n_notadebito=5001,
                n_factura=0,
                monto=Decimal("50.00"),
                s3_file=archivos[9],
            )

        # Nota de credito para orden 2
        if not NotasCredito.objects.filter(orden=ordenes[1]).exists():
            NotasCredito.objects.create(
                orden=ordenes[1],
                n_factura=0,
                monto=Decimal("20.00"),
                s3_file=archivos[10],
            )

        self.stdout.write("  Notas creadas: 1 debito, 1 credito")

    def _create_transacciones(self, clientes):
        """Crea transacciones de prueba"""
        self.stdout.write("Creando transacciones...")
        transacciones_data = [
            {
                "rifci": clientes[0].ci_rif,
                "cliente": clientes[0].razon_social,
                "tipo": "FACTURA",
                "n_control": 10001,
                "n_documento": 1001,
                "monto": Decimal("230.00"),
                "monto_impuesto": Decimal("36.80"),
            },
            {
                "rifci": clientes[3].ci_rif,
                "cliente": clientes[3].razon_social,
                "tipo": "FACTURA",
                "n_control": 10002,
                "n_documento": 1002,
                "monto": Decimal("250.00"),
                "monto_impuesto": Decimal("40.00"),
            },
            {
                "rifci": clientes[1].ci_rif,
                "cliente": clientes[1].razon_social,
                "tipo": "NOTA_CREDITO",
                "n_control": 20001,
                "n_documento": 0,
                "monto": Decimal("20.00"),
                "monto_impuesto": Decimal("3.20"),
            },
        ]

        transacciones = []
        for data in transacciones_data:
            if not Transaccion.objects.filter(n_control=data["n_control"]).exists():
                transaccion = Transaccion.objects.create(**data)
                transacciones.append(transaccion)

        self.stdout.write(f"  Transacciones creadas: {len(transacciones)}")

    def _create_offsets(self):
        """Crea offsets de prueba"""
        self.stdout.write("Creando offsets...")
        FacturaOffset.objects.get_or_create(factura_offset=1000)
        self.stdout.write("  FacturaOffset creado: 1000")

    def _print_summary(self):
        """Imprime resumen de datos creados"""
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write("RESUMEN DE DATOS CREADOS")
        self.stdout.write("=" * 50)
        self.stdout.write(f"  Usuarios: {User.objects.count()}")
        self.stdout.write(f"  Grupos: {Group.objects.count()}")
        self.stdout.write(f"  Pacientes: {Paciente.objects.count()}")
        self.stdout.write(f"  Medicos: {MedicoTratante.objects.count()}")
        self.stdout.write(f"  Patologos: {Patologo.objects.count()}")
        self.stdout.write(f"  Estudios: {Estudio.objects.count()}")
        self.stdout.write(f"  Muestras: {Muestra.objects.count()}")
        self.stdout.write(f"  FasesMuestra: {FaseMuestra.objects.count()}")
        self.stdout.write(f"  Informes: {Informe.objects.count()}")
        self.stdout.write(f"  Resultados IHQ: {ResultadoInmunostoquimica.objects.count()}")
        self.stdout.write(f"  Clientes: {Cliente.objects.count()}")
        self.stdout.write(f"  Ordenes: {Orden.objects.count()}")
        self.stdout.write(f"  Items Orden: {ItemOrden.objects.count()}")
        self.stdout.write(f"  Pagos: {Pago.objects.count()}")
        self.stdout.write(f"  Facturas: {Factura.objects.count()}")
        self.stdout.write(f"  Recibos: {Recibo.objects.count()}")
        self.stdout.write(f"  Notas Credito: {NotasCredito.objects.count()}")
        self.stdout.write(f"  Notas Debito: {NotasDebito.objects.count()}")
        self.stdout.write(f"  Transacciones: {Transaccion.objects.count()}")
        self.stdout.write(f"  Archivos: {UploadedFile.objects.count()}")
        self.stdout.write(f"  Cambio USD/BS: {CambioUSDBS.objects.count()}")
        self.stdout.write("=" * 50)
