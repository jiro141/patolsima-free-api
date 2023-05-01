from jinja2 import Environment, FileSystemLoader
import pdfkit


class Cliente:
    def __init__(self):
        self.razon_social = "Los bolletes CA"
        self.ci_rif = "V1092736"
        self.email = "asd@asd.asd"
        self.telefono_celular = "9187263"
        self.telefono_fijo = "1982763"


class Estudio:
    def __init__(self, codigo, tipo):
        self.codigo = codigo
        self.tipo = tipo


class ItemOrden:
    def __init__(self, estudio, monto_usd):
        self.monto_usd = monto_usd
        self.estudio = estudio


class Orden:
    def __init__(self):
        self.id = 125367
        self.items_orden = [
            ItemOrden(Estudio("aklsjdh1289736", "Inmunostoquimica"), 123.8),
            ItemOrden(Estudio("3486askjdf", "Biopsia"), 50.0),
        ]


environment = Environment(loader=FileSystemLoader("./"))
recibo_template = environment.get_template("body_recibo.html")
header_template = environment.get_template("header_recibo.html")
bodytext = recibo_template.render(
    cliente=Cliente(), orden=Orden(), total_usd=1928367, total_bs=912367
)
with open("temp_header.html", "w") as f:
    f.writelines(header_template.render(num_recibo=1))

config = pdfkit.configuration(wkhtmltopdf="/usr/local/bin/wkhtmltopdf")
options = {
    "--header-html": "temp_header.html",
    "--footer-html": "footer_recibo.html",
}
pdfkit.from_string(
    bodytext,
    "pdf_generated.pdf",
    configuration=config,
    options=options,
)
