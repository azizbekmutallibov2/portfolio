# Portfolio — Arxitektura (v1)

> Bu hujjat — yagona haqiqat manbai. Ma'lumotlar modeli: `database.md`. UI: `component-spec.md`. Progress: `process.md`.
> Kalit so'zlar: **SHART** — majburiy; **TAQIQ** — qilinmaydi; **TAVSIYA** — imkon bo'lsa.

---

## 1. Maqsad va scope

Shaxsiy portfolio sayti: bitta ochiq sahifa (hero, loyihalar, stack, infra, ta'lim, profillar, aloqa) va faqat sayt egasi uchun boshqaruv paneli (xabarlar, kontent, loyihalar).

**v1 ichida:**
- Ochiq sayt (SSR), dark/light tema, desktop + mobil.
- Aloqa formasi → bazaga yoziladi, spam va rate-limit himoyasi bilan.
- Panel: kirish/chiqish, dashboard, xabarlar (ro'yxat, ko'rish, o'chirish), hero matni, profil havolalari, loyihalar CRUD.
- Kichik ochiq REST API (loyihalar, aloqa, health) — Infra bo'limida aynan shu endpointlar ko'rsatiladi.
- Production deploy: Nginx + Gunicorn (systemd) + PostgreSQL, Ubuntu VPS (WebDock).
- CI: lint, import qoidalari, migratsiya tekshiruvi, testlar, `check --deploy`.

**v1 dan tashqari (TAQIQ — qo'shilmaydi):** blog, rasm/fayl yuklash, inglizcha versiya, Redis, Celery, Docker'da production, OpenAPI/Swagger, analytics, SPA frontend, Django admin productionda.

---

## 2. Arxitektura qarorlari (ADR-lite)

| # | Qaror | Nega | Rad etilgan muqobil |
|---|---|---|---|
| 1 | **Django monolit, server-side rendering** (Django templates) | 1 deploy birligi, SEO tayyor, JS'siz ishlaydi, tez. Portfolio uchun SPA ortiqcha murakkablik. | DRF + Next.js (2 servis, CORS, token auth, 2 deploy) |
| 2 | **HackSoft qatlamlari:** `services.py` (yozish), `selectors.py` (o'qish), views/apis yupqa | Biznes mantiq bir joyda; 3 ta interfeys (sayt, panel, API) bir xil servislardan foydalanadi. | Mantiq view/model ichida |
| 3 | **Interfeys applar domen applardan ajratilgan** (`public`, `panel`, `api` → `content`, `contact`) va bu `import-linter` bilan CI'da tekshiriladi | Qatlam qoidasi hujjatda emas, avtomatik tekshiruvda yashaydi. | Faqat kelishuv |
| 4 | **Oddiy `forms.Form` va `serializers.Serializer`**; `ModelForm.save()` / `ModelSerializer.save()` TAQIQ | `ModelForm.is_valid()` instance'ni xotirada o'zgartiradi → servisdagi o'zgarish aniqlash buziladi va servis chetlab o'tiladi. | ModelForm |
| 5 | **Kichik public DRF API** (4 endpoint), auth'siz | Infra bo'limi real endpointlarni ko'rsatadi; repo'da DRF ko'nikmasi ko'rinadi. | API umuman yo'q |
| 6 | **Panel — Django session auth**, faqat `is_staff` | CSRF himoyasi tayyor, JWT kerak emas. | JWT |
| 7 | **Gunicorn'ni systemd boshqaradi** | Ubuntu'ning o'zida bor; restart, journald log, boot'da start. PM2 — Node vositasi, Python servisi uchun ortiqcha qaramlik. | PM2 |
| 8 | **Rate-limit — servisda, PostgreSQL orqali** (IP hash + vaqt oynasi) + Nginx `limit_req` chetda | Barcha worker'lar uchun to'g'ri ishlaydi, Redis kerak emas, test qilinadi. | DRF throttle + LocMemCache (har worker alohida hisoblaydi) |
| 9 | **Static — Nginx beradi**, `ManifestStaticFilesStorage` (hash'li fayl nomlari, 1 yillik cache) | Tez, cache-busting avtomatik. | WhiteNoise |
| 10 | **Strict CSP** → templatelarda inline `style=""` va inline `<script>` TAQIQ | XSS yuzasi kichrayadi; CI'dagi test buni kuzatadi. | `unsafe-inline` |
| 11 | **Django admin faqat `DEBUG=True`da** | Productionda hujum yuzasi yo'q; panel hamma ishni qiladi. | `/admin/` ochiq |
| 12 | **v1 faqat o'zbekcha** | Hozir ikki tilni yuritish — ikki barobar ish. v2 da Django i18n bilan inglizcha qo'shiladi. | Boshidan i18n |
| 13 | **Testlar real PostgreSQL'da** | Prod bilan bir xil xatti-harakat (constraint'lar, index'lar). | SQLite |

---

## 3. Tizim diagrammasi

```
Brauzer / mobil
      │ HTTPS :443
      ▼
┌──────────────────────── Ubuntu VPS (WebDock) ─────────────────────────┐
│ Nginx  — TLS, /static/, limit_req, CSP                                │
│   │  unix socket: /run/portfolio/gunicorn.sock                         │
│   ▼                                                                    │
│ Gunicorn  (systemd: portfolio.service, 2×CPU+1 worker)                 │
│   ▼                                                                    │
│ Django                                                                 │
│   Interfeys:  apps.public (SSR)   apps.panel (SSR, staff)   apps.api   │
│                      └────────────────┼──────────────────────┘         │
│   Domen:      apps.content  (SiteSettings, Project)                    │
│               apps.contact  (ContactMessage)                           │
│               services.py = yozish · selectors.py = o'qish             │
│   Asos:       apps.core (utils, base model) · apps.users (User)        │
│   ▼ ORM                                                                │
│ PostgreSQL 16 (lokal)                                                  │
└────────────────────────────────────────────────────────────────────────┘
      (Faza 6, ixtiyoriy) contact.message_create → on_commit → Telegram Bot API
```

**Bog'liqlik qoidasi (SHART):**
- `public`, `panel`, `api` → `content`, `contact`, `core`, `users` dan import qilishi mumkin.
- `content`, `contact`, `core`, `users` → interfeys applardan hech narsa import qilmaydi.
- `public`, `panel`, `api` bir-biridan import qilmaydi.

---

## 4. Texnologiyalar

| Qatlam | Tanlov |
|---|---|
| Til | Python 3.12 |
| Framework | Django 5.2 LTS (`Django>=5.2,<5.3`) |
| API | Django REST Framework (`djangorestframework>=3.16`) |
| DB drayver | `psycopg[binary]>=3.2` |
| Konfiguratsiya | `django-environ>=0.11` |
| WSGI | `gunicorn>=23` (faqat prod) |
| Test | `pytest`, `pytest-django`, `pytest-cov` |
| Lint/format | `ruff` |
| Arxitektura tekshiruvi | `import-linter` |
| Frontend | Django templates, oddiy CSS (custom properties), vanilla JS. Build tool yo'q. |
| Shriftlar | Geist, Geist Mono (Google Fonts) |
| DB | PostgreSQL 16 (lokalda `docker compose` orqali) |

Boshqa dependency qo'shish TAQIQ. O'rnatgandan keyin `requirements/*.txt` da aniq versiyalar `==` bilan pin qilinadi.

---

## 5. Loyiha tuzilmasi

```
portfolio/
├── manage.py
├── pyproject.toml              # ruff, pytest, coverage sozlamalari
├── .importlinter
├── .env.example
├── .gitignore
├── docker-compose.yml          # faqat lokal postgres:16
├── README.md                   # lokal ishga tushirish + deploy runbook
├── requirements/
│   ├── base.txt
│   ├── dev.txt                 # -r base.txt + test/lint
│   └── prod.txt                # -r base.txt + gunicorn
├── config/
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── dev.py
│   │   ├── test.py
│   │   └── prod.py
│   ├── urls.py
│   ├── api_urls.py             # /api/v1/ ostidagi hamma narsa
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── __init__.py
│   ├── core/                   # TimeStampedModel, model_update, ApplicationError, utils, templatetags
│   ├── users/                  # User(AbstractUser)
│   ├── content/                # SiteSettings, Project  — models, validators, services, selectors, management/commands/seed_content.py
│   ├── contact/                # ContactMessage — models, validators, services, selectors, integrations.py (Faza 6)
│   ├── public/                 # ochiq sayt: views, forms, urls, static_content.py, sitemaps.py
│   ├── panel/                  # boshqaruv paneli: views, forms, urls, decorators.py
│   └── api/                    # DRF: views.py, urls.py
│       (har app ichida tests/ papkasi)
├── templates/
│   ├── base.html
│   ├── components/             # _theme_toggle.html, _field.html, _flash.html
│   ├── public/                 # home.html + partials/_header … _footer
│   ├── panel/                  # base_panel.html, login.html, dashboard.html, messages_list.html,
│   │                           # message_detail.html, content.html, partials/
│   ├── 403.html  403_csrf.html  404.html  500.html
├── static/
│   ├── css/  tokens.css  base.css  public.css  panel.css
│   ├── js/   theme-init.js  theme.js  panel.js
│   └── img/  favicon.svg
├── deploy/
│   ├── gunicorn.conf.py
│   ├── systemd/portfolio.service
│   ├── nginx/portfolio.conf
│   └── deploy.sh
├── conftest.py
├── .github/workflows/ci.yml
└── docs/                       # shu hujjatlar
```

---

## 6. Qatlam qoidalari

### 6.1 Models
- Faqat maydonlar, `Meta` (ordering, constraints, indexes), `__str__`, sodda property (masalan `stack_items`).
- Biznes mantiq, boshqa modelni o'zgartirish, tashqi chaqiruv — TAQIQ.
- Barcha modellar (User'dan tashqari) `core.models.TimeStampedModel` dan meros oladi (SiteSettings bundan mustasno — faqat `updated_at`).

### 6.2 Selectors (`selectors.py`) — faqat o'qish
- Funksiyalar, faqat keyword argumentlar (`def project_list(*, published_only: bool = True)`).
- `QuerySet`, model yoki oddiy `dict` qaytaradi. Hech narsa yozmaydi.
- Type hint SHART.

### 6.3 Services (`services.py`) — barcha yozish
- Funksiyalar, faqat keyword argumentlar, type hint.
- Yozishdan oldin `full_clean()` SHART. Bir nechta yozuv bo'lsa `@transaction.atomic`.
- Yangilash uchun `core.services.model_update` ishlatiladi.
- Servis boshqa servis va selectorni chaqira oladi.
- Biznes qoidasi buzilsa `core.exceptions.ApplicationError` (yoki subklassi) ko'taradi.

### 6.4 Interfeyslar (views / apis / forms)
- Kiruvchi ma'lumotni forma yoki serializer bilan tekshiradi → servis/selector chaqiradi → javob qaytaradi. Boshqa mantiq yo'q.
- ORM'ga to'g'ridan-to'g'ri murojaat (`Model.objects...`) TAQIQ — faqat selector orqali. Istisno: `get_object_or_404` o'rniga ham selector ishlatiladi (`project_get(...)` → `None` bo'lsa `Http404`).
- Formalar `forms.Form`, serializerlar `serializers.Serializer` (ADR-4).

### 6.5 Namuna

```python
# apps/core/services.py
def model_update(*, instance, fields: list[str], data: dict) -> tuple[Model, bool]:
    changed = []
    for field in fields:
        if field in data and getattr(instance, field) != data[field]:
            setattr(instance, field, data[field])
            changed.append(field)
    if changed:
        instance.full_clean()
        if any(f.name == "updated_at" for f in instance._meta.fields):
            changed.append("updated_at")
        instance.save(update_fields=changed)
    return instance, bool(changed)
```

```python
# apps/contact/services.py
@transaction.atomic
def message_create(*, name: str, contact: str, body: str, ip: str, user_agent: str = "") -> ContactMessage:
    ip_hash = hash_ip(ip) if ip else ""
    if ip_hash:
        since = timezone.now() - timedelta(hours=1)
        if message_recent_count(ip_hash=ip_hash, since=since) >= settings.CONTACT_RATE_LIMIT_PER_HOUR:
            raise RateLimitExceeded("Juda ko'p xabar yuborildi. Bir soatdan keyin qayta urinib ko'ring.")
    message = ContactMessage(
        name=name.strip(), contact=contact.strip(), body=body.strip(),
        ip_hash=ip_hash, user_agent=user_agent[:300],
    )
    message.full_clean()
    message.save()
    return message
```

```python
# apps/public/views.py
@require_POST
def contact_submit(request):
    form = ContactForm(request.POST)
    if not form.is_valid():
        return render(request, "public/home.html", build_home_context(contact_form=form))
    if form.cleaned_data["website"]:  # honeypot: jim qabul qilamiz, saqlamaymiz
        messages.success(request, SUCCESS_TEXT)
        return redirect(f"{reverse('public:home')}#contact")
    try:
        message_create(
            name=form.cleaned_data["name"], contact=form.cleaned_data["contact"],
            body=form.cleaned_data["message"], ip=get_client_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
        )
    except RateLimitExceeded as exc:
        form.add_error(None, exc.message)
        return render(request, "public/home.html", build_home_context(contact_form=form), status=429)
    messages.success(request, SUCCESS_TEXT)
    return redirect(f"{reverse('public:home')}#contact")
```

### 6.6 Core yordamchilari
- `core.exceptions`: `ApplicationError(message, extra=None)`; `contact.exceptions.RateLimitExceeded(ApplicationError)`.
- `core.utils.get_client_ip(request)`: `HTTP_X_REAL_IP` → bo'lmasa `REMOTE_ADDR`. Izoh: prod'da Gunicorn faqat unix socket'da tinglaydi va Nginx `X-Real-IP`ni har doim qayta yozadi, shuning uchun sarlavhani mijoz soxtalashtira olmaydi.
- `core.utils.hash_ip(ip)`: `hmac.new(settings.IP_HASH_SALT.encode(), ip.encode(), hashlib.sha256).hexdigest()`. Xom IP bazaga yozilmaydi.
- `core.templatetags.url_tags.display_url`: `https://www.github.com/x/` → `github.com/x` (sxema, `www.`, oxirgi `/` olib tashlanadi).

---

## 7. Applar va javobgarlik

| App | Turi | Javobgarlik |
|---|---|---|
| `core` | asos | TimeStampedModel, model_update, xatolar, IP utils, `validate_phone`, template filter |
| `users` | asos | `User(AbstractUser)`, `AUTH_USER_MODEL = "users.User"` |
| `content` | domen | SiteSettings (singleton), Project; seed buyrug'i |
| `contact` | domen | ContactMessage; rate-limit; (Faza 6) bildirishnoma |
| `public` | interfeys | Bosh sahifa, aloqa POST, robots.txt, sitemap.xml, `static_content.py` |
| `panel` | interfeys | Kirish/chiqish, dashboard, xabarlar, kontent, loyihalar CRUD |
| `api` | interfeys | `/api/v1/` endpointlari |

`static_content.py` — Stack, Infra, Ta'lim bo'limlarining o'zgarmas ma'lumotlari (frozen dataclass'lar). Mazmuni `component-spec.md`da.

---

## 8. URL xaritasi

### 8.1 Ochiq sayt (`apps.public`, namespace `public`)
| Method | URL | Name | Izoh |
|---|---|---|---|
| GET | `/` | `home` | Barcha bo'limlar. Anonim uchun **≤ 2 SQL so'rov**. |
| POST | `/contact/` | `contact` | Faqat POST (GET → 405). Muvaffaqiyat → `302 /#contact` + flash. Xato → home qayta render (200, rate-limit → 429). |
| GET | `/robots.txt` | `robots` | `text/plain`: `Disallow: /panel/`, `Disallow: /api/`, `Sitemap:` |
| GET | `/sitemap.xml` | — | `django.contrib.sitemaps`, faqat `public:home`, `protocol="https"` |

### 8.2 Panel (`apps.panel`, namespace `panel`) — `/panel/login/`dan boshqa hammasi `@staff_required`
| Method | URL | Name | Izoh |
|---|---|---|---|
| GET, POST | `/panel/login/` | `login` | `LoginView`, `redirect_authenticated_user=True`, faqat staff kira oladi |
| POST | `/panel/logout/` | `logout` | `LogoutView` → `panel:login` |
| GET | `/panel/` | `dashboard` | Hisoblagichlar + oxirgi 10 xabar |
| GET | `/panel/messages/` | `messages` | Barcha xabarlar, 20 tadan sahifalash (`?page=`) |
| GET | `/panel/messages/<int:pk>/` | `message-detail` | To'liq xabar; ochilganda o'qilgan deb belgilanadi (idempotent, ataylab) |
| POST | `/panel/messages/<int:pk>/delete/` | `message-delete` | → `panel:messages` |
| GET | `/panel/content/` | `content` | Hero forma, havolalar formasi, loyihalar ro'yxati, "Yangi loyiha" formasi |
| POST | `/panel/content/hero/` | `hero-update` | → `panel:content#hero` |
| POST | `/panel/content/links/` | `links-update` | → `panel:content#links` |
| POST | `/panel/projects/new/` | `project-create` | Xato bo'lsa content sahifasi forma xatolari bilan qayta render |
| GET, POST | `/panel/projects/<int:pk>/edit/` | `project-edit` | Content sahifasi, o'ng pastda tahrirlash formasi |
| POST | `/panel/projects/<int:pk>/delete/` | `project-delete` | → `panel:content#projects` |

`staff_required`: anonim → `panel:login?next=...`ga redirect; kirgan, lekin staff emas → 403.
`settings.LOGIN_URL = "panel:login"`, `LOGIN_REDIRECT_URL = "panel:dashboard"`.

### 8.3 API (`apps.api`, namespace `api`, prefiks `/api/v1/`)
| Method | URL | Name | Javob |
|---|---|---|---|
| GET | `/api/v1/projects/` | `project-list` | `200 {"count": N, "results": [Project]}` — faqat published, `order, id` bo'yicha |
| GET | `/api/v1/projects/<slug>/` | `project-detail` | `200 Project` · unpublished/yo'q → `404` |
| POST | `/api/v1/contact/` | `contact-create` | `201 {"detail": "Xabar qabul qilindi."}` · `400` maydon xatolari · `429 {"detail": ...}` |
| GET | `/api/v1/health/` | `health` | `200 {"status":"ok","database":"ok"}` · DB ishlamasa `503 {"status":"degraded","database":"error"}` |

Project JSON: `slug, title, tag, tag_label, problem, solution, role, stack (list[str]), repo_url, demo_url`.
Contact so'rovi: `{"name", "contact", "message"}` — validatsiya sayt formasi bilan bir xil (`contact.validators`).

DRF sozlamalari:
```python
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],  # dev.py BrowsableAPIRenderer qo'shadi
    "DEFAULT_PARSER_CLASSES": ["rest_framework.parsers.JSONParser"],
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
}
```
API view'lari HackSoft uslubida: `APIView` + ichki `InputSerializer` / `OutputSerializer`.

### 8.4 Boshqa
- `config/urls.py`: `public.urls` (`""`), `panel.urls` (`"panel/"`), `config.api_urls` (`"api/v1/"`), sitemap. `if settings.DEBUG:` → `path("django-admin/", admin.site.urls)`.
- Xato sahifalari: `403.html`, `403_csrf.html`, `404.html`, `500.html` (500 — mustaqil, `base.html`ni extend qilmaydi, request/DB'ga tayanmaydi).

---

## 9. Asosiy oqimlar

**Aloqa formasi:** POST `/contact/` → Nginx `limit_req` → CSRF → `ContactForm` (validatsiya + honeypot) → `message_create` (IP hash → oxirgi 1 soatda ≥ `CONTACT_RATE_LIMIT_PER_HOUR` bo'lsa `RateLimitExceeded`) → `full_clean` → saqlash → `302 /#contact` + "Xabaringiz yuborildi. Tez orada javob beraman."

**Panel tahrirlash:** POST `/panel/projects/<pk>/edit/` → `staff_required` → `project_get` → `ProjectForm` → `project_update(project=..., data=form.cleaned_data)` → flash "Loyiha saqlandi." → redirect.

**API ro'yxat:** GET `/api/v1/projects/` → `project_list(published_only=True)` → `OutputSerializer(many=True)` → `{"count","results"}`.

---

## 10. Xavfsizlik

| Tahdid | Himoya |
|---|---|
| Panel brute-force | Nginx `limit_req` `/panel/login/` (10 r/min, burst 5); faqat `is_staff` kiradi; xato matni har doim bir xil ("Login yoki parol noto'g'ri.") |
| Spam | Honeypot maydon `website`; servisdagi rate-limit (5/soat/IP, env bilan); Nginx `limit_req` `/contact/`, `/api/v1/contact/` (6 r/min, burst 3); `client_max_body_size 1m` |
| CSRF | Django CSRF barcha sayt/panel POST'larida. Logout faqat POST. API'da session auth yo'q → ambient huquq yo'q. |
| XSS | Django auto-escape; `|safe` TAQIQ; CSP: `script-src 'self'`, inline yo'q |
| Clickjacking | `X_FRAME_OPTIONS = "DENY"`, CSP `frame-ancestors 'none'` |
| Transport | TLS (Let's Encrypt), HSTS, `SECURE_SSL_REDIRECT`, secure cookie'lar |
| Maxfiylik | Xom IP saqlanmaydi (HMAC-SHA256 hash). `.env` commit qilinmaydi. |
| Hujum yuzasi | Django admin prod'da yo'q; footer'da panel havolasi yo'q; `/panel/` robots'da yopiq, sahifalarda `noindex` |
| Tashqi havolalar | `target="_blank" rel="noopener noreferrer"` |

Prod xavfsizlik sozlamalari (`prod.py`):
```python
DEBUG = False
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = env.int("DJANGO_HSTS_SECONDS", default=3600)   # ishonch hosil bo'lgach 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = False
SILENCED_SYSTEM_CHECKS = ["security.W021"]   # preload — domen tayyor bo'lganda ongli qaror
SESSION_COOKIE_AGE = 60 * 60 * 12
X_FRAME_OPTIONS = "DENY"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"},
}
```

---

## 11. Konfiguratsiya

**base.py:** `LANGUAGE_CODE = "uz"`, `TIME_ZONE = "Asia/Tashkent"`, `USE_TZ = True`, `AUTH_USER_MODEL = "users.User"`, `DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"`, `TEMPLATES` → `DIRS=[BASE_DIR/"templates"]` + standart context processor'lar (request, auth, messages). DB so'rovi qiluvchi context processor TAQIQ.

`.env` faqat mavjud bo'lsa o'qiladi: `if (BASE_DIR / ".env").exists(): environ.Env.read_env(BASE_DIR / ".env")`.

**Muhit o'zgaruvchilari (`.env.example`):**

| O'zgaruvchi | Misol | Izoh |
|---|---|---|
| `DJANGO_SETTINGS_MODULE` | `config.settings.dev` | dev / test / prod |
| `DJANGO_SECRET_KEY` | — | `python -c "import secrets; print(secrets.token_urlsafe(64))"` (faqat URL-safe belgilar — bash `source` uchun xavfsiz) |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | vergul bilan |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://example.uz` | prod |
| `DATABASE_URL` | `postgres://portfolio:portfolio@localhost:5432/portfolio` | |
| `DJANGO_STATIC_ROOT` | `/srv/portfolio/static` | prod; default `BASE_DIR/"staticfiles"` |
| `DJANGO_HSTS_SECONDS` | `3600` | prod |
| `IP_HASH_SALT` | — | tasodifiy satr |
| `CONTACT_RATE_LIMIT_PER_HOUR` | `5` | |
| `TELEGRAM_BOT_TOKEN` | bo'sh | Faza 6; bo'sh bo'lsa o'chiq |
| `TELEGRAM_CHAT_ID` | bo'sh | Faza 6 |

**test.py:** `PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]`, `CONTACT_RATE_LIMIT_PER_HOUR = 5`.

**Logging:** barcha log stdout'ga (`StreamHandler`, format `{levelname} {asctime} {name} {message}`), root `INFO`, `django.request` `WARNING`. Prod'da systemd → journald (`journalctl -u portfolio`).

---

## 12. Test strategiyasi

**Piramida:**
1. **Servis va selector testlari** (eng ko'p) — biznes qoidalari, chegaraviy holatlar.
2. **Interfeys testlari** — Django `Client` / DRF `APIClient`: status kodlar, redirect'lar, huquqlar, forma xatolari.
3. **Himoya testlari (guard)** — arxitektura va sifat kafolatlari:
   - `test_templates_have_no_inline_styles_or_scripts` — `templates/` ichida `style="` va `src`siz `<script` yo'q.
   - `test_infra_endpoints_are_real` — `static_content.INFRA_ENDPOINTS`dagi har bir yo'l `resolve()` bo'ladi va `url_name`ga mos (`{slug}` → `sample`).
   - `test_home_query_count` — anonim bosh sahifa `django_assert_max_num_queries(2)`.
   - `test_dashboard_query_count` — `django_assert_max_num_queries(6)` (session + user bilan).

**Qoidalar:**
- Vositalar: `pytest`, `pytest-django`, `pytest-cov`. Factory'lar — oddiy funksiyalar (`apps/<app>/tests/factories.py`: `make_project(**overrides)`), factory_boy yo'q.
- Nomlash: `test_<birlik>__<holat>__<natija>`, masalan `test_message_create__over_limit__raises_rate_limit`.
- `created_at`ni o'tmishga surish: `ContactMessage.objects.filter(pk=m.pk).update(created_at=...)`.
- `conftest.py` fixture'lari: `staff_user`, `regular_user`, `staff_client`, `api_client`.
- Coverage: umumiy **≥ 85%** (CI'da majburiy); `services.py` va `selectors.py` uchun maqsad — 100% branch.
- Brauzer E2E yo'q; o'rniga `component-spec.md` §12 dagi qo'lda QA ro'yxati.

**Majburiy test holatlari** — har faza DoD'ida (§15) sanab o'tilgan.

---

## 13. CI (`.github/workflows/ci.yml`)

Trigger: `push`, `pull_request`. `ubuntu-24.04`, `postgres:16` service (health-check bilan), Python 3.12, pip cache.

Qadamlar (tartib bilan, biri yiqilsa to'xtaydi):
1. `pip install -r requirements/dev.txt`
2. `ruff check .`
3. `ruff format --check .`
4. `lint-imports`
5. `python manage.py makemigrations --check --dry-run`
6. `pytest --cov=apps --cov-report=term-missing --cov-fail-under=85`
7. `check --deploy`:
   ```bash
   DJANGO_SETTINGS_MODULE=config.settings.prod \
   DJANGO_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(64))')" \
   DJANGO_ALLOWED_HOSTS=example.com DJANGO_CSRF_TRUSTED_ORIGINS=https://example.com \
   python manage.py check --deploy --fail-level WARNING
   ```

`.importlinter`:
```ini
[importlinter]
root_packages =
    apps

[importlinter:contract:domain-does-not-import-interfaces]
name = Domain and base apps must not import interface apps
type = forbidden
source_modules =
    apps.core
    apps.users
    apps.content
    apps.contact
forbidden_modules =
    apps.public
    apps.panel
    apps.api

[importlinter:contract:interfaces-independent]
name = Interface apps are independent of each other
type = independence
modules =
    apps.public
    apps.panel
    apps.api
```

`pyproject.toml` (asosiy qismi):
```toml
[tool.ruff]
line-length = 100
target-version = "py312"
extend-exclude = ["**/migrations/*"]

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "DJ", "S", "SIM"]

[tool.ruff.lint.per-file-ignores]
"**/tests/**" = ["S101", "S105", "S106"]
"conftest.py" = ["S101", "S105", "S106"]

[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "config.settings.test"
python_files = ["test_*.py"]
addopts = "-q --strict-markers"
```

**Git:** har faza alohida branch (`phase-0-scaffold`, `phase-1-data`, …) → PR → CI yashil + review → `main`ga merge. Commit'lar — Conventional Commits (`feat:`, `fix:`, `test:`, `chore:`, `docs:`).

---

## 14. Deployment (WebDock Ubuntu VPS)

### 14.1 Server tuzilmasi
```
/srv/portfolio/app       # git repo (egasi: portfolio)
/srv/portfolio/venv      # virtualenv
/srv/portfolio/static    # collectstatic natijasi (Nginx o'qiydi)
/etc/portfolio/portfolio.env   # root:portfolio, 640
/run/portfolio/gunicorn.sock   # systemd RuntimeDirectory
```

### 14.2 `deploy/gunicorn.conf.py`
```python
import multiprocessing

bind = "unix:/run/portfolio/gunicorn.sock"
umask = 0o007
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 30
graceful_timeout = 30
max_requests = 1000
max_requests_jitter = 100
accesslog = "-"
errorlog = "-"
```

### 14.3 `deploy/systemd/portfolio.service`
```ini
[Unit]
Description=Portfolio Django app (Gunicorn)
After=network.target postgresql.service

[Service]
Type=notify
NotifyAccess=main
User=portfolio
Group=www-data
RuntimeDirectory=portfolio
WorkingDirectory=/srv/portfolio/app
EnvironmentFile=/etc/portfolio/portfolio.env
ExecStart=/srv/portfolio/venv/bin/gunicorn config.wsgi:application -c /srv/portfolio/app/deploy/gunicorn.conf.py
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=10
Restart=on-failure
RestartSec=3
PrivateTmp=true
NoNewPrivileges=true
ProtectSystem=full
ProtectHome=true

[Install]
WantedBy=multi-user.target
```

### 14.4 `deploy/nginx/portfolio.conf`
`example.uz` — real domen bilan almashtiriladi. Ubuntu 22.04/24.04 dagi Nginx 1.18/1.24 uchun `listen 443 ssl http2;` sintaksisi (`http2 on;` emas).
```nginx
limit_req_zone $binary_remote_addr zone=portfolio_forms:10m rate=6r/m;
limit_req_zone $binary_remote_addr zone=portfolio_login:10m rate=10r/m;
limit_req_status 429;

upstream portfolio_app {
    server unix:/run/portfolio/gunicorn.sock fail_timeout=0;
}

server {
    listen 80;
    listen [::]:80;
    server_name example.uz www.example.uz;
    return 301 https://example.uz$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name www.example.uz;
    ssl_certificate     /etc/letsencrypt/live/example.uz/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.uz/privkey.pem;
    return 301 https://example.uz$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name example.uz;

    ssl_certificate     /etc/letsencrypt/live/example.uz/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.uz/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;

    server_tokens off;
    client_max_body_size 1m;

    gzip on;
    gzip_min_length 1024;
    gzip_types text/css application/javascript application/json image/svg+xml;

    # Server darajasidagi header'lar faqat add_header'siz location'larga meros qoladi.
    add_header Content-Security-Policy "default-src 'self'; script-src 'self'; style-src 'self' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self'; form-action 'self'; frame-ancestors 'none'; base-uri 'self'; object-src 'none'" always;
    add_header Permissions-Policy "camera=(), microphone=(), geolocation=()" always;

    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_redirect off;
    proxy_read_timeout 30s;

    location /static/ {
        alias /srv/portfolio/static/;
        access_log off;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location = /contact/        { limit_req zone=portfolio_forms burst=3 nodelay; proxy_pass http://portfolio_app; }
    location = /api/v1/contact/ { limit_req zone=portfolio_forms burst=3 nodelay; proxy_pass http://portfolio_app; }
    location = /panel/login/    { limit_req zone=portfolio_login burst=5 nodelay; proxy_pass http://portfolio_app; }
    location / { proxy_pass http://portfolio_app; }
}
```

### 14.5 `deploy/deploy.sh` (sudo huquqli admin foydalanuvchi ishga tushiradi)
```bash
#!/usr/bin/env bash
set -euo pipefail
APP=/srv/portfolio/app
VENV=/srv/portfolio/venv
DOMAIN="${1:?usage: deploy.sh example.uz}"
run() { sudo -u portfolio bash -c "set -a; source /etc/portfolio/portfolio.env; set +a; cd $APP; $*"; }

run "git fetch --prune && git checkout main && git pull --ff-only"
run "$VENV/bin/pip install -r requirements/prod.txt"
run "$VENV/bin/python manage.py migrate --noinput"
run "$VENV/bin/python manage.py collectstatic --noinput"
run "$VENV/bin/python manage.py check --deploy --fail-level WARNING"
sudo systemctl reload portfolio
sleep 2
curl -fsS "https://$DOMAIN/api/v1/health/" && echo " — deploy OK"
```

### 14.6 Birinchi o'rnatish (README'ga runbook sifatida yoziladi)
1. `sudo apt install python3-venv postgresql nginx certbot python3-certbot-nginx git`
2. `sudo adduser --system --group --home /srv/portfolio portfolio`; `/srv/portfolio/{app,static}` va `/etc/portfolio` yaratish.
3. PostgreSQL: `CREATE ROLE portfolio LOGIN PASSWORD '...'; CREATE DATABASE portfolio OWNER portfolio;`
4. Repo'ni `/srv/portfolio/app`ga clone (portfolio foydalanuvchisi sifatida), venv yaratish, `requirements/prod.txt`.
5. `/etc/portfolio/portfolio.env` to'ldirish, `chown root:portfolio`, `chmod 640`.
6. `migrate`, `collectstatic`, `createsuperuser`, `seed_content`.
7. Unit'ni `/etc/systemd/system/`ga nusxalash → `systemctl daemon-reload && systemctl enable --now portfolio`.
8. Sertifikat: `sudo certbot certonly --nginx -d example.uz -d www.example.uz`.
9. Nginx conf'ni `sites-available`ga qo'yib, `sites-enabled`ga symlink → `sudo nginx -t && sudo systemctl reload nginx`.
10. Tekshirish: `curl https://example.uz/api/v1/health/`, `sudo certbot renew --dry-run`.
11. HSTS: bir hafta muammosiz ishlagach `DJANGO_HSTS_SECONDS=31536000`.

---

## 15. Fazalar va Definition of Done

**Har faza uchun umumiy DoD (hammasi o'tishi SHART):**
```
ruff check .
ruff format --check .
lint-imports
python manage.py makemigrations --check --dry-run
pytest --cov=apps --cov-fail-under=85
```
+ `process.md` yangilangan, faza branch'ida commit qilingan. Keyin agent **to'xtaydi** va review kutadi.

### Faza 0 — Skelet va CI
Tuzilma (§5), settings split, `.env.example`, requirements, `pyproject.toml`, `.importlinter`, `docker-compose.yml`, `.gitignore`, README (lokal ishga tushirish), barcha app'lar (bo'sh `AppConfig`), `users.User`, `core` (TimeStampedModel, model_update, ApplicationError, utils, `validate_phone`, `display_url`), `GET /api/v1/health/`, CI workflow.
Testlar: health 200; DB xatosida 503 (cursor mock); `model_update` — o'zgarish bor/yo'q, `updated_at` qo'shilishi, `full_clean` chaqirilishi; `get_client_ip` (X-Real-IP bor/yo'q); `hash_ip` deterministik va xom IP'dan farqli; `display_url` variantlari.

### Faza 1 — Ma'lumotlar qatlami
`database.md` bo'yicha modellar, migratsiyalar (SiteSettings data migration bilan), validatorlar, selectorlar, servislar, `seed_content` buyrug'i.
Testlar: `database.md` §6 dagi ro'yxat. Qo'shimcha DoD: `seed_content` ikki marta ishga tushirilganda dublikat yo'q.

### Faza 2 — Ochiq sayt
`base.html`, CSS/JS (`component-spec.md`), barcha bo'limlar desktop + mobil, `static_content.py`, aloqa formasi, robots, sitemap, xato sahifalari.
Testlar: home 200 va barcha bo'lim `id`lari bor; so'rovlar ≤ 2; unpublished loyiha ko'rinmaydi; 0 loyihada bo'sh holat matni; bo'sh havolalar render qilinmaydi; aloqa valid → 302 + saqlandi + flash; invalid → xatolar, saqlanmadi; honeypot → 302, saqlanmadi; limitdan oshsa → 429 + xato; GET `/contact/` → 405; robots `/panel/`ni yopadi; sitemap 200; guard testlar (§12).
TAVSIYA: brauzer vositasi bo'lsa, 390 / 768 / 1440 px, dark va light skrinshotlarini `docs/screenshots/`ga saqlash.

### Faza 3 — Panel
Login/logout, `staff_required`, dashboard, xabarlar (ro'yxat, ko'rish, o'chirish), content sahifasi (hero, havolalar, loyihalar CRUD), `panel.css`, `panel.js`, mobil holat.
Testlar: barcha panel URL'lari anonim → login'ga redirect (parametrize); oddiy user → 403; staff → 200; staff bo'lmagan user login qila olmaydi (umumiy xato matni); logout GET → 405; hero update faqat ruxsat etilgan maydonlarni o'zgartiradi; havolalarda sxemasiz kiritish `https://` bilan normallashadi; noto'g'ri domen (masalan GitHub maydoniga gitlab) → xato; loyiha create/edit/delete; delete GET → 405; xabar ochilganda `is_read=True`; sahifalash (21 xabar → 2 sahifa); CSRF'siz POST → 403 (`Client(enforce_csrf_checks=True)`); dashboard so'rovlar ≤ 6.

### Faza 4 — API
Loyihalar ro'yxati/detail, contact create, DRF sozlamalari.
Testlar: ro'yxat faqat published va tartibda; javob shakli va `stack` — list; detail unpublished/yo'q → 404; contact 201 va saqlandi; 400 maydon xatolari; 429 limit; noto'g'ri method → 405; prod settings'da renderer faqat JSON.

### Faza 5 — Production
`prod.py` (§10), logging, `deploy/` fayllari (§14), README deploy runbook, favicon, meta/OG teglari, CI'da `check --deploy`.
DoD: CI to'liq yashil, `check --deploy` o'tadi. Serverga deploy'ni sayt egasi runbook bo'yicha qiladi.

### Faza 6 — Ixtiyoriy: bildirishnoma va backup
- `contact/integrations.py::telegram_notify(*, message)`: `urllib.request`, timeout 3 s, xato log qilinadi va hech qachon ko'tarilmaydi; token bo'sh bo'lsa hech narsa qilmaydi. `message_create` ichida `transaction.on_commit(...)` orqali chaqiriladi.
- `deploy/backup.sh` + `portfolio-backup.service/.timer`: har kuni `pg_dump -Fc`, 14 kunlik saqlash.
Testlar: `django_capture_on_commit_callbacks` bilan chaqiruv; tarmoq xatosi request'ni buzmaydi; token bo'sh → chaqiruv yo'q.

---

## 16. Agent uchun qoidalar (qisqa)
1. Spec — yagona manba. Spec'da yo'q dependency, maydon, endpoint, sahifa, "yaxshilanish" qo'shilmaydi.
2. Noaniqlik/ziddiyat → spec'ga mos eng oddiy variant + `process.md` → "Savollar". `docs/*.md` (process.md'dan tashqari) o'zgartirilmaydi.
3. Bir vaqtda bitta faza. Faza oxirida DoD → `process.md` → commit → to'xtash.
4. Kod, nomlar, izohlar, commit'lar — inglizcha. UI matnlari — o'zbekcha, spec'dagidek.
5. Test — kod bilan birga yoziladi.
6. Secret'lar commit qilinmaydi.