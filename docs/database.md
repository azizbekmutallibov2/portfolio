# Portfolio — Ma'lumotlar bazasi (v1)

PostgreSQL 16. Barcha PK — `BigAutoField`. Vaqt — `USE_TZ=True` (UTC saqlanadi, `Asia/Tashkent`da ko'rsatiladi).
Validatsiya ikki joyda: model validatorlari (`full_clean` orqali servisda) va forma/serializer (foydalanuvchiga xato ko'rsatish uchun). Ikkalasi ham **bir xil validator funksiyalarini** ishlatadi.

---

## 1. `core.TimeStampedModel` (abstract)

| Maydon | Tur | Izoh |
|---|---|---|
| `created_at` | `DateTimeField(auto_now_add=True, db_index=True)` | |
| `updated_at` | `DateTimeField(auto_now=True)` | |

## 2. `users.User`

```python
class User(AbstractUser):
    pass
```
`AUTH_USER_MODEL = "users.User"` — birinchi migratsiyadan oldin. Panelga kirish uchun `is_staff=True` (superuser `createsuperuser` bilan yaratiladi).

---

## 3. `content.SiteSettings` — singleton

Bitta qator, `id = 1`. Hero va aloqa ma'lumotlari.

| Maydon | Tur | Cheklov | Default |
|---|---|---|---|
| `id` | BigAutoField | `CheckConstraint(condition=Q(id=1), name="site_settings_singleton")` | 1 |
| `hero_line_1` | `CharField(max_length=60)` | | `Kod yozaman.` |
| `hero_line_2` | `CharField(max_length=60)` | | `Serverga chiqaraman.` |
| `about_text` | `CharField(max_length=300)` | | `Azizillo. Django va Django REST Framework'da backend yozaman. TATU, Software Engineering, 1-kurs.` |
| `status_text` | `CharField(max_length=160)` | | `TuitDorm — TATU yotoqxonasini boshqarish tizimi ustida ishlayapman.` |
| `github_url` | `URLField(blank=True)` | `validate_github_url` | `""` |
| `telegram_url` | `URLField(blank=True)` | `validate_telegram_url` | `""` |
| `linkedin_url` | `URLField(blank=True)` | `validate_linkedin_url` | `""` |
| `contact_email` | `EmailField(blank=True)` | | `""` |
| `contact_phone` | `CharField(max_length=20, blank=True)` | `validate_phone` | `""` |
| `updated_at` | `DateTimeField(auto_now=True)` | | |

- Django 5.2'da `CheckConstraint(condition=...)` (eski `check=` — deprecated).
- Data migration `0002_create_site_settings`: `SiteSettings(id=1)` default'lar bilan yaratiladi (`get_or_create`).
- `verbose_name` o'zbekcha.

**Validatorlar (`content/validators.py`):**
- `validate_github_url`: host `github.com` yoki `www.github.com`, yo'l bo'sh emas.
- `validate_telegram_url`: host `t.me`.
- `validate_linkedin_url`: host `linkedin.com` yoki `www.linkedin.com`, yo'l `/in/` bilan boshlanadi.
- Xato matni: `"Havola {domen} manziliga olib borishi kerak."`
- `validate_phone` — `contact.validators`dan emas, `core.validators`da (ikkala app ishlatadi): ruxsat etilgan belgilar `+`, raqam, bo'shliq, `(`, `)`, `-`; raqamlar soni 7–15. Xato: `"Telefon raqam noto'g'ri."`

## 4. `content.Project`

| Maydon | Tur | Cheklov / izoh |
|---|---|---|
| `id` | BigAutoField | |
| `title` | `CharField(max_length=120)` | |
| `slug` | `SlugField(max_length=140, unique=True)` | Servis yaratadi; yangilashda **o'zgarmaydi** |
| `tag` | `CharField(max_length=20, choices=ProjectTag.choices, default=ProjectTag.PRODUCTION)` | |
| `problem` | `TextField` | `MaxLengthValidator(600)` |
| `solution` | `TextField` | `MaxLengthValidator(600)` |
| `role` | `CharField(max_length=300)` | |
| `stack` | `CharField(max_length=200)` | Normallashgan: `"Django, PostgreSQL, Nginx"` |
| `repo_url` | `URLField(blank=True)` | |
| `demo_url` | `URLField(blank=True)` | |
| `order` | `PositiveSmallIntegerField(default=0)` | Kichigi oldinda |
| `is_published` | `BooleanField(default=True)` | |
| `created_at`, `updated_at` | TimeStampedModel | |

```python
class ProjectTag(models.TextChoices):
    PRODUCTION = "production", "PRODUCTION"
    TEAM = "team", "GURUH LOYIHASI"
    PERSONAL = "personal", "SHAXSIY LOYIHA"
    LEARNING = "learning", "O'QUV LOYIHASI"
```

**Meta:**
- `ordering = ["order", "id"]`
- `indexes = [models.Index(fields=["is_published", "order"], name="project_published_order_idx")]`

**Property:** `stack_items -> list[str]` — `stack`ni vergul bo'yicha bo'lib, bo'sh joylarni tozalaydi. Templateda `" · "` bilan, API'da list sifatida.

## 5. `contact.ContactMessage`

| Maydon | Tur | Cheklov / izoh |
|---|---|---|
| `id` | BigAutoField | |
| `name` | `CharField(max_length=100)` | `MinLengthValidator(2)` |
| `contact` | `CharField(max_length=150)` | `validate_contact` — email **yoki** telefon |
| `body` | `TextField` | `MinLengthValidator(10)`, `MaxLengthValidator(2000)` |
| `is_read` | `BooleanField(default=False)` | |
| `ip_hash` | `CharField(max_length=64, blank=True)` | HMAC-SHA256; xom IP saqlanmaydi |
| `user_agent` | `CharField(max_length=300, blank=True)` | 300 belgigacha kesiladi |
| `created_at`, `updated_at` | TimeStampedModel | |

**Meta:**
- `ordering = ["-created_at"]`
- `indexes = [models.Index(fields=["ip_hash", "created_at"], name="message_ip_created_idx")]` — rate-limit so'rovi uchun.

**`contact/validators.py::validate_contact(value)`:** `strip()` → `EmailValidator` o'tsa OK → aks holda `core.validators.validate_phone` → ikkalasi ham o'tmasa `ValidationError("Telefon raqam yoki email kiriting.", code="invalid_contact")`.

---

## 6. Selectorlar, servislar va ularning testlari

### `content/selectors.py`
| Funksiya | Qaytaradi | Test |
|---|---|---|
| `site_settings_get()` | `SiteSettings` (`get_or_create(pk=1)[0]`) | qator o'chirilgan bo'lsa ham qaytaradi |
| `project_list(*, published_only=True)` | `QuerySet[Project]` | faqat published; tartib `order, id`; `published_only=False` hammasini beradi |
| `project_get(*, pk=None, slug=None, published_only=True)` | `Project \| None` | yo'q → None; unpublished + published_only → None |
| `project_counts()` | `{"total": int, "published": int}` — **bitta** `aggregate` so'rovi | `django_assert_num_queries(1)` |

### `content/services.py`
| Funksiya | Qoida | Test |
|---|---|---|
| `site_settings_update(*, data, fields)` | `fields` faqat `HERO_FIELDS` yoki `LINK_FIELDS` ichidan (boshqasi → `ValueError`); `model_update` | faqat berilgan maydonlar o'zgaradi; noto'g'ri URL → `ValidationError`; ruxsatsiz maydon → `ValueError` |
| `project_create(*, title, tag, problem, solution, role, stack, repo_url="", demo_url="", order=0, is_published=True)` | slug: `slugify(title)[:120]` yoki `"loyiha"`; band bo'lsa `-2`, `-3`…; `stack` normallashadi | `"O'zbekiston Kitobxonlari Jamiyati"` → `ozbekiston-kitobxonlari-jamiyati`; bir xil nom → `-2`; kirill nom → `loyiha`; stack normallashuvi; bo'sh `title` → `ValidationError` |
| `project_update(*, project, data)` | `PROJECT_UPDATABLE_FIELDS` (slug yo'q); `stack` normallashadi | slug o'zgarmaydi; o'zgarish yo'q → save chaqirilmaydi |
| `project_delete(*, project)` | | o'chiriladi |

`normalize_stack("Django · PostgreSQL,  Nginx, django")` → `"Django, PostgreSQL, Nginx"` (ajratkich `,` yoki `·`; bo'sh joylar olib tashlanadi; takror — katta-kichik harfga qaramay birinchisi qoladi).

`HERO_FIELDS = ["hero_line_1", "hero_line_2", "about_text", "status_text"]`
`LINK_FIELDS = ["github_url", "telegram_url", "linkedin_url", "contact_email", "contact_phone"]`

### `contact/selectors.py`
| Funksiya | Qaytaradi | Test |
|---|---|---|
| `message_list()` | `QuerySet` `-created_at` | tartib |
| `message_get(*, pk)` | `ContactMessage \| None` | |
| `message_counts()` | `{"total", "unread"}` — bitta `aggregate` (`Count("id", filter=Q(is_read=False))`) | 1 so'rov |
| `message_recent_count(*, ip_hash, since)` | `int` | oynadan tashqaridagilar hisoblanmaydi; boshqa IP hisoblanmaydi |

### `contact/services.py`
| Funksiya | Qoida | Test |
|---|---|---|
| `message_create(*, name, contact, body, ip, user_agent="")` | architecture §6.5 | saqlanadi, `ip_hash` 64 belgi va xom IP emas; `CONTACT_RATE_LIMIT_PER_HOUR`-chi xabar o'tadi, keyingisi `RateLimitExceeded`; 1 soatdan eski xabarlar hisoblanmaydi; `ip=""` bo'lsa limit tekshirilmaydi; noto'g'ri `contact` → `ValidationError`; bo'sh joylar `strip`; user_agent 300 ga kesiladi |
| `message_mark_read(*, message)` | idempotent, faqat `is_read=False` bo'lsa yozadi | ikki marta chaqirish xavfsiz |
| `message_delete(*, message)` | | |

---

## 7. Seed — `python manage.py seed_content`

Idempotent: `SiteSettings` — `get_or_create(pk=1)`; loyihalar — `update_or_create(slug=...)`. Mavjud `SiteSettings` qiymatlarini **qayta yozmaydi**.

| slug | title | tag | order | is_published |
|---|---|---|---|---|
| `tuitdorm` | TuitDorm | production | 1 | `True` |
| `ozbekiston-kitobxonlari-jamiyati` | O'zbekiston Kitobxonlari Jamiyati | team | 2 | **`False`** (placeholder'lar to'ldirilguncha saytda ko'rinmaydi) |

**TuitDorm:**
- problem: `TATU yotoqxonasida davomat qog'oz daftarlarda yuritilgan: sekin, xatoga moyil, natijani tez ko'rib bo'lmaydi.`
- solution: `Yotoqxonani boshqarish uchun production-grade tizim: ma'lumotlar PostgreSQL'da, ilova Nginx orqasida VPS'da ishlaydi.`
- role: `Arxitektura, backend va deployment — noldan o'zim.`
- stack: `Django, PostgreSQL, Nginx`
- repo_url, demo_url: bo'sh

**OKJ:**
- problem: `[TO'LDIRING: platforma qaysi ehtiyojni yopadi — 1–2 jumla]`
- solution: `Backend Django REST'da, frontend Next.js (App Router)da. Django loyihasi 13 ta ilovaga bo'lingan; biznes mantiq services va selectors qatlamlarida (HackSoft yondashuvi).`
- role: `[TO'LDIRING: siz qilgan qism]`
- stack: `Django REST Framework, Next.js`
- repo_url, demo_url: bo'sh

Test: buyruq ikki marta → `Project.objects.count() == 2`, `SiteSettings.objects.count() == 1`; qo'lda o'zgartirilgan `hero_line_1` qayta yozilmaydi.