# MindScope

MindScope is a research portfolio platform with a FastAPI backend, Angular frontend, Supabase Postgres, and Supabase Auth. Public visitors can browse projects and published blog posts, while authenticated research users can manage the private writing workspace.

## Stack

- Backend: FastAPI, SQLAlchemy, async PostgreSQL, Supabase Auth token verification
- Frontend: Angular standalone components, Supabase client auth
- Database: Supabase Postgres with SQL migration scripts in `backend/sql`
- Local orchestration: Docker Compose

## Run With Docker

1. Create the backend env file:

```powershell
Copy-Item backend/.env.example backend/.env
```

2. Update `backend/.env` with your real Supabase database and auth values.

3. Update `frontend/src/environments/environment.ts` with your real frontend config values.
   Use `frontend/src/environments/environment.example.ts` as the committed placeholder reference.

4. Start the stack:

```powershell
docker compose up --build
```

5. Open:

- Frontend: `http://localhost:4200`
- Backend API: `http://localhost:8000`
- FastAPI docs: `http://localhost:8000/docs`

The backend container runs on `0.0.0.0:8000` and the frontend container runs on `0.0.0.0:4200`. Docker does not require a local Python virtual environment.

## Local Environment Files

Keep secrets out of Git:

- `backend/.env` is local-only and ignored by Git
- `backend/.env.example` stays committed
- `frontend/src/environments/environment.ts` should contain local project values only
- `frontend/src/environments/environment.example.ts` stays committed with placeholders

Do not commit real Supabase anon keys, database passwords, or project-specific URLs.

## Backend Env Variables

Required in `backend/.env`:

- `DATABASE_URL`
- `SUPABASE_URL`
- `SUPABASE_JWKS_URL`

Commonly used:

- `APP_NAME`
- `APP_ENV`
- `API_PREFIX`
- `CORS_ORIGINS`
- `SUPABASE_JWT_AUDIENCE`

Example values are already included in [backend/.env.example](/C:/Users/panonit/Documents/mindscope-neurocognitive-eeg-research/backend/.env.example:1).

## Frontend Environment Values

Required in [frontend/src/environments/environment.ts](/C:/Users/panonit/Documents/mindscope-neurocognitive-eeg-research/frontend/src/environments/environment.ts:1):

- `backendApiBaseUrl`
- `supabaseUrl`
- `supabaseAnonKey`

Typical local backend value:

- `backendApiBaseUrl = 'http://127.0.0.1:8000/api/v1'`

## Supabase Setup Note

- Enable Supabase Auth for your project.
- Make sure the `profiles` table and research role logic are created from the SQL scripts below.
- `SUPABASE_JWKS_URL` should point to `https://<your-project>.supabase.co/auth/v1/.well-known/jwks.json`.
- The current project intentionally keeps a simple development-time workflow for creating a research user; no admin role-management UI or admin endpoints are required.

## Migration Order

Run the SQL scripts in this order against your Supabase Postgres database:

1. `backend/sql/001_initial_schema.sql`
2. `backend/sql/002_auth_profiles.sql`
3. `backend/sql/003_seed_examples.sql`
4. `backend/sql/004_blog_role_management.sql`

## Public Vs Research-Only Routes

Public frontend routes:

- `/`
- `/projects`
- `/projects/:slug`
- `/blog`
- `/blog/:slug`
- `/login`

Research-only frontend routes:

- `/research/blog`
- `/research/blog/new`
- `/research/blog/:id/edit`
- `/research-hub`

If an authenticated user is not in the research role, research-only pages redirect to the styled forbidden state at `/research/forbidden`.

## API Routes Added For Public Slugs

New public backend routes:

- `GET /api/v1/research/blog-posts/slug/{slug}`
- `GET /api/v1/research/projects/slug/{slug}`

The existing ID-based routes remain available for edit flows and internal research tooling.

## Quick Verification

Slug pages:

1. Create or inspect a project/blog post with a known slug.
2. Visit `/projects/<slug>` for projects.
3. Visit `/blog/<slug>` for published public posts.

Research guard:

1. Sign in with a non-research account.
2. Visit `/research/blog`.
3. Confirm you are redirected to `/research/forbidden`.
4. Sign in with a research account and confirm the workspace opens normally.
