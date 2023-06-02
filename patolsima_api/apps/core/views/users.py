from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class GetUserGroups(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request, format=None):
        return Response({"groups": [group.name for group in request.user.groups.all()]})
