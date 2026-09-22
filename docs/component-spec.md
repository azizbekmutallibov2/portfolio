# Portfolio — UI spetsifikatsiyasi (v1)

Vizual reference: `docs/design/*.dc.html` (Main = desktop 1440, Site-Mobile = 390, Admin-*).
Ulardagi `<x-dc>`, `<helmet>`, `<sc-for>`, `<sc-if>`, `{{...}}`, `support.js` — dizayn vositasi sintaksisi, **ko'chirilmaydi**. O'lcham, bo'shliq va ranglar shu fayllardan; **matn va kontent manbai — shu hujjat va `database.md`**, design fayllar emas (ularda eski placeholder'lar bor).

Umumiy qoidalar:
- Inline `style=""` va inline `<script>` TAQIQ (CSP). Hamma stil `static/css/`da.
- Build tool yo'q. CSS custom properties, flexbox/grid. Class nomlari — BEM-lite (`.project`, `.project__title`, `.btn--primary`).
- JS'siz ham hammasi ishlaydi (tema dark bo'lib qoladi, toggle yashiriladi).
- `border-radius: 0` hamma joyda (pulse nuqtasidan tashqari). Soya (shadow) yo'q.

---

## 1. Tokenlar — `static/css/tokens.css`

```css
:root,
[data-theme="dark"] {
  color-scheme: dark;
  --bg: #0A0A0A;
  --surface: #111111;
  --line: #262626;
  --fg: #EDEDED;
  --fg-2: #A3A3A3;
  --fg-3: #8A8A8A;
  --inverse: #EDEDED;
  --on-inverse: #0A0A0A;
  --accent: #34D399;
  --danger: #F87171;
}
[data-theme="light"] {
  color-scheme: light;
  --bg: #FAFAFA;
  --surface: #FFFFFF;
  --line: #E2E2E2;
  --fg: #0A0A0A;
  --fg-2: #525252;
  --fg-3: #6B6B6B;
  --inverse: #0A0A0A;
  --on-inverse: #FAFAFA;
  --accent: #065F46;
  --danger: #B91C1C;
}
:root {
  --font-sans: "Geist", system-ui, -apple-system, "Segoe UI", sans-serif;
  --font-mono: "Geist Mono", ui-monospace, Menlo, Consolas, monospace;
  --ease-out: cubic-bezier(.2, .7, .2, 1);
  --pad-x: 20px;          /* <768 */
  --section-y: 64px;
}
@media (min-width: 768px)  { :root { --pad-x: 32px; } }
@media (min-width: 1024px) { :root { --pad-x: 48px; --section-y: 96px; } }
```
Kontrast tekshirilgan (WCAG AA): `fg-3`, `accent`, `danger` ikkala temada ham ≥ 4.5:1.

## 2. Tipografiya

| Rol | Desktop (≥1024) | Mobil (<768) | Qolgani |
|---|---|---|---|
| Display (hero h1) | 120px | 56px | `clamp(3.5rem, 2.014rem + 6.095vw, 7.5rem)`, lh .96, ls -0.055em, 600 |
| Panel login display | 96px | yashiriladi | lh .96, ls -0.055em, 600 |
| H2 bo'lim | 56px | 40px | `clamp(2.5rem, 2.129rem + 1.524vw, 3.5rem)`, lh 1, ls -0.045em, 600 |
| Panel H1 | 56px | 40px | ls -0.05em, 600 |
| H3 loyiha nomi | 34px | 28px | lh 1.05, ls -0.04em, 600 |
| Lead | 18px | 16px | lh 1.55, `--fg-2`, max-width 560–640px |
| Body | 15px | 15px | lh 1.65, `--fg-2` |
| Label | 11–12px mono | 10–11px mono | uppercase, ls .06–.08em, `--fg-3` |
| Mono data | 13–14px | 12–13px | `--font-mono` |

Shriftlar: `<link rel="preconnect" href="https://fonts.googleapis.com">`, `<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>`, `family=Geist:wght@300..800&family=Geist+Mono:wght@400;500&display=swap`. `body { -webkit-font-smoothing: antialiased; }`.

## 3. Layout

- Konteyner: `max-width: 1440px; margin-inline: auto; padding-inline: var(--pad-x)`.
- Bo'lim: `padding-block: var(--section-y); border-top: 1px solid var(--line)`.
- Bo'lim grid (≥1024): `grid-template-columns: 192px minmax(0, 1fr); gap: 48px` — chapda label (`01 / LOYIHALAR`), o'ngda kontent. <1024: label sarlavha ustida, `margin-bottom: 20px`.
- Breakpoint'lar: `<768` mobil, `768–1023` planshet (mobil layout, kengroq padding), `≥1024` desktop.

