# Gigi Yogurt Backend (with Auth & Orders)

This backend is ready for deployment to Render (or other providers).

## Quick start (Render)
1. Push this `backend/` folder to your GitHub repo.
2. On Render: Create a **Web Service** -> Docker
   - Dockerfile path: `backend/Dockerfile` (if you place this folder under `backend` in repo)
3. Add a Postgres database on Render (Provisioned Database) and set environment variables (Render provides them):
   - RENDER_DB_USER, RENDER_DB_PASSWORD, RENDER_DB_HOST, RENDER_DB_PORT, RENDER_DB_NAME
4. Add these env vars in the service settings (or use them in `.env`):
   - `DATABASE_URL=postgresql://${RENDER_DB_USER}:${RENDER_DB_PASSWORD}@${RENDER_DB_HOST}:${RENDER_DB_PORT}/${RENDER_DB_NAME}`
   - `SECRET_KEY=<random-secret>`
   - `ACCESS_TOKEN_EXPIRE_MINUTES=60`
5. Deploy. After deploy, run `create_admin.py` to create your first admin user or use the open `/auth/users` bootstrap endpoint.

## Local dev (docker-compose)
You can also run Postgres locally and point `DATABASE_URL` accordingly.
