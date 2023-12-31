import os
from jinja2 import Environment, FileSystemLoader

core_templates_environment = Environment(
    loader=FileSystemLoader(
        f"{os.getcwd()}/patolsima_api/apps/core/utils/pdf_templates/"
    )
)
informe_body_template = core_templates_environment.get_template("informe_body.html")
informe_footer_template = core_templates_environment.get_template("informe_footer.html")
informe_header_template = core_templates_environment.get_template("informe_header.html")
