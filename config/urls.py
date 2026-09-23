from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from apps.public.sitemaps import sitemaps

urlpatterns = [
    path("", include("apps.public.urls")),
    path("api/v1/", include("config.api_urls")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
]

if settings.DEBUG:
    urlpatterns += [path("django-admin/", admin.site.urls)]
