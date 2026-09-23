from django.urls import path

from apps.panel import views

app_name = "panel"

urlpatterns = [
    path("login/", views.PanelLoginView.as_view(), name="login"),
    path("logout/", views.PanelLogoutView.as_view(), name="logout"),
    path("", views.dashboard, name="dashboard"),
    path("messages/", views.messages_list_view, name="messages"),
    path("messages/<int:pk>/", views.message_detail, name="message-detail"),
    path("messages/<int:pk>/delete/", views.message_delete_view, name="message-delete"),
    path("content/", views.content, name="content"),
    path("content/hero/", views.hero_update, name="hero-update"),
    path("content/links/", views.links_update, name="links-update"),
    path("projects/new/", views.project_create, name="project-create"),
    path("projects/<int:pk>/edit/", views.project_edit, name="project-edit"),
    path("projects/<int:pk>/delete/", views.project_delete, name="project-delete"),
]
