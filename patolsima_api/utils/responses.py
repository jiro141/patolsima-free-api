from rest_framework.response import Response


def method_not_allowed():
    return Response(status=405, data={"error": "Method not allowed"})
