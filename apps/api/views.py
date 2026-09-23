from django.db import connection
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.serializers import ContactCreateInputSerializer, ProjectOutputSerializer
from apps.contact.exceptions import RateLimitExceeded
from apps.contact.services import message_create
from apps.content.selectors import project_get, project_list
from apps.core.utils import get_client_ip

CONTACT_ACCEPTED_TEXT = "Xabar qabul qilindi."


@api_view(["GET"])
def health(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except Exception:
        return Response({"status": "degraded", "database": "error"}, status=503)
    return Response({"status": "ok", "database": "ok"})


class ProjectListAPIView(APIView):
    def get(self, request):
        projects = list(project_list(published_only=True))
        serializer = ProjectOutputSerializer(projects, many=True)
        return Response({"count": len(projects), "results": serializer.data})


class ProjectDetailAPIView(APIView):
    def get(self, request, slug):
        project = project_get(slug=slug, published_only=True)
        if project is None:
            raise Http404
        return Response(ProjectOutputSerializer(project).data)


class ContactCreateAPIView(APIView):
    def post(self, request):
        serializer = ContactCreateInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            message_create(
                name=serializer.validated_data["name"],
                contact=serializer.validated_data["contact"],
                body=serializer.validated_data["message"],
                ip=get_client_ip(request),
                user_agent=request.META.get("HTTP_USER_AGENT", ""),
            )
        except RateLimitExceeded as exc:
            return Response({"detail": exc.message}, status=429)

        return Response({"detail": CONTACT_ACCEPTED_TEXT}, status=201)
