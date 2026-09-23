from django.contrib import messages as django_messages
from django.contrib.auth import views as auth_views
from django.core.paginator import Paginator
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from apps.contact.selectors import message_counts, message_get, message_list
from apps.contact.services import message_delete as message_delete_service
from apps.contact.services import message_mark_read
from apps.content.models import Project
from apps.content.selectors import project_counts, project_get, project_list, site_settings_get
from apps.content.services import HERO_FIELDS, LINK_FIELDS, project_update, site_settings_update
from apps.content.services import project_create as project_create_service
from apps.content.services import project_delete as project_delete_service
from apps.panel.decorators import staff_required
from apps.panel.forms import HeroForm, LinksForm, ProjectForm, StaffAuthenticationForm


class PanelLoginView(auth_views.LoginView):
    template_name = "panel/login.html"
    authentication_form = StaffAuthenticationForm
    redirect_authenticated_user = True


class PanelLogoutView(auth_views.LogoutView):
    next_page = "panel:login"


def _hero_initial() -> dict:
    site = site_settings_get()
    return {field: getattr(site, field) for field in HERO_FIELDS}


def _links_initial() -> dict:
    site = site_settings_get()
    return {field: getattr(site, field) for field in LINK_FIELDS}


def _project_initial(project: Project) -> dict:
    return {
        "title": project.title,
        "tag": project.tag,
        "stack": project.stack,
        "order": project.order,
        "problem": project.problem,
        "solution": project.solution,
        "role": project.role,
        "is_published": project.is_published,
        "repo_url": project.repo_url,
        "demo_url": project.demo_url,
    }


def _content_context(
    *,
    hero_form: HeroForm | None = None,
    links_form: LinksForm | None = None,
    project_form: ProjectForm | None = None,
    editing_project: Project | None = None,
) -> dict:
    return {
        "hero_form": hero_form or HeroForm(initial=_hero_initial()),
        "links_form": links_form or LinksForm(initial=_links_initial()),
        "projects": project_list(published_only=False),
        "project_form": project_form or ProjectForm(),
        "editing_project": editing_project,
        "active_nav": "content",
    }


@staff_required
def dashboard(request: HttpRequest) -> HttpResponse:
    context = {
        "message_counts": message_counts(),
        "project_counts": project_counts(),
        "recent_messages": message_list()[:10],
        "active_nav": "dashboard",
    }
    return render(request, "panel/dashboard.html", context)


@staff_required
def messages_list_view(request: HttpRequest) -> HttpResponse:
    paginator = Paginator(message_list(), 20)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(
        request, "panel/messages_list.html", {"page_obj": page_obj, "active_nav": "messages"}
    )


@staff_required
def message_detail(request: HttpRequest, pk: int) -> HttpResponse:
    message = message_get(pk=pk)
    if message is None:
        raise Http404
    message_mark_read(message=message)
    return render(
        request, "panel/message_detail.html", {"message": message, "active_nav": "messages"}
    )


@staff_required
@require_POST
def message_delete_view(request: HttpRequest, pk: int) -> HttpResponse:
    message = message_get(pk=pk)
    if message is None:
        raise Http404
    message_delete_service(message=message)
    django_messages.success(request, "Xabar o'chirildi.")
    return redirect("panel:messages")


@staff_required
def content(request: HttpRequest) -> HttpResponse:
    return render(request, "panel/content.html", _content_context())


@staff_required
@require_POST
def hero_update(request: HttpRequest) -> HttpResponse:
    form = HeroForm(request.POST)
    if form.is_valid():
        _, changed = site_settings_update(data=form.cleaned_data, fields=HERO_FIELDS)
        django_messages.success(request, "Hero matni saqlandi." if changed else "O'zgarish yo'q.")
        return redirect(f"{reverse('panel:content')}#hero")
    return render(request, "panel/content.html", _content_context(hero_form=form))


@staff_required
@require_POST
def links_update(request: HttpRequest) -> HttpResponse:
    form = LinksForm(request.POST)
    if form.is_valid():
        _, changed = site_settings_update(data=form.cleaned_data, fields=LINK_FIELDS)
        django_messages.success(request, "Havolalar saqlandi." if changed else "O'zgarish yo'q.")
        return redirect(f"{reverse('panel:content')}#links")
    return render(request, "panel/content.html", _content_context(links_form=form))


@staff_required
@require_POST
def project_create(request: HttpRequest) -> HttpResponse:
    form = ProjectForm(request.POST)
    if form.is_valid():
        project_create_service(**form.cleaned_data)
        django_messages.success(request, "Loyiha qo'shildi.")
        return redirect(f"{reverse('panel:content')}#projects")
    return render(request, "panel/content.html", _content_context(project_form=form))


@staff_required
def project_edit(request: HttpRequest, pk: int) -> HttpResponse:
    project = project_get(pk=pk, published_only=False)
    if project is None:
        raise Http404

    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project_update(project=project, data=form.cleaned_data)
            django_messages.success(request, "Loyiha saqlandi.")
            return redirect(f"{reverse('panel:content')}#projects")
        return render(
            request,
            "panel/content.html",
            _content_context(project_form=form, editing_project=project),
        )

    form = ProjectForm(initial=_project_initial(project))
    return render(
        request, "panel/content.html", _content_context(project_form=form, editing_project=project)
    )


@staff_required
@require_POST
def project_delete(request: HttpRequest, pk: int) -> HttpResponse:
    project = project_get(pk=pk, published_only=False)
    if project is None:
        raise Http404
    project_delete_service(project=project)
    django_messages.success(request, "Loyiha o'chirildi.")
    return redirect(f"{reverse('panel:content')}#projects")
