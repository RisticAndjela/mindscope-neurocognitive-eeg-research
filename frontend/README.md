# MindScope Frontend

Angular frontend for MindScope's public project/blog experience and the private research writing workspace.

## Routes

- `/`
- `/projects`
- `/projects/:slug`
- `/blog`
- `/blog/:slug`
- `/login`
- `/research/blog`
- `/research/blog/new`
- `/research/blog/:id/edit`
- `/research/forbidden`

## Local Setup

1. Copy the placeholder values from `src/environments/environment.example.ts`.
2. Update `src/environments/environment.ts` with your real backend and Supabase values.
3. Run:

```bash
npm install
npm start
```

The frontend expects the backend API at `http://127.0.0.1:8000/api/v1` by default.
