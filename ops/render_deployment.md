# Render deployment — Command Center (FE + BE)

Step-by-step plan to deploy the **ICS/OT Command Center** to [Render](https://render.com) with both the React frontend and FastAPI backend on the **free tier**.

**Deployment model:** one **Render Web Service** (Docker). The backend serves the built UI from `apps/command_center/dist/` (same as local integrated mode). No separate FE host is required.

**Scope:** synthetic read-only workshop/demo deployment — not live OT. The API has **no authentication** (OPEN-029); treat the public URL as demo-only and restrict who you share it with.

---

## Architecture

```text
Browser
   │
   ▼
Render Web Service (Docker container)
   ├── FastAPI  :8000  →  /health, /assets/…, /risk/…, …
   └── StaticFiles      →  /  (React SPA from dist/)
         │
         └── data/  (bundled CSV/JSON brownfield estate)
```

| Component | Source | Render service |
|-----------|--------|----------------|
| Backend API | `src/ot_command/api.py` | Web Service (Docker) |
| Frontend | `apps/command_center` → `npm run build` | Served by same container |
| Estate data | `data/` (~11 MB) | Copied into container image |
| AI (optional) | `AI_ENABLED=0` default | Environment variable; keep `0` for $0 model cost |

---

## Prerequisites

On your workstation:

| Tool | Purpose | Install |
|------|---------|---------|
| [Docker Desktop](https://docs.docker.com/desktop/) | Build and test the image locally | Recommended before first deploy |
| [Git](https://git-scm.com/) | Push code to GitHub | Required for Render Git deploy |
| Node.js 18+ | Local FE build verification (optional) | Already used for dev |
| Python 3.11+ | Local BE verification (optional) | Already used for dev |

Accounts:

| Account | Purpose |
|---------|---------|
| [GitHub](https://github.com) | Host the repo Render pulls from |
| [Render](https://render.com) | Free Web Service hosting (sign up with GitHub) |

The repo root already includes a multi-stage **`Dockerfile`** (React build + Python API) and **`.dockerignore`**. No Dockerfile changes are required for Render.

**Suggested naming** (replace `YOUR_SUFFIX` with something unique, e.g. `fde-cc-01`):

| Item | Example value |
|------|---------------|
| Render service name | `ics-ot-command-center` |
| Public URL | `https://ics-ot-command-center.onrender.com` |
| Git branch | `main` |

---

## Step 0 — Verify integrated build locally

From the **repo root**:

```powershell
cd apps\command_center
npm install
npm run build
cd ..\..
$env:PYTHONPATH = "src"
python -m uvicorn ot_command.api:app --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000 — UI loads and `/health` returns JSON with `api_version`.

> **Important:** Do **not** set `VITE_API_URL` for production builds. The client uses same-origin paths (`/health`, `/assets/…`) when `VITE_API_URL` is unset.

---

## Step 1 — Build and test the container locally

From the **repo root**:

```powershell
docker build -t ics-ot-command-center:local .
docker run --rm -p 8000:8000 ics-ot-command-center:local
```

Verify:

```powershell
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/
```

Stop the container when done (`Ctrl+C`).

---

## Step 2 — Push the repo to GitHub

Render deploys from a Git repository. If the project is not on GitHub yet:

1. Create a new **private** or **public** repository on GitHub (private is fine for workshop demos).
2. Push this repo:

```powershell
git remote add origin https://github.com/<YOUR_USER>/<YOUR_REPO>.git
git push -u origin main
```

> **Do not commit secrets.** Keep `.env.development.local` out of git (it should stay gitignored).

---

## Step 3 — Create a Render Web Service (Dashboard)

1. Sign in at [dashboard.render.com](https://dashboard.render.com) (use **Sign in with GitHub**).
2. Click **New +** → **Web Service**.
3. Connect your GitHub account if prompted, then select the repository for this project.
4. Configure the service:

| Setting | Value |
|---------|-------|
| **Name** | `ics-ot-command-center` (or your choice — becomes part of the URL) |
| **Region** | Closest to your audience (e.g. Oregon / Frankfurt) |
| **Branch** | `main` |
| **Root Directory** | *(leave blank — repo root)* |
| **Runtime** | **Docker** |
| **Instance Type** | **Free** |

5. Expand **Advanced** and set:

| Setting | Value |
|---------|-------|
| **Docker Command** | *(leave blank — uses `CMD` from Dockerfile)* |
| **Health Check Path** | `/health` |

6. Add **Environment Variables**:

| Key | Value |
|-----|-------|
| `AI_ENABLED` | `0` |
| `OT_DATA_ROOT` | `/app` |

> `PYTHONPATH=/app/src` is already set in the Dockerfile; you do not need to add it again unless you override the image.

7. Click **Create Web Service**.

Render builds the Docker image from your `Dockerfile` and deploys it. The first build takes **5–15 minutes** (npm install + pip install + data copy).

---

## Step 4 — Confirm port configuration

The container listens on **port 8000** (`EXPOSE 8000` in the Dockerfile, `uvicorn … --port 8000`).

After the service is created:

1. Open the service in the Render dashboard.
2. Go to **Settings** → **Networking** (or **Environment** depending on UI version).
3. Confirm **Port** is **8000**.

Render reads the `EXPOSE` directive automatically in most cases; if health checks fail with connection errors, set the port explicitly to `8000`.

---

## Step 5 — Verify deployment

When the deploy status shows **Live**, open your service URL (shown at the top of the dashboard), e.g.:

```text
https://ics-ot-command-center.onrender.com
```

Check the API:

```powershell
curl https://ics-ot-command-center.onrender.com/health
```

Expected `/health` response shape:

```json
{
  "status": "ok",
  "mode": "synthetic-read-only",
  "ai_enabled": false,
  "api_version": "3.0.0"
}
```

Open the URL in a browser — the React command center should load; scenario rail and estate views should populate from bundled `data/`.

If something fails, open **Logs** in the Render dashboard (build logs vs runtime logs).

---

## Step 6 — Redeploy after code changes

With Git-connected deploy (default):

1. Commit and push to the tracked branch (`main`):

```powershell
git add .
git commit -m "Update command center"
git push origin main
```

2. Render starts a new build automatically. Watch progress under **Events** / **Logs**.

To redeploy without a code change: dashboard → **Manual Deploy** → **Deploy latest commit**.

---

## Step 7 (optional) — `render.yaml` (Infrastructure as Code)

To codify the service in the repo, add `render.yaml` at the **repo root**:

```yaml
services:
  - type: web
    name: ics-ot-command-center
    runtime: docker
    plan: free
    branch: main
    healthCheckPath: /health
    envVars:
      - key: AI_ENABLED
        value: "0"
      - key: OT_DATA_ROOT
        value: /app
```

Then in the Render dashboard: **New +** → **Blueprint** → select the repo. Render creates the web service from the blueprint. Future changes to `render.yaml` sync on deploy.

---

## Free tier behavior

| Behavior | Detail |
|----------|--------|
| **Cost** | $0 on the Free instance type |
| **Sleep** | Service **spins down after ~15 minutes** with no traffic |
| **Cold start** | First request after sleep may take **30–60 seconds** |
| **Hours** | 750 instance hours/month (enough for one always-on service most months) |
| **Build time** | Free tier build minutes are limited; large Docker builds may queue |

For a live workshop, hit `/health` a few minutes before the session to wake the service, or warn attendees about the first-load delay.

---

## Alternative — Split FE and BE (not recommended)

Only use if you must host the SPA separately:

| Layer | Service | Notes |
|-------|---------|-------|
| FE | Render Static Site | Deploy `apps/command_center/dist` |
| BE | Render Web Service (Python/Docker) | API only, no StaticFiles |

Extra work required:

1. Build FE with `VITE_API_URL=https://<api-host>` so fetches hit the API origin.
2. Add the static-site origin to CORS in `src/ot_command/api.py` (`allow_origins`).
3. Configure SPA routing for deep links.

The **integrated single-container** path above avoids CORS and matches how the repo is designed.

---

## Security and operations checklist

| Item | Action |
|------|--------|
| Public exposure | API is read-only but unauthenticated — share the URL only with workshop participants; consider a private repo |
| AI | Keep `AI_ENABLED=0` unless you have model keys and FinOps approval (OPEN-028) |
| Secrets | Do not commit `.env.development.local`; use Render **Environment** for runtime settings |
| Cost control | Stay on **Free** instance type; delete the service when finished |
| Rollback | Dashboard → **Events** → redeploy a previous successful deploy |
| Health | Monitor `GET /health` and `GET /ops/slo` |

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Blank UI, `/health` works | `dist/` missing from image | Confirm multi-stage `Dockerfile` at repo root; check build logs for `npm run build` |
| Deploy fails during build | Docker build error | Read **Build logs**; run `docker build .` locally to reproduce |
| Health check failed | Wrong port | Set port to **8000** in service settings |
| 502 / service unavailable | Container crash on start | Check **Runtime logs**; verify `PYTHONPATH` and `data/` present in image |
| UI loads, API 404 on routes | Built with `VITE_API_URL=/api` | Rebuild without `VITE_API_URL` for integrated deploy |
| `scenario bindings not found` | `scenario_bindings.json` missing from image | Confirm Dockerfile copies `apps/command_center/scenario_bindings.json` and `scenarios/`; redeploy |
| Very slow first load | Free tier cold start | Normal after idle; pre-warm with `curl …/health` before demo |
| Build timeout | Free tier limits | Retry deploy; ensure `.dockerignore` excludes `node_modules`, `.venv`, `tests` |

---

## Tear down

1. Render dashboard → select the web service.
2. **Settings** → scroll to **Delete Web Service** → confirm.

No other cloud resources (registry, VM, etc.) to clean up.

---

## Quick reference — local vs Render

| Mode | FE | BE | URL |
|------|----|----|-----|
| Dev (local) | Vite `:5173` | uvicorn `:8000` | http://127.0.0.1:5173 |
| Integrated (local) | StaticFiles | uvicorn `:8000` | http://127.0.0.1:8000 |
| Render (this guide) | StaticFiles in container | same container | `https://<service-name>.onrender.com` |

Related docs: root [`README.md`](../README.md), [`apps/command_center/README.md`](../apps/command_center/README.md), [`ops/runbooks.md`](runbooks.md).
