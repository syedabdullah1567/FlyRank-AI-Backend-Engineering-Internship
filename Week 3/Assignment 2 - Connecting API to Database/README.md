# FastAPI Tasks API (SQLite Backend)

A lightweight RESTful API built with FastAPI and SQLite to manage daily tasks.

---

## Technical Design & Database Decisions

* **Why SQLite?**
  * **Zero Setup:** Requires no separate database server process or installation overhead.
  * **Single-File Storage:** The entire database resides in a single lightweight file (`tasks.db`), simplifying local development.
  * **Persistence:** Data survives application restarts while maintaining minimal memory usage.

* **Database File Location:**
  * The database file lives at `tasks.db` in the root folder.
  * It is created automatically upon startup if it does not exist, and is ignored by version control (`.gitignore`) so fresh clones start clean without dirty state.

---

## Quickstart

Run the server with a single command:

```bash
uv run fastapi dev main.py

or uv run fastapi dev <your file path to main.py>

```

## The application will automatically check for tasks.db, initialize the tasks table if missing, and seed initial sample tasks automatically.