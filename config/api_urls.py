from django.urls import path

from apps.api import views

app_name = "api"

urlpatterns = [
    path("health/", views.health, name="health"),
    path("projects/", views.ProjectListAPIView.as_view(), name="project-list"),
    path("projects/<slug:slug>/", views.ProjectDetailAPIView.as_view(), name="project-detail"),
    path("contact/", views.ContactCreateAPIView.as_view(), name="contact-create"),
]
