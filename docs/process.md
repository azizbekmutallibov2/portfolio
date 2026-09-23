# process.md

> Agent har faza oxirida shu faylni yangilaydi. Qisqa va faktlar bilan yoziladi.
> Spec fayllari (`architecture.md`, `database.md`, `component-spec.md`) bu yerda emas, review'dan keyin o'zgartiriladi.

## Holat

| Faza | Holat | Branch | Oxirgi commit |
|---|---|---|---|
| 0 — Skelet va CI | [R] | `phase-0-scaffold` | `fc7665e` |
| 1 — Ma'lumotlar qatlami | [R] | `phase-1-data` | `7a3130c` |
| 2 — Ochiq sayt | [ ] | `phase-2-public` | |
| 3 — Panel | [ ] | `phase-3-panel` | |
| 4 — API | [ ] | `phase-4-api` | |
| 5 — Production | [ ] | `phase-5-prod` | |
| 6 — Bildirishnoma va backup (ixtiyoriy) | [ ] | `phase-6-extras` | |

Belgilar: `[ ]` boshlanmagan · `[~]` jarayonda · `[R]` review kutyapti · `[x]` qabul qilindi

---

## Faza 0 — Skelet va CI
**Holat:** [R]

**Qilindi:**
- Loyiha tuzilmasi §5 bo'yicha: `config/` (settings split: base/dev/test/prod), `apps/` (core, users, content, contact, public, panel, api), `requirements/`, `templates/`, `static/`.
- `apps.core`: `TimeStampedModel`, `model_update`, `ApplicationError`, `get_client_ip`, `hash_ip`, `validate_phone`, `display_url` template filter.
- `apps.users.User(AbstractUser)`, `AUTH_USER_MODEL` sozlandi, birinchi migratsiya yaratildi.
- `content`, `contact`, `public`, `panel` — bo'sh `AppConfig` (modellar Faza 1/2/3 da).
- `GET /api/v1/health/` — DRF `@api_view`, DB xatosida 503 qaytaradi.
- `.importlinter` qatlam qoidalari (domen → interfeys import taqiqi, interfeyslar mustaqil).
- `pyproject.toml` (ruff, pytest), `.env.example`, `.gitignore`, `README.md` (lokal ishga tushirish).
- `.github/workflows/ci.yml`: postgres:16 service, ruff, lint-imports, makemigrations --check, pytest --cov, check --deploy.
- `conftest.py`: `staff_user`, `regular_user`, `staff_client`, `api_client` fixture'lari.

**Asosiy fayllar:**
- `apps/core/services.py` — `model_update` (spec §6.5 namunasi bilan bir xil)
- `apps/core/utils.py` — `get_client_ip` (X-Real-IP ustuvor), `hash_ip` (HMAC-SHA256)
- `apps/core/templatetags/url_tags.py` — `display_url` filtri
- `apps/api/views.py` — health endpoint
- `config/settings/base.py` — barcha umumiy sozlamalar, env orqali o'qiladi

**DoD natijasi:**
- `ruff check .` — All checks passed!
- `ruff format --check .` — barcha fayllar formatlangan
- `lint-imports` — 2 kept, 0 broken
- `makemigrations --check --dry-run` — No changes detected
- `check --deploy --fail-level WARNING` — no issues
- `pytest --cov=apps --cov-fail-under=85` — 29 passed, coverage 100%

**Spec'dan chetlanish:**
- **Docker olib tashlandi.** Sayt egasi noutbukdan Docker'ni butunlay o'chirishni so'radi. `docker-compose.yml` yaratilmadi; o'rniga kompyuterda avval o'rnatilgan **PostgreSQL 18** (native, Windows service) ishlatiladi — `.env`dagi `DATABASE_URL` shu bilan ishlaydi. Production hech qachon Docker ishlatmagan (spec TAQIQ qilgan), CI esa GitHub Actions'ning oddiy `postgres:16` service konteyneridan foydalanadi (bu foydalanuvchi kompyuteriga bog'liq emas) — demak faqat **lokal-dev qulayligi** o'zgardi, arxitektura qarori (ADR-1..13) buzilmadi.
- **Python versiyasi:** spec 3.12 talab qiladi, lokal kompyuterda **3.14** ishlatildi (sayt egasi tanlovi). CI hamon 3.12'da ishlaydi (`.github/workflows/ci.yml`), shuning uchun production/CI muvofiqligi buzilmaydi.
- **`pytest<9` pin qilindi** (`requirements/dev.txt`). Sabab: pytest 9.1.1 + pytest-django 4.14.0 kombinatsiyasi `assert not self._finalizers` ichki xatosini beradi (bir nechta test fayli birga ishlaganda). pytest 8.4.2'da muammo yo'q.
- **`docs/**` ruff'dan chiqarildi** (`pyproject.toml` `extend-exclude`). Sabab: ruff 0.16.8 endi markdown ichidagi ```python kod bloklarini ham formatlaydi; bu spec fayllarini (yagona haqiqat manbai) o'zgartirib qo'yar edi.

**Savollar (review uchun):**
- `apps/core/tests/test_services.py`da `model_update` uchun hali hech qanday konkret `TimeStampedModel` submodeli yo'q (birinchisi — `content.Project` — Faza 1'da keladi), shuning uchun test `unittest.mock.Mock` bilan yozildi (real DB model o'rniga). Faza 1'da `project_update`/`site_settings_update` orqali funksiyaning integratsiyadagi ishlashi qo'shimcha tasdiqlanadi. Roziml?
- PostgreSQL local rolega vaqtincha `CREATEDB` huquqi berildi (pytest-django test bazasini yaratishi uchun). Bu productionga ta'sir qilmaydi (production'da alohida VPS bazasi, §14).

