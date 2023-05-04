import time
from typing import Union
from patolsima_api.apps.facturacion.models import Orden, Factura, Recibo
from patolsima_api.apps.facturacion.utils.jinja import *
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


def render_recibo_factura(registro: Union[Factura, Recibo], tipo: str) -> str:
    filename = f"{tipo}_{registro.orden.id}_{int(time.time())}"
    context = {
        "cliente": registro.orden.cliente,
        "orden": registro.orden,
        "items_orden": registro.orden.items_orden.all().order_by(
            "estudio__tipo", "estudio__codigo"
        ),
        **registro.orden.balance,
        **registro.pdf_reder_context,
    }
    templates = RECIBO_TEMPLATES if tipo == "recibo" else FACTURA_TEMPLATES
    pdf_filename = render_pdf(
        context=context, templates=templates, destination=filename
    )
    return pdf_filename
