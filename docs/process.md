# process.md

> Agent har faza oxirida shu faylni yangilaydi. Qisqa va faktlar bilan yoziladi.
> Spec fayllari (`architecture.md`, `database.md`, `component-spec.md`) bu yerda emas, review'dan keyin o'zgartiriladi.

## Holat

| Faza | Holat | Branch | Oxirgi commit |
|---|---|---|---|
| 0 — Skelet va CI | [ ] | `phase-0-scaffold` | |
| 1 — Ma'lumotlar qatlami | [ ] | `phase-1-data` | |
| 2 — Ochiq sayt | [ ] | `phase-2-public` | |
| 3 — Panel | [ ] | `phase-3-panel` | |
| 4 — API | [ ] | `phase-4-api` | |
| 5 — Production | [ ] | `phase-5-prod` | |
| 6 — Bildirishnoma va backup (ixtiyoriy) | [ ] | `phase-6-extras` | |

Belgilar: `[ ]` boshlanmagan · `[~]` jarayonda · `[R]` review kutyapti · `[x]` qabul qilindi

---

## Shablon (har faza uchun nusxa olinadi)

### Faza N — nomi
**Holat:** [R]

**Qilindi:**
- ...

**Asosiy fayllar:**
- `path/to/file.py` — nima uchun

**DoD natijasi:**
- `ruff check .` — 
- `ruff format --check .` — 
- `lint-imports` — 
- `makemigrations --check` — 
- `pytest` — N passed, coverage X%

**Spec'dan chetlanish:** yo'q / [nima — nega]

**Savollar (review uchun):**
- ...

**Ma'lum muammolar / keyinga qoldirilgan:**
- ...

**Review tuzatishlari:** (review'dan keyin to'ldiriladi)
- ...

---