**Ma'lum muammolar / keyinga qoldirilgan:**
- `docker-compose.yml` shu loyiha uchun umuman yaratilmaydi (yuqoridagi qarorga qarang).

**Review tuzatishlari:** (review'dan keyin to'ldiriladi)
- ...

---

## Faza 1 — Ma'lumotlar qatlami
**Holat:** [R]

**Qilindi:**
- `content.SiteSettings` (singleton, `CheckConstraint`) va `content.Project` modellari, `database.md` §3-4 bo'yicha.
- `contact.ContactMessage` modeli, §5 bo'yicha (IP xesh, rate-limit uchun index).
- Validatorlar: `content.validators` (github/telegram/linkedin URL), `contact.validators.validate_contact` (email yoki telefon).
- Selectorlar: `content.selectors` (`site_settings_get`, `project_list`, `project_get`, `project_counts`), `contact.selectors` (`message_list`, `message_get`, `message_counts`, `message_recent_count`).
- Servislar: `content.services` (`site_settings_update`, `project_create`, `project_update`, `project_delete`, `normalize_stack`), `contact.services` (`message_create` — rate-limit bilan, `message_mark_read`, `message_delete`).
- `python manage.py seed_content` — idempotent (TuitDorm + OKJ placeholder bilan).
- Migratsiyalar: `content.0001_initial`, `content.0002_create_site_settings` (data migration), `contact.0001_initial`.
- Har bir app uchun `tests/factories.py` (`make_project`, `make_message`).

**Asosiy fayllar:**
- `apps/content/services.py` — slug generatsiyasi (`slugify` + takrorlanish hisoblagichi), `normalize_stack`
- `apps/contact/services.py` — `message_create` (HMAC IP xesh, soatlik rate-limit)
- `apps/content/management/commands/seed_content.py` — `get_or_create`/`update_or_create` bilan idempotent

**DoD natijasi:**
- `ruff check .` — All checks passed!
- `ruff format --check .` — barcha fayllar formatlangan
- `lint-imports` — 2 kept, 0 broken
- `makemigrations --check --dry-run` — No changes detected
- `pytest --cov=apps --cov-fail-under=85` — 92 passed, coverage 99.72%
- `seed_content` ikki marta ishga tushirildi (lokal DB'da qo'lda ham, testda ham) — dublikat yo'q, qo'lda o'zgartirilgan `hero_line_1` saqlanib qoldi.

**Spec'dan chetlanish:**
- `project_create`da `problem`, `solution`, `role`, `stack` uchun `""` default olib tashlandi (majburiy keyword qilindi). Sabab: bu maydonlar modelda `blank=False`, shuning uchun bo'sh default bilan chaqirilsa `full_clean()` doim `ValidationError` berar edi — default amaliy jihatdan ishlamas edi. `database.md`dagi funksiya imzosida bu maydonlar uchun default ko'rsatilmagan, shuning uchun bu spec'ga zid emas, aniqlashtirish edi.

**Savollar (review uchun):**
- `validate_telegram_url` faqat host'ni tekshiradi (`t.me`), yo'lni (`/username`) tekshirmaydi — spec faqat "host t.me" deb yozgan, github/linkedin'dan farqli o'laroq yo'l talabini keltirmagan. Shunday qoldirildimi, yoki bo'sh yo'lni (`https://t.me/`) ham rad etish kerakmi?

**Ma'lum muammolar / keyinga qoldirilgan:**
- OKJ loyihasining `problem`/`role` maydonlari hali `[TO'LDIRING: ...]` placeholder holatida (`seed_content.py`) — `is_published=False`, panelda to'ldirilib yoqiladi (Faza 3).

**Review tuzatishlari:** (review'dan keyin to'ldiriladi)
- ...

---