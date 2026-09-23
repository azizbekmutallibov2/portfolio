from dataclasses import dataclass


@dataclass(frozen=True)
class StackRow:
    layer: str
    tech: str
    note: str


STACK: tuple[StackRow, ...] = (
    StackRow("TIL", "Python", "Asosiy til, backend uchun."),
    StackRow(
        "FRAMEWORK",
        "Django, Django REST Framework",
        "REST API, services/selectors arxitekturasi.",
    ),
    StackRow("MA'LUMOTLAR BAZASI", "PostgreSQL", "TuitDorm va shu saytning bazasi."),
    StackRow(
        "SERVER",
        "Nginx, Gunicorn, systemd, PM2",
        "Reverse proxy va WSGI; Python servislar — systemd, Node servislar — PM2.",
    ),
    StackRow("INFRA", "Ubuntu VPS (WebDock)", "Serverni o'zim sozlaganman va yuritaman."),
    StackRow("FRONTEND", "Next.js", "OKJ platformasida, App Router bilan."),
    StackRow("VOSITALAR", "Git, Docker, Linux", "Versiyalash, konteynerlar, buyruq qatori."),
)


@dataclass(frozen=True)
class InfraNode:
    index: str
    name: str
    sub: str
    in_frame: bool


INFRA_NODES: tuple[InfraNode, ...] = (
    InfraNode("01", "Client", "brauzer / mobil", False),
    InfraNode("02", "Nginx", "TLS · reverse proxy", True),
    InfraNode("03", "Gunicorn", "WSGI · systemd", True),
    InfraNode("04", "Django", "services · selectors", True),
    InfraNode("05", "PostgreSQL", "ma'lumotlar bazasi", True),
)


@dataclass(frozen=True)
class InfraEndpoint:
    method: str
    path: str
    note: str
    url_name: str


INFRA_ENDPOINTS: tuple[InfraEndpoint, ...] = (
    InfraEndpoint("GET", "/api/v1/projects/", "ro'yxat", "api:project-list"),
    InfraEndpoint("GET", "/api/v1/projects/{slug}/", "bitta loyiha", "api:project-detail"),
    InfraEndpoint("POST", "/api/v1/contact/", "xabar", "api:contact-create"),
    InfraEndpoint("GET", "/api/v1/health/", "holat", "api:health"),
)


@dataclass(frozen=True)
class InfraLog:
    who: str
    msg: str


INFRA_LOGS: tuple[InfraLog, ...] = (
    InfraLog("client", "→ GET https://{host}/api/v1/projects/"),
    InfraLog("nginx", "→ TLS, proxy_pass → unix socket"),
    InfraLog("gunicorn", "→ systemd boshqaradigan worker"),
    InfraLog("django", "→ api → selector → ORM"),
    InfraLog("postgres", "→ SELECT … FROM content_project"),
    InfraLog("client", "← 200 JSON"),
)


@dataclass(frozen=True)
class EducationItem:
    when: str
    title: str
    sub: str


EDUCATION: tuple[EducationItem, ...] = (
    EducationItem(
        "HOZIR · 1-KURS",
        "TATU",
        "Toshkent Axborot Texnologiyalari Universiteti — Software Engineering.",
    ),
    EducationItem("HOZIR", "Najot Ta'lim", "Python backend yo'nalishi."),
)
