import pdfkit
import os
import contextlib
from typing import Dict, Any
from django.conf import settings


def render_pdf(
    context: Dict[str, Any],
    templates: Dict[str, dict],
    destination: str,
    extra_args: Dict[str, Any] = None,
) -> str:
    """
    Renders a PDF and returns the path of the file generated.
    :param context: All the variables that can be used to  render the templates.
    :param templates: A dictionary that contains the templates. The structure of the dict is {
    template_name: {source: X, pre_render: Y, template_obj: Z}}. "source" means the HTML to take. If a template needs
    to be rendered then the Jinja template obj must be stored in "template_ob" and the "pre_render" flag must be
    True.
    :param destination: file name used to render the PDF
    :param extra_args: A dictionary that contains options to WKHTMLTOPDF and other things.
    :return: path to the file generated.
    """
    if not extra_args:
        extra_args = {}

    for t_key, t_config in templates.items():
        if t_config.get("pre_render"):
            temp_filename = f"{settings.PDFKIT_RENDER_PATH}/{destination}_{t_key}.html"
            with open(temp_filename, "w") as temp_file:
                temp_file.writelines(t_config["template_obj"].render(**context))
            t_config["source"] = temp_filename

    wkhtmltopdf_options = {**(extra_args.pop("wkhtmltopdf_options", {}))}

    if "header" in templates:
        c = templates.pop("header")
        wkhtmltopdf_options["--header-html"] = c["source"]
    if "footer" in templates:
        c = templates.pop("footer")
        wkhtmltopdf_options["--footer-html"] = c["source"]

    output_filename = f"{settings.PDFKIT_RENDER_PATH}/{destination}.pdf"

    pdfkit.from_file(
        [conf["source"] for t, conf in templates.items()],
        output_filename,
        configuration=settings.PDFKIT_CONFIGURATION,
        options=wkhtmltopdf_options,
    )

    # Deletion of the temporal files
    for template_obj in templates.values():
        with contextlib.suppress(OSError):
            os.remove(template_obj["source"])

    return output_filename
