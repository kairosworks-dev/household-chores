# Shared Chore Manager

A web app for two people sharing a household to track chores, completions, and
reminders. Scope lives in `_docs/plan.md`.

## Stack

- Python 3.13, Django 6.1, managed with `uv` (see `pyproject.toml`, `uv.lock`)
- SQLite locally; Postgres in production
- Server-rendered Django templates, one handwritten stylesheet, no frontend build
- pytest + pytest-django

## Layout

- `config/` — the Django project: settings, root URLs, asgi/wsgi
- `chores/` — chores, completions, reminders
- `accounts/` — user, household, invites (not created yet, see issue #2)
- `_docs/` — plan, backlog, process, guidelines

## Commands

- `uv sync` - install dependencies
- `uv run pytest` - the whole suite
- `uv run pytest chores/tests/test_models.py` - one test file
- `uv run python manage.py runserver` - the dev server
- `uv run python manage.py makemigrations` / `migrate` - schema changes
- `uv run python manage.py createsuperuser` - an admin login

## Rules

- Dependencies are added in `pyproject.toml`. Do not add one without
  asking
- Secrets and environment-specific values are read from the environment in
  `config/settings.py` and documented in `.env.example`. Never hardcode one,
  and never commit `.env` or `db.sqlite3`
- Tests live next to the code they cover, in each app's `tests/` package
- Work happens on `main`

## Documents

- `_docs/plan.md` - project scope; check before building something new
- `_docs/backlog.md` - the tasks, numbered to match GitHub issues
- `_docs/process.md` - how work is organized
- `_docs/task-template.md` - the shape of a well-formed task
- Before writing tests, read `_docs/testing-guidelines.md`
- For anything touching the UI, read `_docs/design-system.md`
