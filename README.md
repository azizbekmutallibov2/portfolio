# Portfolio

Shaxsiy portfolio sayti. Arxitektura va spetsifikatsiya: [`docs/`](docs/) papkasida
(`architecture.md`, `database.md`, `component-spec.md`, `process.md`).

## Lokal ishga tushirish

Talab qilinadi: Python 3.12+, PostgreSQL 16+ (mahalliy o'rnatilgan, Docker ishlatilmaydi — sabab
`docs/process.md`da yozilgan).

```bash
python -m venv venv
source venv/Scripts/activate      # Windows Git Bash
# yoki: venv\Scripts\activate.bat  # Windows cmd.exe

pip install -r requirements/dev.txt
cp .env.example .env
```

PostgreSQL'da quyidagi database va foydalanuvchi mavjud bo'lishi kerak (`.env`dagi
`DATABASE_URL` shu bilan mos):

```sql
CREATE ROLE portfolio LOGIN PASSWORD 'portfolio';
CREATE DATABASE portfolio OWNER portfolio;
```

```bash
python manage.py migrate
pytest
python manage.py runserver
```

Brauzerda [http://127.0.0.1:8000/api/v1/health/](http://127.0.0.1:8000/api/v1/health/) —
`{"status": "ok", "database": "ok"}` chiqishi kerak.

## Tekshiruvlar (CI bilan bir xil)

```bash
ruff check .
ruff format --check .
lint-imports
python manage.py makemigrations --check --dry-run
pytest --cov=apps --cov-report=term-missing --cov-fail-under=85
```

## Deploy

Production runbook: `docs/architecture.md` §14.
