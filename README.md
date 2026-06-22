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