## 4. Komponentlar

| Komponent | Spec |
|---|---|
| `.btn` | inline-flex, gap 10px, height 44px (mobil 48px), padding 0 20px, 500 14px sans, border 1px `--line`, fon shaffof; hover: border `--fg`; transition .2s |
| `.btn--primary` | fon `--inverse`, rang `--on-inverse`, border `--inverse`; hover: opacity .86 |
| `.tag` | mono 11px (mobil 10px), ls .06em, rang/border `--accent`, padding 3px 8px |
| `.label` | mono, uppercase, 11px, ls .08em, `--fg-3` |
| `.link` | rang `--fg`, border-bottom 1px `--line`, padding-bottom 2px; hover: border va rang `--accent` |
| `.row-hover` | hover: fon `--surface`, transition .25s; ichidagi `.arrow` → `translateX(4px)` |
| `.field` | label (`.label`) + input. Input: to'liq kenglik, fon shaffof, border faqat pastda 1px `--line`, radius 0, 400 16px sans, padding 10px 0 12px; focus: border `--fg`, outline yo'q; placeholder `--fg-3` |
| `.field--error` | input border `--danger`, `aria-invalid="true"`; ostida `.field__error` mono 12px `--danger`, `id` bilan `aria-describedby` |
| `select` | `.field` input kabi + `appearance: none` + o'ng tomonda `▾` (CSS background emas — `::after` wrapper'da) |
| checkbox | native, `accent-color: var(--accent)`, label yonida 14px |
| `.flash` | mono 13px, padding 14px 0, border-bottom 1px `--line`; success — `--accent`, error — `--danger`; `role="status"` |
| `.theme-toggle` | §5 |
| `.pulse-dot` | 7×7px, radius 50%, fon `--accent`, animatsiya `pulse 2.4s ease-in-out infinite` (50% → opacity .3) |
| `.cursor` | 8×15px (mobil 7×13), fon `--fg`, `cur 1.1s steps(1) infinite` |
| `:focus-visible` | `outline: 1px solid var(--accent); outline-offset: 3px` |

`components/_field.html` — label, input, xato va help matnini bitta joyda render qiladi: `{% include "components/_field.html" with field=form.name %}`. Widget class'lari forma `__init__`da beriladi, templateda emas.

## 5. Tema

- `<html lang="uz" class="no-js" data-theme="dark">` server tomonda.
- `static/js/theme-init.js` — `<head>`da, **birinchi**, sinxron (`defer`siz): `localStorage.theme` ∈ {dark, light} bo'lsa `data-theme`ga qo'yadi; `no-js` → `js`. `try/catch` bilan.
- `static/js/theme.js` (`defer`): `[data-theme-toggle]` bosilganda temani almashtiradi, `localStorage`ga yozadi, `aria-pressed`ni yangilaydi (light = `true`).
- Markup:
```html
<button type="button" class="theme-toggle" data-theme-toggle aria-pressed="false">
  <span class="visually-hidden">Light rejim</span>
  <span class="theme-toggle__opt theme-toggle__opt--dark" aria-hidden="true">DARK</span>
  <span class="theme-toggle__opt theme-toggle__opt--light" aria-hidden="true">LIGHT</span>
</button>
```
- CSS: height 32px (mobil 36px), border 1px `--line`, mono 500 11px ls .06em `--fg-3`; `.theme-toggle__opt` padding 0 10px; faol variant (`[data-theme="dark"] …--dark`, `[data-theme="light"] …--light`) fon `--inverse`, rang `--on-inverse`. `.no-js .theme-toggle { display: none; }`.
- Default — dark (tizim sozlamasiga qaralmaydi).

## 6. Harakat

| Nima | Qayerda | Spec |
|---|---|---|
| `fade` | faqat hero va panel sarlavhalari | .9s `--ease-out`, `translateY(8px)` → 0; kechikishlar `.d1` .08s, `.d2` .16s, `.d3` .24s |
| `pulse` | hero "Hozir" nuqtasi | §4 |
| `cur` | infra log kursori | §4 |
| `flow` / `vflow` | infra sim'lari | 5×5px `--accent` kvadrat, 3.2s linear infinite, 0→15% opacity 1, 85%→100% opacity 0; desktop gorizontal (40px sim, 0→35px), mobil vertikal (24px sim, 0→19px) |
| smooth scroll | `html` | faqat `@media (prefers-reduced-motion: no-preference)` ichida |

`@media (prefers-reduced-motion: reduce)` — barcha animatsiyalar `none`.

---

## 7. Ochiq sayt — `templates/public/home.html`

