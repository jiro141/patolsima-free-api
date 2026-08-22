#!/usr/bin/env python
"""
Script para poblar la base de datos con datos de prueba.
Uso: python seed_database.py

Este script es alternativo al management command.
Puedes ejecutarlo directamente o usar:
  python manage.py seed_all_data
"""
import os
import sys
import django
from datetime import date
from decimal import Decimal

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "patolsima_api.settings")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Cambiar al directorio del proyecto
os.chdir(os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.contrib.auth.models import User, Group
from django.db import transaction

from patolsima_api.apps.core.models import (
    Paciente,
    MedicoTratante,
    Patologo,
    Estudio,
    Muestra,
    Informe,
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


@transaction.atomic
def seed():
    print("=" * 50)
    print("POBLANDO BASE DE DATOS CON DATOS DE PRUEBA")
    print("=" * 50)

    # 1. Usuarios y grupos
    print("\n1. Creando usuarios y grupos...")
    grupos = {}
    for nombre in ["admin", "patologo", "recepcion", "facturacion"]:
        grupos[nombre], _ = Group.objects.get_or_create(name=nombre)

    if not User.objects.filter(username="admin").exists():
        admin = User.objects.create_superuser(
            username="admin", email="admin@patolsima.com",
            password="admin123", first_name="Admin", last_name="Sistema"
        )
        admin.groups.add(grupos["admin"])

    if not User.objects.filter(username="dr_martinez").exists():
        user_pat = User.objects.create_user(
            username="dr_martinez", email="martinez@patolsima.com",
            password="patologo123", first_name="Carlos", last_name="Martinez"
        )
        user_pat.groups.add(grupos["patologo"])

    for username, email, pwd, first, last, group in [
        ("recepcion1", "recepcion@patolsima.com", "recepcion123", "Maria", "Gonzalez", "recepcion"),
        ("facturacion1", "facturacion@patolsima.com", "facturacion123", "Pedro", "Lopez", "facturacion"),
    ]:
        if not User.objects.filter(username=username).exists():
            u = User.objects.create_user(username=username, email=email, password=pwd, first_name=first, last_name=last)
            u.groups.add(grupos[group])

    print("   Usuarios: admin, dr_martinez, recepcion1, facturacion1")

    # 2. Archivos
    print("\n2. Creando archivos...")
    archivos = []
    for nombre, tipo, size in [
        ("informe.pdf", "application/pdf", 1024),
        ("imagen.jpg", "image/jpeg", 2048),
        ("resultado.pdf", "application/pdf", 512),
        ("biopsia.png", "image/png", 3072),
        ("doc.docx", "application/msword", 256),
        ("factura1.pdf", "application/pdf", 1024),
        ("factura2.pdf", "application/pdf", 1024),
        ("recibo1.pdf", "application/pdf", 512),
        ("recibo2.pdf", "application/pdf", 512),
        ("nota1.pdf", "application/pdf", 256),
        ("nota2.pdf", "application/pdf", 256),
    ]:
        a, _ = UploadedFile.objects.get_or_create(file_name=nombre, defaults={"size": size, "content_type": tipo})
        archivos.append(a)
    print(f"   Archivos: {len(archivos)}")

    # 3. Tipo de cambio
    print("\n3. Creando tipo de cambio...")
    CambioUSDBS.objects.get_or_create(bs_e=Decimal("36.50"))
    print("   USD/BS: 36.50")

    # 4. Pacientes
    print("\n4. Creando pacientes...")
    pacientes = []
    for ci, nom, ape, fecha, sexo, email, tel in [
        ("V-12345678", "Juan Carlos", "Perez Rodriguez", date(1985, 3, 15), "MASCULINO", "juan@email.com", "+584121234567"),
        ("V-23456789", "Maria Fernanda", "Lopez Garcia", date(1990, 7, 22), "FEMENINO", "maria@email.com", "+584149876543"),
        ("V-34567890", "Pedro Antonio", "Sanchez Martinez", date(1978, 11, 5), "MASCULINO", "pedro@email.com", "+584245551234"),
        ("V-45678901", "Ana Patricia", "Rodriguez Fernandez", date(1995, 1, 30), "FEMENINO", "ana@email.com", "+584127778899"),
        ("V-56789012", "Luis Eduardo", "Gomez Hernandez", date(1982, 6, 18), "MASCULINO", "luis@email.com", "+584163334455"),
    ]:
        p, _ = Paciente.objects.get_or_create(ci=ci, defaults={"nombres": nom, "apellidos": ape, "fecha_nacimiento": fecha, "sexo": sexo, "email": email, "telefono_celular": tel})
        pacientes.append(p)
    print(f"   Pacientes: {len(pacientes)}")

    # 5. Medicos
    print("\n5. Creando medicos...")
    medicos = []
    for ci, nom, ape, ncomed, esp, email in [
        ("V-11111111", "Roberto", "Garcia Lopez", "MED-001", "Cirugia General", "roberto@clinica.com"),
        ("V-22222222", "Carmen", "Torres Ruiz", "MED-002", "Ginecologia", "carmen@clinica.com"),
        ("V-33333333", "Fernando", "Diaz Moreno", "MED-003", "Dermatologia", "fernando@clinica.com"),
        ("V-44444444", "Isabel", "Morales Castro", "MED-004", "Oncologia", "isabel@clinica.com"),
    ]:
        m, _ = MedicoTratante.objects.get_or_create(ci=ci, ncomed=ncomed, defaults={"nombres": nom, "apellidos": ape, "especialidad": esp, "email": email})
        medicos.append(m)
    print(f"   Medicos: {len(medicos)}")

    # 6. Patologos
    print("\n6. Creando patologos...")
    user_pat = User.objects.get(username="dr_martinez")
    patologos = []
    for ncomed, nom, ape, user in [
        ("PAT-001", "Carlos", "Martinez", user_pat),
        ("PAT-002", "Laura", "Fernandez", None),
    ]:
        p, _ = Patologo.objects.get_or_create(ncomed=ncomed, defaults={"nombres": nom, "apellidos": ape, "user": user})
        patologos.append(p)
    print(f"   Patologos: {len(patologos)}")

    # 7. Estudios
    print("\n7. Creando estudios...")
    estudios = []
    for pac, med, pat, notas, urg, tipo in [
        (pacientes[0], medicos[0], patologos[0], "Biopsia cutanea", True, "BIOPSIA"),
        (pacientes[1], medicos[1], patologos[0], "Citologia ginecologica", False, "CITOLOGIA_GINECOLOGICA"),
        (pacientes[2], medicos[2], patologos[1], "Biopsia melanoma", True, "BIOPSIA"),
        (pacientes[3], medicos[3], patologos[0], "Citologia especial", False, "CITOLOGIA_ESPECIAL"),
        (pacientes[4], medicos[0], patologos[1], "Inmunohistoquimica", False, "INMUNOHISTOQUIMICA"),
    ]:
        e, _ = Estudio.objects.get_or_create(paciente=pac, notas=notas, defaults={"medico_tratante": med, "patologo": pat, "urgente": urg, "tipo": tipo})
        estudios.append(e)
    print(f"   Estudios: {len(estudios)}")

    # 8. Muestras
    print("\n8. Creando muestras...")
    muestras = []
    for est, tipo, desc, estado in [
        (estudios[0], "Biopsia cutanea", "Fragmento 2x1 cm", "RECIBIDA"),
        (estudios[1], "Citologia cervico-vaginal", "Muestra de exocervix", "COLORACION"),
        (estudios[2], "Biopsia de piel", "Lesion 0.5 cm", "DESHIDRATACION"),
        (estudios[3], "Citologia especial", "Liquido ascitico", "INCLUSION_EN_PARAFINA"),
        (estudios[4], "Tejido para IHQ", "Bloque fijado", "CORTE_MICROTOMO"),
        (estudios[0], "Segunda biopsia", "Fragmento adicional", "RECIBIDA"),
    ]:
        if not Muestra.objects.filter(estudio=est, tipo_de_muestra=tipo).exists():
            m = Muestra.objects.create(estudio=est, tipo_de_muestra=tipo, descripcion=desc, estado=estado)
            muestras.append(m)
    print(f"   Muestras: {len(muestras)}")

    # 9. Informes
    print("\n9. Creando informes...")
    informes = []
    for est, macro, micro, recib, diag, notas, comp, apr in [
        (estudios[0], "Tejido cutaneo variable", "Melanocitos atipicos", "Biopsia en formol", "Melanoma cutaneo", "Margen amplio", True, True),
        (estudios[1], "Muestra liquida", "Celiteglandular", "Citologia base liquida", "Negativa para SIL", "Control 12 meses", True, False),
        (estudios[2], "Lesion pigmentada 5mm", "Melanocitos atipicos", "Biopsia punch 4mm", "Nevo displasico vs Melanoma", "Estudio adicional", False, False),
    ]:
        if not Informe.objects.filter(estudio=est).exists():
            i = Informe.objects.create(estudio=est, descripcion_macroscopica=macro, descripcion_microscopica=micro, muestra_recibida=recib, diagnostico=diag, notas=notas, completado=comp, aprobado=apr)
            informes.append(i)
    print(f"   Informes: {len(informes)}")

    # 10. Clientes
    print("\n10. Creando clientes...")
    clientes = []
    for rif, razon, email, tel in [
        ("J-40123456-7", "Clinica Santa Maria C.A.", "clinica@santamaria.com", "+584125551234"),
        ("J-30987654-3", "Laboratorio Clinico Valencia", "lab@labvalencia.com", "+584146667788"),
        ("J-29876543-2", "Centro Medico Maracay", "centro@medimaracay.com", "+584248889900"),
        ("V-12345678", "Paciente Particular", "juan@email.com", "+584121234567"),
    ]:
        c, _ = Cliente.objects.get_or_create(ci_rif=rif, defaults={"razon_social": razon, "email": email, "telefono_celular": tel})
        clientes.append(c)
    print(f"   Clientes: {len(clientes)}")

    # 11. Ordenes
    print("\n11. Creando ordenes...")
    ordenes = []
    for cli, conf in [(clientes[0], True), (clientes[1], True), (clientes[2], False), (clientes[3], True)]:
        o, _ = Orden.objects.get_or_create(cliente=cli, confirmada=conf)
        ordenes.append(o)
    print(f"   Ordenes: {len(ordenes)}")

    # 12. Items
    print("\n12. Creando items de orden...")
    items_data = [
        (ordenes[0], estudios[0], Decimal("150.00")),
        (ordenes[0], estudios[1], Decimal("80.00")),
        (ordenes[1], estudios[2], Decimal("200.00")),
        (ordenes[2], estudios[3], Decimal("120.00")),
        (ordenes[3], estudios[4], Decimal("250.00")),
    ]
    items = []
    for orden, estudio, monto in items_data:
        if not ItemOrden.objects.filter(orden=orden, estudio=estudio).exists():
            i = ItemOrden.objects.create(orden=orden, estudio=estudio, monto_usd=monto)
            items.append(i)
    print(f"   Items: {len(items)}")

    # 13. Pagos
    print("\n13. Creando pagos...")
    pagos_data = [
        (ordenes[0], Decimal("230.00"), "Pago completo"),
        (ordenes[1], Decimal("100.00"), "Anticipo"),
        (ordenes[3], Decimal("250.00"), "Pago completo"),
    ]
    for orden, monto, detalle in pagos_data:
        Pago.objects.get_or_create(orden=orden, monto_usd=monto, defaults={"detalle": detalle})
    print(f"   Pagos: {len(pagos_data)}")

    # 14. Facturas
    print("\n14. Creando facturas...")
    if not Factura.objects.filter(orden=ordenes[0]).exists():
        Factura.objects.create(orden=ordenes[0], n_factura=1001, monto=Decimal("230.00"), s3_file=archivos[5])
    if not Factura.objects.filter(orden=ordenes[3]).exists():
        Factura.objects.create(orden=ordenes[3], n_factura=1002, monto=Decimal("250.00"), s3_file=archivos[6])
    print("   Facturas: 2")

    # 15. Recibos
    print("\n15. Creando recibos...")
    if not Recibo.objects.filter(orden=ordenes[0]).exists():
        Recibo.objects.create(orden=ordenes[0], s3_file=archivos[7])
    if not Recibo.objects.filter(orden=ordenes[1]).exists():
        Recibo.objects.create(orden=ordenes[1], s3_file=archivos[8])
    print("   Recibos: 2")

    # 16. Notas
    print("\n16. Creando notas...")
    if not NotasDebito.objects.filter(orden=ordenes[2]).exists():
        NotasDebito.objects.create(orden=ordenes[2], n_notadebito=5001, monto=Decimal("50.00"), s3_file=archivos[9])
    if not NotasCredito.objects.filter(orden=ordenes[1]).exists():
        NotasCredito.objects.create(orden=ordenes[1], monto=Decimal("20.00"), s3_file=archivos[10])
    print("   Notas: 1 debito, 1 credito")

    # 17. Transacciones
    print("\n17. Creando transacciones...")
    for rif, cli, tipo, ctrl, doc, monto, imp in [
        ("J-40123456-7", "Clinica Santa Maria", "FACTURA", 10001, 1001, Decimal("230.00"), Decimal("36.80")),
        ("V-12345678", "Paciente Particular", "FACTURA", 10002, 1002, Decimal("250.00"), Decimal("40.00")),
        ("J-30987654-3", "Laboratorio Valencia", "NOTA_CREDITO", 20001, 0, Decimal("20.00"), Decimal("3.20")),
    ]:
        if not Transaccion.objects.filter(n_control=ctrl).exists():
            Transaccion.objects.create(rifci=rif, cliente=cli, tipo=tipo, n_control=ctrl, n_documento=doc, monto=monto, monto_impuesto=imp)
    print("   Transacciones: 3")

    # 18. Offset
    print("\n18. Creando offsets...")
    FacturaOffset.objects.get_or_create(factura_offset=1000)
    print("   FacturaOffset: 1000")

    # Resumen
    print("\n" + "=" * 50)
    print("RESUMEN FINAL")
    print("=" * 50)
    print(f"  Pacientes: {Paciente.objects.count()}")
    print(f"  Medicos: {MedicoTratante.objects.count()}")
    print(f"  Patologos: {Patologo.objects.count()}")
    print(f"  Estudios: {Estudio.objects.count()}")
    print(f"  Muestras: {Muestra.objects.count()}")
    print(f"  Informes: {Informe.objects.count()}")
    print(f"  Clientes: {Cliente.objects.count()}")
    print(f"  Ordenes: {Orden.objects.count()}")
    print(f"  Items: {ItemOrden.objects.count()}")
    print(f"  Pagos: {Pago.objects.count()}")
    print(f"  Facturas: {Factura.objects.count()}")
    print(f"  Recibos: {Recibo.objects.count()}")
    print(f"  Transacciones: {Transaccion.objects.count()}")
    print("=" * 50)
    print("DATOS DE PRUEBA CREADOS EXITOSAMENTE!")


if __name__ == "__main__":
    seed()
