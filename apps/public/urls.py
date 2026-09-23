from django.urls import path

from apps.public import views

app_name = "public"

urlpatterns = [
    path("", views.home, name="home"),
    path("contact/", views.contact_submit, name="contact"),
    path("robots.txt", views.robots, name="robots"),
]