Tuzilma: skip link (`Asosiy kontentga o'tish` → `#main`, fokusda ko'rinadi) → `<header>` → `<main id="main">` (6 ta `<section aria-labelledby>`) → `<footer>`. Faqat bitta `<h1>`.

### 7.1 Header (`partials/_header.html`)
- **Desktop:** height 64px, border-bottom. Chapda `azizillo` (16px/600/-0.02em) + mono 12px `--fg-3` `/ backend`. O'ngda `<nav aria-label="Asosiy">` (gap 32px; 13px sans `--fg-2`, hover `--accent`): Loyihalar `#projects`, Stack `#stack`, Infra `#infra`, Aloqa `#contact`; nav bilan toggle orasi 40px.
- **Mobil:** 1-qator 56px — logo + toggle. 2-qator — nav, border-top, `justify-content: space-between`, har link 44px baland, mono 12px ls .02em.
- Sticky emas.

### 7.2 Hero (`_hero.html`) — `SiteSettings`dan
- Desktop `min-height: 700px`, mobil 560px; `display: flex; flex-direction: column`.
- Meta qator: mono 12px ls .06em `--fg-3`, padding 24px 0, border-bottom; chapda `PYTHON BACKEND DASTURCHI`, o'ngda `TOSHKENT, O'ZBEKISTON`. Mobil: 11px, 18px 0, `PYTHON BACKEND` / `TOSHKENT`.
- H1 (pastga tekislangan, `flex: 1; justify-content: flex-end`, padding-bottom 56px / mobil 36px): `<span>` blok `hero_line_1` (`--fg`) va `<span>` blok `hero_line_2` (`--fg-2`).
- **Desktop pastki grid** — 3 ustun, border-top, ustunlar orasida border-left, padding `28px 32px 36px` (birinchisi chapdan 0, oxirgisi o'ngdan 0), ichida gap 14px:
  1. `KIM` label + `about_text` (17px lh 1.55 `--fg-2`)
  2. `HOZIR` label + pulse nuqta (margin-top 9px) + `status_text` (17px `--fg`)
  3. `BOSHLASH` label + `Loyihalarni ko'rish ↓` (primary, `#projects`) + `Aloqa` (`#contact`), gap 12px
- **Mobil:** border-top, padding 20px 0 28px, ustun gap 20px: `about_text` (16px) → pulse + `Hozir: {{ status_text }}` (15px `--fg`) → primary tugma to'liq kenglik. Label'lar yo'q, `Aloqa` tugmasi yo'q.
- Fade: meta `.fade`, h1 `.fade.d1`, pastki blok `.fade.d2`.

### 7.3 Loyihalar (`_projects.html`) — `id="projects"`, label `01 / LOYIHALAR`
- H2 `Loyihalar`; lead `Har biri uchun: qanday muammo bor edi, nima qurdim va mening rolim nima.`
- Ro'yxat `<ol>`: margin-top 56px (mobil 36px); tashqi border 1px `--line` (pastisiz); har `<li class="project row-hover">` border-bottom.
- **Desktop qator:** flex, gap 48px, padding 40px.
  - Chap ustun 240px, gap 20px: [indeks `01` mono 12px `--fg-3` + `.tag` (`get_tag_display`)] gap 12px → `<h3>` title.
  - O'ng: 2×2 grid, gap 32px 40px: `MUAMMO` / `YECHIM` / `MENING ROLIM` (15px lh 1.65 `--fg-2`) / `STACK` (mono 14px `--fg`, `stack_items|join:" · "`). Har blok: label + matn, gap 10px.
  - Havolalar qatori: margin-top 32px, padding-top 24px, border-top, mono 13px, gap 32px: `GitHub <span class="arrow">→</span> {{ repo_url|display_url }}` va `Demo → {{ demo_url|display_url }}`. URL bo'sh bo'lsa o'sha havola **render qilinmaydi**; ikkalasi ham bo'sh bo'lsa qator yo'q. `target="_blank" rel="noopener noreferrer"`.
- **Mobil:** padding 24px 20px 28px, vertikal gap 24px; h3 28px; bloklar gap 8px, matn 15px lh 1.6; stack mono 13px; havolalar vertikal, gap 14px, mono 12px, `align-self: flex-start`.
- Indeks: `{{ forloop.counter|stringformat:"02d" }}`.
- **Bo'sh holat:** bitta qator, padding 32px 40px, mono 13px `--fg-3`: `Loyihalar tez orada qo'shiladi.`

### 7.4 Stack (`_stack.html`) — `id="stack"`, label `02 / STACK`
- H2 `Stack`; lead `Kundalik ishlatadigan vositalar, qatlamlar bo'yicha.`
- Semantik `<table>`: margin-top 56px, border-top. Desktop: `thead` mono 11px ls .08em `--fg-3` (`QATLAM` / `TEXNOLOGIYA` / `IZOH`), padding 14px 0; qatorlar grid `220px 1fr 1fr`, gap 24px, `align-items: baseline`, padding 22px 0, border-bottom, `.row-hover`. Qatlam mono 12px `--fg-3`; texnologiya 22px/500/-0.02em; izoh 15px `--fg-2`.
- Mobil: `thead` vizual yashirin; `tr` blok, padding 18px 0, gap 6px; texnologiya 20px, izoh 14px.
- Ma'lumot `static_content.STACK`:

| layer | tech | note |
|---|---|---|
| TIL | Python | Asosiy til, backend uchun. |
| FRAMEWORK | Django, Django REST Framework | REST API, services/selectors arxitekturasi. |
| MA'LUMOTLAR BAZASI | PostgreSQL | TuitDorm va shu saytning bazasi. |
| SERVER | Nginx, Gunicorn, systemd, PM2 | Reverse proxy va WSGI; Python servislar — systemd, Node servislar — PM2. |
| INFRA | Ubuntu VPS (WebDock) | Serverni o'zim sozlaganman va yuritaman. |
| FRONTEND | Next.js | OKJ platformasida, App Router bilan. |
| VOSITALAR | Git, Docker, Linux | Versiyalash, konteynerlar, buyruq qatori. |

### 7.5 Infra (`_infra.html`) — `id="infra"`, label `03 / INFRA`
- H2 `Infra / Deployment`; lead (max 640px): `So'rov mijozdan bazagacha shu yo'ldan o'tadi. Shu sayt ham aynan shu yo'lda ishlaydi — server WebDock'dagi Ubuntu VPS, uni o'zim sozlaganman.`
- **Diagramma** — `<ol aria-label="So'rov yo'li">`, sim'lar `aria-hidden="true"`:
  - Desktop (margin-top 56px, flex, stretch): Client tuguni (150px) → sim → punktir ramka (`1px dashed --line`, padding 36px 20px 20px, `position: relative`, chap-yuqorida mono 11px ls .08em `UBUNTU VPS · WEBDOCK`) ichida 4 tugun, orasida sim. Tugun: border 1px `--line`, fon `--bg`, padding 20px, `flex: 1`, vertikal `space-between`, gap 20px; indeks mono 12px `--fg-3`; nom 18px/500 (Client 20px); izoh mono 11px `--fg-3`; hover border `--fg`.
  - Mobil: vertikal. Tugun — qator (nom + izoh chapda, indeks o'ngda), padding 16px 20px, nom 18px. Sim — 1×24px, margin-left 24px. Ramka padding 34px 12px 12px, label 10px.
- Tugunlar (`static_content.INFRA_NODES`):

| idx | name | sub | ramka ichida |
|---|---|---|---|
| 01 | Client | brauzer / mobil | yo'q |
| 02 | Nginx | TLS · reverse proxy | ha |
| 03 | Gunicorn | WSGI · systemd | ha |
| 04 | Django | services · selectors | ha |
| 05 | PostgreSQL | ma'lumotlar bazasi | ha |

- **Pastda 2 ustun** (desktop grid, gap 48px, margin-top 48px; mobil ustma-ust, oraliq 36px):
  1. Sarlavha qatori (mono 11px ls .08em `--fg-3`, padding-bottom 14px, border-bottom): `API ENDPOINTLAR` / `SHU SAYT`. Qatorlar mono 13px, padding 16px 0, border-bottom, `.row-hover`: method (64px, `--fg-3`) · path (`--fg`) · izoh (`--fg-3`). Mobil: 12px, method 44px, izoh yashirin, path `word-break: break-all`.
  2. Sarlavha `SO'ROV YO'LI` / `LOG`. Log mono 13px lh 2 (mobil 12px lh 1.9): `who` (76px / mobil 64px, `--fg-3`) + `msg` (`--fg-2`). Oxirida `$ ` + `.cursor`.
- `static_content.INFRA_ENDPOINTS` (`url_name` — guard test uchun):

| method | path | note | url_name |
|---|---|---|---|
| GET | `/api/v1/projects/` | ro'yxat | `api:project-list` |
| GET | `/api/v1/projects/{slug}/` | bitta loyiha | `api:project-detail` |
| POST | `/api/v1/contact/` | xabar | `api:contact-create` |
| GET | `/api/v1/health/` | holat | `api:health` |

- `static_content.INFRA_LOGS` (`{host}` → templateda `request.get_host`):

| who | msg |
|---|---|
| client | `→ GET https://{host}/api/v1/projects/` |
| nginx | `→ TLS, proxy_pass → unix socket` |
| gunicorn | `→ systemd boshqaradigan worker` |
| django | `→ api → selector → ORM` |
| postgres | `→ SELECT … FROM content_project` |
| client | `← 200 JSON` |

### 7.6 Ta'lim (`_education.html`) — `id="education"`, label `04 / TA'LIM`
- H2 `Ta'lim` (margin-bottom 56px / mobil 36px), border-top ro'yxat. Desktop qator: flex, gap 48px, padding 28px 0, border-bottom, `.row-hover`; `when` mono 12px ls .06em `--fg-3`, 160px, padding-top 6px; title 24px/500/-0.025em; sub 15px `--fg-2`, margin-top 6px. Mobil: vertikal, gap 8px, padding 22px 0, title 22px, sub 14px.
- `static_content.EDUCATION`:

| when | title | sub |
|---|---|---|
| HOZIR · 1-KURS | TATU | Toshkent Axborot Texnologiyalari Universiteti — Software Engineering. |
| HOZIR | Najot Ta'lim | Python backend yo'nalishi. |

### 7.7 Profillar (`_profiles.html`) — `id="profiles"`, label `05 / PROFILLAR`
- Vizual H2 yo'q → `<h2 class="visually-hidden">Profillar</h2>`.
- `SiteSettings` havolalaridan: GitHub, Telegram, LinkedIn (shu tartibda). Bo'sh URL → qator yo'q; hammasi bo'sh → bo'lim umuman render qilinmaydi (header nav'da uning linki yo'q, shuning uchun muammo yo'q).
- Desktop qator (`<a class="row-hover">`, padding 26px 0, border-bottom): chapda nom 32px/600/-0.04em; o'ngda `{{ url|display_url }}` mono 13px `--fg-3` + `.arrow` (`--fg`), gap 20px. Mobil: vertikal, min-height 72px, padding 14px 0, nom 24px + `→` mono 14px, handle mono 12px.
- `target="_blank" rel="noopener noreferrer"`.

### 7.8 Aloqa (`_contact.html`) — `id="contact"`, label `06 / ALOQA`
- **Desktop:** 2 ustun, gap 96px.
  - Chap (gap 48px): H2 `Loyiha yoki ish taklifi bormi?`; keyin (gap 28px) `TELEFON` → `<a href="tel:...">` 26px ls -0.02em; `EMAIL` → `<a href="mailto:...">` 26px. Bo'sh bo'lsa o'sha blok yo'q.
  - O'ng: `<form method="post" action="{% url 'public:contact' %}#contact" novalidate>` + `{% csrf_token %}`, maydonlar orasi 28px:
    - `ISM` — `name`, `autocomplete="name"`, `maxlength="100"`, placeholder `Ismingiz`
    - `TELEFON YOKI EMAIL` — `contact`, `maxlength="150"`, placeholder `+998 ... yoki email`
    - `XABAR` — `message`, `<textarea rows="4">`, `maxlength="2000"`, placeholder `Nima haqida?`, `resize: none`
    - honeypot `website` — `.visually-hidden` wrapper ichida, `tabindex="-1"`, `autocomplete="off"`, label `Bu maydonni bo'sh qoldiring`
    - `Yuborish →` (primary, `type="submit"`)
  - Umumiy xato (rate-limit) — tugma ustida `.flash` error.
  - Muvaffaqiyat — forma ustida `.flash` success: `Xabaringiz yuborildi. Tez orada javob beraman.`
- **Mobil:** bitta ustun, gap 36px; H2 40px; telefon/email 22px; maydonlar orasi 24px; tugma to'liq kenglik.
- Forma xatolari (Django `uz` + o'zimizniki): majburiy maydon — Django standart matni; ism < 2 — `Ism kamida 2 ta harf bo'lsin.`; xabar < 10 — `Xabar kamida 10 ta belgidan iborat bo'lsin.`; contact — `Telefon raqam yoki email kiriting.`

### 7.9 Footer (`_footer.html`)
- Mono 12px `--fg-3`, border-top. Desktop: height 72px, 3 element `space-between`: `© {% now "Y" %} Azizillo` · `Toshkent, O'zbekiston` · `Yuqoriga ↑` (`.link`, `#top`; `<body id="top">`).
- Mobil: padding 22px 20px 28px, 2 qator (gap 14px): [© · Toshkent] va [Yuqoriga ↑ o'ngda].
- **Panel havolasi yo'q.**

### 7.10 Meta (`base.html`)
- `<title>Azizillo — Python backend dasturchi</title>`
- `<meta name="description" content="Azizillo — Python backend dasturchi. Django, DRF, PostgreSQL, Nginx: loyihalar, stack va deployment.">`
- `<link rel="canonical" href="https://{{ request.get_host }}/">`, `og:title`, `og:description`, `og:type=website`, `og:url`, `og:locale=uz_UZ`. `og:image` — v1'da yo'q.
- `<meta name="color-scheme" content="dark light">`, `<link rel="icon" href="{% static 'img/favicon.svg' %}" type="image/svg+xml">` — favicon: 32×32 qora kvadrat, markazda 10×10 `#34D399` kvadrat.
- Panel sahifalarida `<meta name="robots" content="noindex, nofollow">`.

---

## 8. Panel

### 8.1 Login (`panel/login.html`)
- **Desktop:** ikki yarim. Chap (50%, border-right, padding 40px 48px, vertikal `space-between`): yuqorida `azizillo / admin`; o'rtada label `BOSHQARUV PANELI` (margin-bottom 24px) + display 96px: `Kontent.` (`--fg`) / `Xabarlar.` (`--fg-2`), `.fade`; pastda mono 12px `--fg-3` `Faqat sayt egasi uchun.`
- O'ng: yuqori-o'ngda toggle (72px qator); markazda 400px ustun (`.fade.d1`), gap 32px: H1 `Kirish` 36px + `Admin panelga kirish uchun ma'lumotlarni kiriting.` (15px `--fg-2`); `LOGIN` (`autocomplete="username"`), `PAROL` (`type="password"`, `autocomplete="current-password"`), gap 24px; `Kirish →` primary to'liq kenglik; `← Saytga qaytish` (`.link` mono 12px).
- Xato — tugma ustida `.flash` error: `Login yoki parol noto'g'ri.` (staff bo'lmagan user uchun ham aynan shu matn).
- **<1024:** chap yarim yashirin; forma to'liq kenglik (max 400px), padding `var(--pad-x)`; toggle yuqorida.

### 8.2 Shell (`panel/base_panel.html`)
- **Desktop:** chapda sidebar 240px (border-right, balandligi 100vh, sticky):
  - 64px qator: `azizillo / admin`, border-bottom.
  - Nav (padding-top 16px): `Dashboard` → `panel:dashboard`; `Xabarlar` → `panel:messages`; `Loyihalar` → `panel:content#projects`; `Profil havolalari` → `panel:content#links`; `Hero matni` → `panel:content#hero`.
  - Pastda (margin-top auto, border-top, padding 8px 0): `Saytga qaytish` → `/`; `Chiqish` — `<form method="post" action="{% url 'panel:logout' %}">` ichidagi tugma, nav link ko'rinishida.
  - Nav elementi: height 44px, padding 0 24px, 14px `--fg-2`, border-left 1px shaffof; hover — fon `--surface`, rang `--fg`; faol (`aria-current="page"`) — rang `--fg`, fon `--surface`, border-left `--fg`. Faollik: dashboard → Dashboard; xabarlar sahifalari → Xabarlar; content va loyiha sahifalari → Loyihalar.
- Topbar 64px (padding 0 48px, border-bottom): breadcrumb mono 12px ls .06em `--fg-3` (`ADMIN / DASHBOARD`, `ADMIN / XABARLAR`, `ADMIN / XABARLAR / #12`, `ADMIN / KONTENT`) + toggle.
- Kontent: padding 48px, vertikal gap 48px (content sahifasida 40px); H1 56px `.fade`. Flash xabarlar H1 ostida.
- **<1024:** sidebar → yuqori panel: 56px qator (logo + toggle), ostida gorizontal skroll qilinadigan nav (`overflow-x: auto`, element 44px); "Saytga qaytish" va "Chiqish" nav oxirida. Topbar breadcrumb'siz. Kontent padding `var(--pad-x)`, H1 40px.

### 8.3 Dashboard (`panel/dashboard.html`)
- H1 `Dashboard`.
- Stat grid (`.fade.d1`): 2 ustun, border 1px, ikkinchisi border-left; katak padding 28px 32px, gap 24px:
  - `KELGAN XABARLAR` → `total` (64px/600/-0.05em); ostida mono 12px `--accent` `{{ unread }} ta o'qilmagan` (0 bo'lsa `--fg-3` `Hammasi o'qilgan`).
  - `LOYIHALAR` → `total`; ostida mono 12px `--fg-3` `{{ published }} tasi saytda`.
  - <768: 1 ustun, ikkinchisi border-top.
- Oxirgi xabarlar (`.fade.d2`): sarlavha qatori (padding-bottom 16px) — label `SO'NGGI XABARLAR` + o'ngda `Barcha xabarlar →` (`.btn`, `panel:messages`) va `Loyihalarni boshqarish →` (`.btn`, `panel:content`), gap 12px.
- Jadval — `partials/_messages_table.html` (§8.4), oxirgi 10 ta.

### 8.4 Xabarlar jadvali (`partials/_messages_table.html`) va ro'yxat (`panel/messages_list.html`)
- Desktop: border-top; sarlavha qatori mono 11px ls .08em `--fg-3`, padding 14px 0: `ISM` / `TELEFON / EMAIL` / `XABAR` / `VAQT`; grid `200px 240px minmax(0,1fr) 120px`, gap 24px.
- Qator — butunlay `<a>` (`panel:message-detail`), `.row-hover`, padding 20px 0, border-bottom, 14px: ism (`--fg`; o'qilmagan bo'lsa oldida 6×6 `--accent` nuqta va weight 500, `<span class="visually-hidden">O'qilmagan</span>`); contact mono 13px `--fg-2`; body `--fg-2` bir qator ellipsis; vaqt mono 12px `--fg-3` `d.m.Y H:i`.
- Mobil: sarlavha qatori yashirin; qator — blok, padding 16px 0: 1-qator ism + vaqt (`space-between`), 2-qator contact mono 12px, 3-qator body 2 qatorli clamp.
- Bo'sh: mono 13px `--fg-3` `Hali xabar yo'q.`
- Ro'yxat sahifasi: H1 `Xabarlar`, jadval, ostida sahifalash: mono 13px, `← Oldingi` · `2 / 5` · `Keyingi →` (`.link`); yo'q bo'lgan tomon ko'rsatilmaydi. 20 ta/sahifa, `Paginator.get_page`.

### 8.5 Xabar (`panel/message_detail.html`)
- H1 — xabar egasining ismi (40px). Ostida 3 ustunli meta (mobil vertikal), har biri label + qiymat: `ALOQA` (email → `mailto:`, telefon → `tel:`, `.link`), `VAQT` (`d.m.Y H:i`), `HOLAT` (`O'qilgan`).
- `XABAR` label + matn 17px lh 1.65 `--fg`, `white-space: pre-wrap`, max-width 720px.
- Amallar (gap 12px): `← Xabarlarga qaytish` (`.btn`); `O'chirish` — `<form method="post" data-confirm="Xabar o'chirilsinmi?">` ichidagi `.btn`, hover'da border va rang `--danger`.

### 8.6 Kontent (`panel/content.html`)
- H1 `Kontent`. Grid `minmax(0,5fr) minmax(0,7fr)`, gap 48px (`.fade.d1`); <1024 — 1 ustun (tartib: hero, havolalar, loyihalar, forma).
- **Chap ustun** (gap 40px), har karta: label-sarlavha (padding-bottom 12px, border-bottom) + maydonlar (gap 22px) + `Saqlash` (primary):
  - `id="hero"` — `HERO MATNI`: `SARLAVHA, 1-QATOR`, `SARLAVHA, 2-QATOR`, `KIM (QISQA MA'LUMOT)` (textarea 3), `HOZIR NIMA USTIDA`. POST → `panel:hero-update`.
  - `id="links"` — `PROFIL HAVOLALARI VA ALOQA`: `GITHUB` (placeholder `github.com/username`), `TELEGRAM` (`t.me/username`), `LINKEDIN` (`linkedin.com/in/username`), `EMAIL`, `TELEFON`. Sxemasiz URL forma `clean_*`da `https://` bilan to'ldiriladi. POST → `panel:links-update`.
- **O'ng ustun** (gap 40px):
  - `id="projects"` — sarlavha qatori: label `LOYIHALAR` + `+ Loyiha qo'shish` (`.btn`, `href="{% url 'panel:content' %}#project-form"`). Ro'yxat border-top; qator (`.row-hover`, flex, gap 24px, padding 20px 0, border-bottom): indeks mono 12px 28px; nom 18px/500 + ostida stack mono 12px `--fg-3`; unpublished bo'lsa nom yonida `.tag` `--fg-3` rangda `YASHIRIN`; amallar — `Tahrirlash` (`<a>` → `panel:project-edit`) va `O'chirish` (`<form method="post" data-confirm="Loyiha o'chirilsinmi?">`). Amal tugmasi `.action`: shaffof, border faqat pastda 1px `--line`, height 32px, mono 12px `--fg-2`; hover rang va border `--fg`.
  - Bo'sh: `Hali loyiha yo'q.`
  - `id="project-form"` — sarlavha `YANGI LOYIHA` yoki `TAHRIRLASH · {{ project.title|upper }}`. 2 ustunli grid, gap 20px 32px (mobil 1 ustun):
    - `NOM` · `TEG` (select)
    - `STACK` (help: `Vergul bilan ajrating: Django, PostgreSQL, Nginx`) · `TARTIB` (number, min 0)
    - `MUAMMO` (textarea 3) · `YECHIM` (textarea 3)
    - `MENING ROLIM` (textarea 2) · `SAYTDA KO'RSATISH` (checkbox)
    - `GITHUB HAVOLA` · `DEMO HAVOLA`
  - Tugmalar (gap 12px): `Saqlash` (primary) · `Bekor qilish` (`.btn`, `panel:content`, faqat tahrirlashda).
- Flash matnlari: `Hero matni saqlandi.` · `Havolalar saqlandi.` · `Loyiha qo'shildi.` · `Loyiha saqlandi.` · `Loyiha o'chirildi.` · `Xabar o'chirildi.` · o'zgarish bo'lmasa `O'zgarish yo'q.`

### 8.7 `static/js/panel.js`
Faqat bitta vazifa: `document.addEventListener("submit", ...)` — `data-confirm` atributi bor formada `window.confirm(msg)` false bo'lsa `preventDefault()`.

---

## 9. Xato sahifalari
- `404.html` (base'ni extend qiladi): markazda display `404` (desktop 120px), ostida `Sahifa topilmadi.` (18px `--fg-2`), `← Bosh sahifa` (`.link`).
- `403.html`: `403` / `Bu sahifaga ruxsat yo'q.`
- `403_csrf.html`: `Sahifa eskirdi.` / `Sahifani yangilab, qayta yuboring.`
- `500.html`: **mustaqil** HTML (base'siz, request'siz), faqat `{% load static %}` va CSS fayllari: `500` / `Serverda xatolik. Birozdan keyin qayta urinib ko'ring.`

## 10. Accessibility (SHART)
- `lang="uz"`, skip link, landmark'lar (`header`, `nav`, `main`, `footer`), bitta `h1`, bo'limlar `aria-labelledby`.
- Barcha input'larda `<label for>`; xatolar `aria-invalid` + `aria-describedby`; flash `role="status"`.
- Mobil tap maydoni ≥ 44px.
- Dekorativ belgilar (`→`, `↓`, sim'lar, nuqtalar) `aria-hidden="true"`.
- Faqat klaviatura bilan butun sayt va panel ishlatiladi; `:focus-visible` ko'rinadi.

## 11. Dizayndan chetlanishlar (ataylab)
1. Infra: `Gunicorn / PM2` → `Gunicorn · WSGI · systemd` (ADR-7). Stack jadvalida PM2 qoladi (Node servislar uchun).
2. Infra endpointlari va log — OKJ'niki emas, **shu saytning real API'si**; guard test bilan kafolatlangan.
3. Saytdagi `[YANGI LOYIHA] — admin paneldan qo'shiladi` qatori olib tashlandi.
4. Footer'dagi `Admin` havolasi olib tashlandi.
5. Ta'lim: `MAQSAD — MAANG` qatori olib tashlandi (qaytarish — `static_content.EDUCATION`ga bitta qator).
6. Bo'sh havolalar (repo, demo, profil, telefon, email) placeholder o'rniga umuman ko'rsatilmaydi.
7. Panel: `HAVOLALAR` bitta maydon o'rniga `GITHUB HAVOLA` + `DEMO HAVOLA`; qo'shildi `TEG`, `TARTIB`, `SAYTDA KO'RSATISH`.
8. Panel: hero formasiga `KIM`, havolalar formasiga `EMAIL` va `TELEFON` qo'shildi.
9. Panel: `Xabarlar` ro'yxati va xabar sahifasi qo'shildi (dizaynda faqat dashboard jadvali bor edi, uzun xabarni o'qib bo'lmasdi).
10. Dashboard: o'qilmagan / saytdagi soni qo'shildi.
11. Panel mobil ko'rinishi, bo'sh/xato/muvaffaqiyat holatlari — dizaynda yo'q edi, shu hujjatda belgilandi.
12. Infra lead matniga "Shu sayt ham aynan shu yo'lda ishlaydi" qo'shildi.

## 12. Qo'lda QA ro'yxati (har UI fazasi oxirida)
- [ ] Kenglik 390, 768, 1024, 1440 px — gorizontal skroll yo'q.
- [ ] Dark va light; sahifa yangilanganda tanlov saqlanadi; yuklanishda "miltillash" yo'q.
- [ ] JS o'chiq: sayt ishlaydi, toggle ko'rinmaydi, forma yuboriladi.
- [ ] `prefers-reduced-motion: reduce` — animatsiya yo'q.
- [ ] Faqat klaviatura: skip link, nav, forma, panel.
- [ ] Uzun loyiha nomi, 0 loyiha, bo'sh havolalar, 2000 belgili xabar.
- [ ] 404 va 500 sahifalari (`DEBUG=False` bilan).
- [ ] Brauzer konsolida CSP xatosi yo'q (Faza 5 dan keyin).