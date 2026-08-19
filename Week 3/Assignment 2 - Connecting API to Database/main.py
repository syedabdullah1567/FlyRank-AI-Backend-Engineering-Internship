import sqlite3


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Stage 0

con = sqlite3.connect("tasks.db")

cur = con.cursor()

# Creating the database tables

# res = cur.execute('''
#     DROP TABLE IF EXISTS tasks
# ''')

# res = cur.execute('''

#     CREATE TABLE tasks(
#     id INTEGER PRIMARY KEY,
#     title TEXT,
#     done BOOLEAN
# )

# ''')

res = cur.execute("SELECT name FROM sqlite_master")
print(res.fetchone())

res = cur.execute('''
    SELECT COUNT(*) FROM tasks
''')

if (res.fetchone()[0] == 0) :
    

    cur.execute(''' 
        INSERT INTO tasks(title, done)
        VALUES
        ("Buy groceries", FALSE),
        ("Read Sqlite3 docs", TRUE),
        ("Complete Stage 0", FALSE)
    ''')
    con.commit()


res = cur.execute('''
    SELECT * FROM tasks
''')

print(res.fetchall())

# Stage 1

app = FastAPI()

@app.get("/tasks")
async def get_all_tasks():
    res = cur.execute('''
        SELECT * FROM tasks
    ''')

    return res.fetchall()  

@app.get("/tasks/{id}")
async def get_task_by_id(id: int):
    res = cur.execute(''' 
        SELECT * FROM tasks
    ''')

    tasks = res.fetchall()

    for task in tasks:
        if task[0] == id:
            return task
    
    raise HTTPException(status_code=404, detail=f"Task {id} not found")

# Stage 2

class TaskCreate(BaseModel):
    title: str


@app.post("/tasks", status_code=201)
async def post_task(task_data: TaskCreate) :
 
    if not task_data.title or task_data.title.strip() == "":
        raise HTTPException(
            status_code=400, detail="Title is required and cannot be empty"
        )

  
    cur.execute(
        "INSERT INTO tasks (title, done) VALUES (?, 0)",
        (task_data.title,)
    )
    con.commit()

    # 4. Use cur.lastrowid to fetch the exact row created
    task_id = cur.lastrowid
    cur.execute("SELECT id, title, done FROM tasks WHERE id = ?", (task_id,))
    row = cur.fetchone()

    
    return {
        "id": row[0],
        "title": row[1],
        "done": bool(row[2])
    }

