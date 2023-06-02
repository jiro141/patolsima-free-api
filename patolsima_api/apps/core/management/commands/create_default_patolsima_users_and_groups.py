from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand, CommandError

from patolsima_api.apps.core.models import *
from patolsima_api.apps.facturacion.models import *
from patolsima_api.apps.uploaded_file_management.models import UploadedFile


class Command(BaseCommand):
    help = "Generates the groups for Patolsima users on first run."

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # Core content types
        estudio_content_type = ContentType.objects.get_for_model(Estudio)
        medicotratante_content_type = ContentType.objects.get_for_model(MedicoTratante)
        paciente_content_type = ContentType.objects.get_for_model(Paciente)
        muestra_content_type = ContentType.objects.get_for_model(Muestra)
        fasemuestra_content_type = ContentType.objects.get_for_model(FaseMuestra)
        patologo_content_type = ContentType.objects.get_for_model(Patologo)
        informe_content_type = ContentType.objects.get_for_model(Informe)
        resultadoinmunostoquimica_content_type = ContentType.objects.get_for_model(
            ResultadoInmunostoquimica
        )

        # Facturacion content types
        cliente_content_type = ContentType.objects.get_for_model(Cliente)
        orden_content_type = ContentType.objects.get_for_model(Orden)
        itemorden_content_type = ContentType.objects.get_for_model(ItemOrden)
        pago_content_type = ContentType.objects.get_for_model(Pago)
        factura_content_type = ContentType.objects.get_for_model(Factura)
        recibo_content_type = ContentType.objects.get_for_model(Recibo)
        notapago_content_type = ContentType.objects.get_for_model(NotaPago)
        cambiousdbs_content_type = ContentType.objects.get_for_model(CambioUSDBS)

        # Uploaded files content types
        uploadedfile_content_type = ContentType.objects.get_for_model(UploadedFile)

        add_estudio_permission = Permission.objects.get(
            codename="add_estudio", content_type=estudio_content_type
        )
        change_estudio_permission = Permission.objects.get(
            codename="change_estudio", content_type=estudio_content_type
        )
        delete_estudio_permission = Permission.objects.get(
            codename="delete_estudio", content_type=estudio_content_type
        )
        view_estudio_permission = Permission.objects.get(
            codename="view_estudio", content_type=estudio_content_type
        )

        add_medicotratante_permission = Permission.objects.get(
            codename="add_medicotratante", content_type=medicotratante_content_type
        )
        change_medicotratante_permission = Permission.objects.get(
            codename="change_medicotratante", content_type=medicotratante_content_type
        )
        delete_medicotratante_permission = Permission.objects.get(
            codename="delete_medicotratante", content_type=medicotratante_content_type
        )
        view_medicotratante_permission = Permission.objects.get(
            codename="view_medicotratante", content_type=medicotratante_content_type
        )

        add_paciente_permission = Permission.objects.get(
            codename="add_paciente", content_type=paciente_content_type
        )
        change_paciente_permission = Permission.objects.get(
            codename="change_paciente", content_type=paciente_content_type
        )
        delete_paciente_permission = Permission.objects.get(
            codename="delete_paciente", content_type=paciente_content_type
        )
        view_paciente_permission = Permission.objects.get(
            codename="view_paciente", content_type=paciente_content_type
        )

        add_informe_permission = Permission.objects.get(
            codename="add_informe", content_type=informe_content_type
        )
        change_informe_permission = Permission.objects.get(
            codename="change_informe", content_type=informe_content_type
        )
        delete_informe_permission = Permission.objects.get(
            codename="delete_informe", content_type=informe_content_type
        )
        view_informe_permission = Permission.objects.get(
            codename="view_informe", content_type=informe_content_type
        )

        add_patologo_permission = Permission.objects.get(
            codename="add_patologo", content_type=patologo_content_type
        )
        change_patologo_permission = Permission.objects.get(
            codename="change_patologo", content_type=patologo_content_type
        )
        delete_patologo_permission = Permission.objects.get(
            codename="delete_patologo", content_type=patologo_content_type
        )
        view_patologo_permission = Permission.objects.get(
            codename="view_patologo", content_type=patologo_content_type
        )

        add_muestra_permission = Permission.objects.get(
            codename="add_muestra", content_type=muestra_content_type
        )
        change_muestra_permission = Permission.objects.get(
            codename="change_muestra", content_type=muestra_content_type
        )
        delete_muestra_permission = Permission.objects.get(
            codename="delete_muestra", content_type=muestra_content_type
        )
        view_muestra_permission = Permission.objects.get(
            codename="view_muestra", content_type=muestra_content_type
        )

        add_fasemuestra_permission = Permission.objects.get(
            codename="add_fasemuestra", content_type=fasemuestra_content_type
        )
        change_fasemuestra_permission = Permission.objects.get(
            codename="change_fasemuestra", content_type=fasemuestra_content_type
        )
        delete_fasemuestra_permission = Permission.objects.get(
            codename="delete_fasemuestra", content_type=fasemuestra_content_type
        )
        view_fasemuestra_permission = Permission.objects.get(
            codename="view_fasemuestra", content_type=fasemuestra_content_type
        )

        add_resultadoinmunostoquimica_permission = Permission.objects.get(
            codename="add_resultadoinmunostoquimica",
            content_type=resultadoinmunostoquimica_content_type,
        )
        change_resultadoinmunostoquimica_permission = Permission.objects.get(
            codename="change_resultadoinmunostoquimica",
            content_type=resultadoinmunostoquimica_content_type,
        )
        delete_resultadoinmunostoquimica_permission = Permission.objects.get(
            codename="delete_resultadoinmunostoquimica",
            content_type=resultadoinmunostoquimica_content_type,
        )
        view_resultadoinmunostoquimica_permission = Permission.objects.get(
            codename="view_resultadoinmunostoquimica",
            content_type=resultadoinmunostoquimica_content_type,
        )

        add_cambiousdbs_permission = Permission.objects.get(
            codename="add_cambiousdbs", content_type=cambiousdbs_content_type
        )
        change_cambiousdbs_permission = Permission.objects.get(
            codename="change_cambiousdbs", content_type=cambiousdbs_content_type
        )
        delete_cambiousdbs_permission = Permission.objects.get(
            codename="delete_cambiousdbs", content_type=cambiousdbs_content_type
        )
        view_cambiousdbs_permission = Permission.objects.get(
            codename="view_cambiousdbs", content_type=cambiousdbs_content_type
        )

        add_cliente_permission = Permission.objects.get(
            codename="add_cliente", content_type=cliente_content_type
        )
        change_cliente_permission = Permission.objects.get(
            codename="change_cliente", content_type=cliente_content_type
        )
        delete_cliente_permission = Permission.objects.get(
            codename="delete_cliente", content_type=cliente_content_type
        )
        view_cliente_permission = Permission.objects.get(
            codename="view_cliente", content_type=cliente_content_type
        )

        add_orden_permission = Permission.objects.get(
            codename="add_orden", content_type=orden_content_type
        )
        change_orden_permission = Permission.objects.get(
            codename="change_orden", content_type=orden_content_type
        )
        delete_orden_permission = Permission.objects.get(
            codename="delete_orden", content_type=orden_content_type
        )
        view_orden_permission = Permission.objects.get(
            codename="view_orden", content_type=orden_content_type
        )

        add_recibo_permission = Permission.objects.get(
            codename="add_recibo", content_type=recibo_content_type
        )
        change_recibo_permission = Permission.objects.get(
            codename="change_recibo", content_type=recibo_content_type
        )
        delete_recibo_permission = Permission.objects.get(
            codename="delete_recibo", content_type=recibo_content_type
        )
        view_recibo_permission = Permission.objects.get(
            codename="view_recibo", content_type=recibo_content_type
        )

        add_pago_permission = Permission.objects.get(
            codename="add_pago", content_type=pago_content_type
        )
        change_pago_permission = Permission.objects.get(
            codename="change_pago", content_type=pago_content_type
        )
        delete_pago_permission = Permission.objects.get(
            codename="delete_pago", content_type=pago_content_type
        )
        view_pago_permission = Permission.objects.get(
            codename="view_pago", content_type=pago_content_type
        )

        add_notapago_permission = Permission.objects.get(
            codename="add_notapago", content_type=notapago_content_type
        )
        change_notapago_permission = Permission.objects.get(
            codename="change_notapago", content_type=notapago_content_type
        )
        delete_notapago_permission = Permission.objects.get(
            codename="delete_notapago", content_type=notapago_content_type
        )
        view_notapago_permission = Permission.objects.get(
            codename="view_notapago", content_type=notapago_content_type
        )

        add_itemorden_permission = Permission.objects.get(
            codename="add_itemorden", content_type=itemorden_content_type
        )
        change_itemorden_permission = Permission.objects.get(
            codename="change_itemorden", content_type=itemorden_content_type
        )
        delete_itemorden_permission = Permission.objects.get(
            codename="delete_itemorden", content_type=itemorden_content_type
        )
        view_itemorden_permission = Permission.objects.get(
            codename="view_itemorden", content_type=itemorden_content_type
        )

        add_factura_permission = Permission.objects.get(
            codename="add_factura", content_type=factura_content_type
        )
        change_factura_permission = Permission.objects.get(
            codename="change_factura", content_type=factura_content_type
        )
        delete_factura_permission = Permission.objects.get(
            codename="delete_factura", content_type=factura_content_type
        )
        view_factura_permission = Permission.objects.get(
            codename="view_factura", content_type=factura_content_type
        )

        add_uploadedfile_permission = Permission.objects.get(
            codename="add_uploadedfile", content_type=uploadedfile_content_type
        )
        change_uploadedfile_permission = Permission.objects.get(
            codename="change_uploadedfile", content_type=uploadedfile_content_type
        )
        delete_uploadedfile_permission = Permission.objects.get(
            codename="delete_uploadedfile", content_type=uploadedfile_content_type
        )
        view_uploadedfile_permission = Permission.objects.get(
            codename="view_uploadedfile", content_type=uploadedfile_content_type
        )

        administracion, created = Group.objects.get_or_create(
            name="administracion", defaults={}
        )
        patologo, created = Group.objects.get_or_create(name="patologo", defaults={})

        administracion.permissions.add(
            # Core
            add_estudio_permission,
            change_estudio_permission,
            delete_estudio_permission,
            view_estudio_permission,
            add_medicotratante_permission,
            change_medicotratante_permission,
            delete_medicotratante_permission,
            view_medicotratante_permission,
            add_paciente_permission,
            change_paciente_permission,
            delete_paciente_permission,
            view_paciente_permission,
            add_informe_permission,
            change_informe_permission,
            delete_informe_permission,
            view_informe_permission,
            add_patologo_permission,
            change_patologo_permission,
            delete_patologo_permission,
            view_patologo_permission,
            add_muestra_permission,
            change_muestra_permission,
            delete_muestra_permission,
            view_muestra_permission,
            add_fasemuestra_permission,
            change_fasemuestra_permission,
            delete_fasemuestra_permission,
            view_fasemuestra_permission,
            add_resultadoinmunostoquimica_permission,
            change_resultadoinmunostoquimica_permission,
            delete_resultadoinmunostoquimica_permission,
            view_resultadoinmunostoquimica_permission,
            # Uploaded files
            add_uploadedfile_permission,
            change_uploadedfile_permission,
            delete_uploadedfile_permission,
            view_uploadedfile_permission,
            # Facturacion
            add_cambiousdbs_permission,
            change_cambiousdbs_permission,
            delete_cambiousdbs_permission,
            view_cambiousdbs_permission,
            add_cliente_permission,
            change_cliente_permission,
            delete_cliente_permission,
            view_cliente_permission,
            add_orden_permission,
            change_orden_permission,
            delete_orden_permission,
            view_orden_permission,
            add_recibo_permission,
            change_recibo_permission,
            delete_recibo_permission,
            view_recibo_permission,
            add_pago_permission,
            change_pago_permission,
            delete_pago_permission,
            view_pago_permission,
            add_notapago_permission,
            change_notapago_permission,
            delete_notapago_permission,
            view_notapago_permission,
            add_itemorden_permission,
            change_itemorden_permission,
            delete_itemorden_permission,
            view_itemorden_permission,
            add_factura_permission,
            change_factura_permission,
            delete_factura_permission,
            view_factura_permission,
        )

        patologo.permissions.add(
            # Core
            view_estudio_permission,
            view_medicotratante_permission,
            view_paciente_permission,
            view_informe_permission,
            view_patologo_permission,
            view_muestra_permission,
            add_informe_permission,
            change_informe_permission,
            delete_informe_permission,
            add_fasemuestra_permission,
            change_fasemuestra_permission,
            delete_fasemuestra_permission,
            view_fasemuestra_permission,
            add_resultadoinmunostoquimica_permission,
            change_resultadoinmunostoquimica_permission,
            delete_resultadoinmunostoquimica_permission,
            view_resultadoinmunostoquimica_permission,
            # Uploaded files
            add_uploadedfile_permission,
            change_uploadedfile_permission,
            delete_uploadedfile_permission,
            view_uploadedfile_permission,
        )

        administracion.save()
        patologo.save()
