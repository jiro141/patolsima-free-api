import os
from jinja2 import Environment, FileSystemLoader

facturacion_environment = Environment(
    loader=FileSystemLoader(
        f"{os.getcwd()}/patolsima_api/apps/facturacion/utils/pdf_templates/"
    )
)
recibo_body_template = facturacion_environment.get_template("body_recibo.html")
recibo_header_template = facturacion_environment.get_template("header_recibo.html")
recibo_footer_template = facturacion_environment.get_template("footer_recibo.html")

nota_de_pago_body_template = facturacion_environment.get_template(
    "nota_de_pago_body.html"
)
