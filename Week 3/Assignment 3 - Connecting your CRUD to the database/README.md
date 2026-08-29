```markdown
# FlyRank Backend Track - Week 1 Assignment 3: Containerized Task API

A FastAPI task CRUD API running against a containerized PostgreSQL database using Docker Compose.

## 🚀 One-Command Setup

1. Copy the environment template:
   ```bash
   cp .env.example .env

```

2. Start the full stack (API + Database):
```bash
docker compose up --build

```



The API will be live at `http://localhost:8000`.

---

## 🔑 Environment Variables

| Variable | Description | Example |
| --- | --- | --- |
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:dev@db:5432/tasks` |

---

## 📡 API Endpoints

| Method | Endpoint | Description | Status Codes |
| --- | --- | --- | --- |
| `GET` | `/tasks` | List all tasks | `200` |
| `GET` | `/tasks/{id}` | Get task by ID | `200`, `404` |
| `POST` | `/tasks` | Create a new task | `201`, `400` |
| `PUT` | `/tasks/{id}` | Update task title or done status | `200`, `400`, `404` |
| `DELETE` | `/tasks/{id}` | Delete task by ID | `204`, `404` |

---

## 🧪 Sample Output

```bash
$ curl -i http://localhost:8000/tasks
HTTP/1.1 200 OK
date: Sat, 29 Aug 2026 12:35:00 GMT
server: uvicorn
content-length: 187
content-type: application/json

[{"id":1,"title":"Buy groceries","done":false},{"id":2,"title":"Read Sqlite3 docs","done":true},{"id":3,"title":"Complete Stage 0","done":false}]

```

---

## 📊 Database Verification

Data running inside the Postgres container verified via `psql`:

```text
tasks=# \dt
        List of relations
 Schema |  Name  | Type  |  Owner   
--------+--------+-------+----------
 public | tasks  | table | postgres
(1 row)

tasks=# SELECT * FROM tasks;
 id |            title            | done 
----+-----------------------------+------
  1 | Buy groceries               | f
  2 | Read Sqlite3 docs           | t
  3 | Complete Stage 0            | f
(3 rows)

```

```

```

---

### Step 3: Round-Trip Verification Checkpoint

Test the clean clone flow locally to guarantee it works end-to-end:

```bash
docker compose down -v
cp .env.example .env
docker compose up --build -d
curl -i http://localhost:8000/tasks
docker compose down