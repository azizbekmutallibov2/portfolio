from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/v1/", include("config.api_urls")),
]

if settings.DEBUG:
    urlpatterns += [path("django-admin/", admin.site.urls)]
