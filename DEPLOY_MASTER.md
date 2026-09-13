# Production deploy (master compose)

## Start
From `Egor-bot` on the server:

```bash
cp .env.example .env   # first time only — fill secrets, paths, mail
docker compose -f docker-compose.master.yaml --env-file .env up -d --build
```

## Services started
- `nginx` — HTTPS reverse proxy (frontend + API + admin + media)
- `certbot` — certificate renewal
- `db` — MySQL
- `redis` — Celery broker
- `admin_bot` — Django + DRF (`bot_admin`)
- `celery` — mail/registration worker queue
- `frontend` — React SPA

**Telegram bot is not started** in this compose.

## Required `.env` paths
| Variable | Points to |
|----------|-----------|
| `ADMIN_APP_PATH` | `bot_admin` repo root (has `Dockerfile`) |
| `FRONTEND_APP_PATH` | `Egor_frontend/foodmap_front` (has `Dockerfile`) |
| `MEDIA_HOST_PATH` | host media directory |

All other env vars for Django, MySQL, Redis, Celery, mail, CORS live in the same `.env`.

## Admin users
Create staff/superusers manually (no public admin registration):

```bash
docker exec -it admin_bot python manage.py createsuperuser --settings=bot_admin.develop_settings
```

## Notes
- `DEBUG=False` is forced for `admin_bot` and `celery` in compose.
- Nginx blocks probes for `.env`, `.git`, compose/Dockerfile, etc.
- First DB boot runs `Deploy/mysql-init/00-create-databases.sh` and imports `Deploy/db_dump/*.sql`.
