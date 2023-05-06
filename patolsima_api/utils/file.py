from django.conf import settings
from django.http import StreamingHttpResponse
from typing import Generator, Iterable


# At the end I replaced everything in this file with a call to Django's FileResponse
# Jesus, 06/05/2023


def extract_file_bytes(filepath: str) -> Generator[bytes, None, None]:
    with open(filepath, "rb") as binary_file:
        while buffer := binary_file.read(settings.BINARY_BUFFER_SIZE_RESPONSES):
            yield buffer


def response_as_binary_file_stream(
    filename: str,
    bytes_array: Iterable[bytes],
    content_type: str = "application/octet-stream",
) -> StreamingHttpResponse:
    response = StreamingHttpResponse(bytes_array, content_type=content_type)
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response
