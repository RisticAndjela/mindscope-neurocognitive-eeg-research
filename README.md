# MindScope Backend

Backend MVP for MindScope research documentation and blog management.

This backend focuses only on:

- research projects
- datasets
- paper notes
- blog posts
- experiments
- model runs
- experiment metrics/results

Recommended cloud database: **Supabase Postgres Free Plan**.

## Stack

- Python
- FastAPI
- SQLAlchemy 2
- Pydantic 2
- PostgreSQL / Supabase
- Alembic-ready structure

## Run locally

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## Database

Create a free Supabase project, copy the Postgres connection string, and put it in `.env`:

```env
DATABASE_URL=postgresql+asyncpg://postgres:<PASSWORD>@<HOST>:5432/postgres
```

Then run the SQL in:

```txt
backend/sql/001_initial_schema.sql
```

inside Supabase SQL Editor.
