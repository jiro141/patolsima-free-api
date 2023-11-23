import pdfkit
import os
import contextlib
from typing import Dict, Any
from django.conf import settings


def _remove_temporal_templates(templates: Dict[str, dict]):
    for template_obj in templates.values():
        with contextlib.suppress(OSError):
            os.remove(template_obj["source"])


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

    wkhtmltopdf_options = {
        "enable-local-file-access": None,
        **(extra_args.pop("wkhtmltopdf_options", {})),
    }

    if "header" in templates:
        wkhtmltopdf_options["--header-html"] = templates["header"]["source"]
    if "footer" in templates:
        wkhtmltopdf_options["--footer-html"] = templates["footer"]["source"]

    if "body_template" in templates:
        templates["body_template_duplicate"] = templates["body_template"].copy()
        templates["body_template_duplicate"]["source"] += templates["body_template"]["source"]

    output_filename = f"{settings.PDFKIT_RENDER_PATH}/{destination}.pdf"
    pdf_body_pages = [
        conf["source"] for t, conf in templates.items() if t not in ["footer", "header"]
    ]

    pdfkit.from_file(
        pdf_body_pages,
        output_filename,
        configuration=settings.PDFKIT_CONFIGURATION,
        options=wkhtmltopdf_options,
        verbose=settings.PDFKIT_VERBOSE_OUTPUT,
    )

    _remove_temporal_templates(templates)  # Deletion of the temporal files
    return output_filename
