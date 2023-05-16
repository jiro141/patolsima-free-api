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
    "body": {
        "template_obj": nota_de_pago_body_template,
        "pre_render": True,
    }
}


def render_recibo_factura(registro: Union[Factura, Recibo], tipo: str) -> str:
    """
    This method takes a Factura/Recibo instance and renders its associated pdf.
    :param registro: Factura/Recibo instance. The Orden instance associated must be pagada=True.
    :return: the path of the PDF file in the filesystem
    """
    filename = f"{tipo}_{registro.orden.id}_{int(time.time())}"
    context = {
        "current_work_path_python": os.getcwd(),
        "cliente": registro.orden.cliente,
        "orden": registro.orden,
        "items_orden": registro.orden.items_orden.all().order_by(
            "estudio__tipo", "estudio__codigo"
        ),
        "pagos": registro.orden.pagos.all().order_by("created_at"),
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
                "--footer-left": "[page]/[topage]",
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
    return render_pdf(
        context={"nota_de_pago": nota_pago, "pago": nota_pago.pago},
        templates=NOTA_DE_PAGO_TEMPLATES,
        destination=filename,
    )
