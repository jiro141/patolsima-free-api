import os
import contextlib
from django.conf import settings
from django.http import StreamingHttpResponse
from typing import Generator, Iterable
from django.http import FileResponse


# At the end I replaced everything in this file with a call to Django's FileResponse
# Jesus, 06/05/2023

# Last sentence was false, so I'll keep the file and its content


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


class FileResponseWithTemporalFileDeletion(FileResponse):
    def __init__(self, *args, **kwargs):
        self.temporal_file_path = kwargs.pop("temporal_file_path", None)
        super().__init__(*args, **kwargs)

    def close(self):
        super().close()
        if self.temporal_file_path:
            with contextlib.suppress(IOError, OSError):
                os.remove(self.temporal_file_path)
