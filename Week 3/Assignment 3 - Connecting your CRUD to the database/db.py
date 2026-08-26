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