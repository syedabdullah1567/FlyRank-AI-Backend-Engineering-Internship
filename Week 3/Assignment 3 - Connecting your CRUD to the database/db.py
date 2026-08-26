import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)

def init_db():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Create tasks table if it does not exist
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    done BOOLEAN NOT NULL DEFAULT FALSE
                );
            """)
            
            # Check if table is empty
            cur.execute("SELECT COUNT(*) FROM tasks;")
            count = cur.fetchone()["count"]
            
            # Seed 3 example tasks only if empty
            if count == 0:
                cur.execute("""
                    INSERT INTO tasks (title, done) VALUES
                    ('Buy groceries', false),
                    ('Read Sqlite3 docs', true),
                    ('Complete Stage 0', false);
                """)
            conn.commit()

def get_all_tasks():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, title, done FROM tasks ORDER BY id ASC;")
            return cur.fetchall()

def get_task_by_id(task_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Parameterized query (%s) prevents SQL injection
            cur.execute("SELECT id, title, done FROM tasks WHERE id = %s;", (task_id,))
            return cur.fetchone()

def create_task(title: str):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # RETURNING * hands back the newly created row including its id
            cur.execute(
                "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id, title, done;",
                (title, False)
            )
            return cur.fetchone()

def update_task(task_id: int, title: str | None, done: bool | None):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            # Check if task exists
            cur.execute("SELECT id, title, done FROM tasks WHERE id = %s;", (task_id,))
            existing = cur.fetchone()
            if not existing:
                return None
            
            # Determine updated values
            new_title = title if title is not None else existing["title"]
            new_done = done if done is not None else existing["done"]

            cur.execute(
                "UPDATE tasks SET title = %s, done = %s WHERE id = %s RETURNING id, title, done;",
                (new_title, new_done, task_id)
            )
            return cur.fetchone()

def delete_task(task_id: int):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM tasks WHERE id = %s RETURNING id;", (task_id,))
            deleted = cur.fetchone()
            return deleted is not None