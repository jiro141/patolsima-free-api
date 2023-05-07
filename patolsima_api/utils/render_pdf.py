import pdfkit
import os
import contextlib
from typing import Dict, Any
from django.conf import settings


def render_pdf(
    context: Dict[str, Any], templates: Dict[str, dict], destination: str
) -> str:
    for t_key, t_config in templates.items():
        if t_config.get("pre_render"):
            temp_filename = f"{settings.PDFKIT_RENDER_PATH}/{destination}_{t_key}.html"
            with open(temp_filename, "w") as temp_file:
                temp_file.writelines(t_config["template_obj"].render(**context))
            t_config["source"] = temp_filename

    options = {}
    if "header" in templates:
        c = templates.pop("header")
        options["--header-html"] = c["source"]
    if "footer" in templates:
        c = templates.pop("footer")
        options["--footer-html"] = c["source"]

    output_filename = f"{settings.PDFKIT_RENDER_PATH}/{destination}.pdf"

    pdfkit.from_file(
        [conf["source"] for t, conf in templates.items()],
        output_filename,
        configuration=settings.PDFKIT_CONFIGURATION,
        options=options,
    )

    # Deletion of the temporal files
    for template_obj in templates.values():
        with contextlib.suppress(OSError):
            os.remove(template_obj["source"])

    return output_filename
