# TaskFlow API

A project & task management REST API (think: a small Trello/Asana backend) —
built as a learning project to go from "some API/SQL exposure" to a
production-shaped FastAPI + PostgreSQL backend.

## Tech stack

- **uv** — Python package & environment manager
- **FastAPI** — web framework
- **PostgreSQL** — database
- **SQLAlchemy** (async) — ORM, from Phase 2
- **Alembic** — migrations, from Phase 2
- **pytest** — testing, from Phase 6
- **Docker Compose** — local Postgres
- **GitHub Actions** — CI, from Phase 6

## Roadmap

- [x] **Phase 0 — Environment & project setup** (this commit)
- [ ] **Phase 1 — FastAPI fundamentals**: routing, path/query params, Pydantic
      request & response models, automatic docs (in-memory task store, no DB
      yet)
- [ ] **Phase 2 — Database layer**: async SQLAlchemy + Postgres, Alembic
      migrations, swap the in-memory store for real persistence
- [ ] **Phase 3 — Data modeling**: Users, Projects, Tasks, Comments, Tags —
      one-to-many and many-to-many relationships
- [ ] **Phase 4 — Auth**: password hashing, JWT login, protected routes,
      project-level roles/permissions
- [ ] **Phase 5 — Advanced patterns**: dependency injection in depth,
      background tasks, pagination & filtering, centralized error handling
- [ ] **Phase 6 — Testing & CI**: pytest + TestClient, a dedicated test
      database, GitHub Actions running the suite on every push
- [ ] **Phase 7 — Production readiness**: structured logging, Dockerizing
      the app itself, environment-based config
- [ ] **Phase 8 (stretch) — Deployment**: ship it to a real host; optionally
      add Redis caching / rate limiting

Each phase lives on its own branch and gets merged into `main` when it works
end to end — see **Git workflow** below.

## Phase 0 setup

```bash
# 1. Install uv, if you don't have it yet
curl -LsSf https://astral.sh/uv/install.sh | sh   # Windows: see astral.sh/uv

# 2. Create the virtual environment and install dependencies
#    (reads pyproject.toml, creates .venv, writes uv.lock)
uv sync

# 3. Create your local env file
cp .env.example .env

# 4. Run the app
uv run uvicorn app.main:app --reload
```

`uv run` runs a command inside `.venv` without you needing to activate it
manually -- though `source .venv/bin/activate` still works if you'd rather
work that way.

Then open **http://127.0.0.1:8000/docs** for the interactive API docs, and
**http://127.0.0.1:8000/health** for the health check.

Postgres isn't wired up yet, but it's ready for Phase 2 whenever you want it
running in the background:

```bash
docker compose up -d
```

## Git workflow

The point of this repo is to be easy to revise later and easy for someone
else to follow, so we're deliberate about history from commit one:

- **`main`** always stays in a working state — every phase is merged in only
  once it runs end to end.
- **`uv.lock` is committed**, not ignored — it pins exact dependency
  versions so anyone who clones this (including future you) gets the same
  environment with one `uv sync`.
- **One branch per phase**, named `phase-N-short-description`, e.g.
  `phase-1-fastapi-fundamentals`, `phase-2-postgres-sqlalchemy`.
- **Commit messages** follow [Conventional Commits](https://www.conventionalcommits.org/):
  - `feat: add task creation endpoint`
  - `fix: correct 422 on missing task title`
  - `docs: update README with Phase 2 setup`
  - `test: add coverage for task deletion`
  - `chore: add .gitignore`
- **Open a PR into `main` for each phase**, even solo — it's a habit worth
  having, and it gives each phase a clean, reviewable diff to look back on.
- Tag `main` at the end of each phase (`git tag phase-1-complete`) so you can
  always jump back to "the app as it was right after learning X."
