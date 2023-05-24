import time
from typing import Union
from patolsima_api.apps.facturacion.models import Orden, Factura, Recibo, NotaPago, Pago
from patolsima_api.apps.facturacion.utils.jinja_templates import *
from patolsima_api.utils.render_pdf import render_pdf


RECIBO_TEMPLATES = {
    "body": {"pre_render": True, "template_obj": recibo_body_template},
    "header": {"pre_render": True, "template_obj": recibo_header_template},
    "footer": {"pre_render": True, "template_obj": recibo_footer_template},
}

FACTURA_TEMPLATES = {
    "body": {"pre_render": True, "template_obj": recibo_body_template},
    "header": {"pre_render": True, "template_obj": recibo_header_template},
    "footer": {"pre_render": True, "template_obj": recibo_footer_template},
}

NOTA_DE_PAGO_TEMPLATES = {
    "body": {"pre_render": True, "template_obj": recibo_body_template},
    "header": {"pre_render": True, "template_obj": recibo_header_template},
    "footer": {"pre_render": True, "template_obj": recibo_footer_template},
}


def render_recibo_factura(registro: Union[Factura, Recibo], tipo: str) -> str:
    """
    This method takes a Factura/Recibo instance and renders its associated pdf.
    :param registro: Factura/Recibo instance. The Orden instance associated must be pagada=True.
    :return: the path of the PDF file in the filesystem
    """
    numero_documento = registro.id if tipo == "recibo" else registro.n_factura
    filename = f"{tipo}_{registro.orden.id}_{int(time.time())}"
    context = {
        "current_work_path_python": os.getcwd(),
        "cliente": registro.orden.cliente,
        "orden": registro.orden,
        "items_orden": registro.orden.items_orden.all().order_by(
            "estudio__tipo", "estudio__codigo"
        ),
        "pagos": registro.orden.pagos.all().order_by("created_at"),
        "tipo_documento": tipo.capitalize(),
        "numero_documento": numero_documento,
        "fecha_emision": registro.created_at.date().isoformat(),
        **registro.orden.balance,
        **registro.pdf_reder_context,
    }
    templates = RECIBO_TEMPLATES if tipo == "recibo" else FACTURA_TEMPLATES
    pdf_filename = render_pdf(
        context=context,
        templates=templates,
        destination=filename,
        extra_args={
            "wkhtmltopdf_options": {
                "--page-size": "A5",
                "--orientation": "Landscape",
                "--header-spacing": "5",
                "--footer-spacing": "5",
                "--margin-left": "50px",
                "--margin-right": "50px",
                "--margin-top": "150px",
                "--margin-bottom": "70px",
            }
        },
    )
    return pdf_filename


def render_nota_de_pago(nota_pago: NotaPago) -> str:
    """
    This method takes a NotaPago instance and renders its associated pdf.
    :param nota_pago: NotaPago instance linked to a processed payment.
    :return: the path of the PDF file in the filesystem
    """
    filename = f"nota_de_pago_{nota_pago.id}_{int(time.time())}"
    orden = nota_pago.pago.orden
    context = {
        "current_work_path_python": os.getcwd(),
        "cliente": orden.cliente,
        "orden": orden,
        "items_orden": orden.items_orden.all().order_by(
            "estudio__tipo", "estudio__codigo"
        ),
        "pagos": orden.pagos.all().order_by("created_at"),
        "tipo_documento": "Nota de Pago",
        "numero_documento": nota_pago.id,
        "fecha_emision": nota_pago.created_at.date().isoformat(),
        **orden.balance,
    }
    pdf_filename = render_pdf(
        context=context,
        templates=NOTA_DE_PAGO_TEMPLATES,
        destination=filename,
        extra_args={
            "wkhtmltopdf_options": {
                "--page-size": "A5",
                "--orientation": "Landscape",
                "--header-spacing": "5",
                "--footer-spacing": "5",
                "--margin-left": "50px",
                "--margin-right": "50px",
                "--margin-top": "150px",
                "--margin-bottom": "70px",
            }
        },
    )
    return pdf_filename
