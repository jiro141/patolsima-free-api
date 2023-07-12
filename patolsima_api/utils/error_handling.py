from rest_framework.exceptions import ValidationError
from rest_framework.views import exception_handler
from rest_framework.response import Response


def general_error_handler(exception: Exception, context):
    response_from_framework_handler = exception_handler(exception, context)

    return (
        response_from_framework_handler
        if response_from_framework_handler
        else Response(
            status=500, data={"detail": f"{type(exception).__name__}: {exception}"}
        )
    )
