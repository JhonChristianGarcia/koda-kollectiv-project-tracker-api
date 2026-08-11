# Koda Kollectiv - Project Tracker API

Backend for the Koda Kollectiv project tracker. FastAPI + SQLite, with basic OAuth2 login so the frontend has something to auth against.

## Stack

- FastAPI
- SQLModel (SQLAlchemy + Pydantic)
- SQLite
- PyJWT + bcrypt for auth
- uv for deps/running

## Structure

```
main.py                # app entrypoint, startup (create tables + seed admin user), routers
database/database.py   # engine/session, Project and User models
projects/projects.py   # /projects routes, all require auth
auth/auth.py            # /auth/register, /auth/token, get_current_user dep, admin seeding
auth/security.py        # password hashing + JWT
.env / .env.example      # SECRET_KEY, INITIAL_ADMIN_* (.env is gitignored)
```

## Running it

Needs Python 3.12+ and uv.

```bash
cp .env.example .env
```

Fill in `.env`:
- `SECRET_KEY` - anything random, used to sign the JWTs
- `INITIAL_ADMIN_USERNAME` / `INITIAL_ADMIN_NAME` / `INITIAL_ADMIN_PASSWORD` - creds for the account that gets created on first run

Then:

```bash
uv sync
uv run fastapi dev
```

Docs at `http://localhost:8000/docs`.

First time it boots, it creates the sqlite tables and adds one admin user from `INITIAL_ADMIN_*` (skips it if that username's already there). Log in with that to get a token, hand it off to whoever's working on the frontend.

## Auth

- `POST /auth/register` - `{ username, name, password }`
- `POST /auth/token` - form fields `username` + `password`, returns `{ access_token, token_type }`
- everything else needs `Authorization: Bearer <token>`

Tokens expire after `ACCESS_TOKEN_EXPIRE_MINUTES` (in `auth/security.py`). No refresh token yet, so once it expires you just log in again.

## Projects endpoints

- `GET /projects/` - list
- `POST /projects/` - create
- `PUT /projects/{id}` - update
- `DELETE /projects/{id}` - delete

All of these need a valid token.

## Stuff to know

- sqlite path is relative, so it depends on where you run the app from - run from repo root or you'll end up with two db files
- registration is open right now, anyone can hit `/auth/register` - fine for now but worth locking down before this goes anywhere real
