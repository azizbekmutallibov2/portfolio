from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from apps.contact.exceptions import RateLimitExceeded
from apps.contact.services import message_create
from apps.content.selectors import project_list, site_settings_get
from apps.core.utils import get_client_ip
from apps.public import static_content
from apps.public.forms import ContactForm

SUCCESS_TEXT = "Xabaringiz yuborildi. Tez orada javob beraman."


def build_home_context(request: HttpRequest, *, contact_form: ContactForm | None = None) -> dict:
    host = request.get_host()
    return {
        "site": site_settings_get(),
        "projects": project_list(),
        "stack": static_content.STACK,
        "infra_client": static_content.INFRA_NODES[0],
        "infra_frame_nodes": static_content.INFRA_NODES[1:],
        "infra_endpoints": static_content.INFRA_ENDPOINTS,
        "infra_logs": [
            static_content.InfraLog(who=log.who, msg=log.msg.format(host=host))
            for log in static_content.INFRA_LOGS
        ],
        "education": static_content.EDUCATION,
        "contact_form": contact_form or ContactForm(),
    }


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "public/home.html", build_home_context(request))


@require_POST
def contact_submit(request: HttpRequest) -> HttpResponse:
    form = ContactForm(request.POST)

    if not form.is_valid():
        form.mark_invalid_fields()
        return render(request, "public/home.html", build_home_context(request, contact_form=form))

    if form.cleaned_data["website"]:
        messages.success(request, SUCCESS_TEXT)
        return redirect(f"{reverse('public:home')}#contact")

    try:
        message_create(
            name=form.cleaned_data["name"],
            contact=form.cleaned_data["contact"],
            body=form.cleaned_data["message"],
            ip=get_client_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
        )
    except RateLimitExceeded as exc:
        form.add_error(None, exc.message)
        return render(
            request,
            "public/home.html",
            build_home_context(request, contact_form=form),
            status=429,
        )

    messages.success(request, SUCCESS_TEXT)
    return redirect(f"{reverse('public:home')}#contact")


def robots(request: HttpRequest) -> HttpResponse:
    lines = [
        "User-agent: *",
        "Disallow: /panel/",
        "Disallow: /api/",
        f"Sitemap: https://{request.get_host()}/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
