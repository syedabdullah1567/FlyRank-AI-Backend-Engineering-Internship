from fastapi import FastAPI, HTTPException
from db import init_db, get_all_tasks, get_task_by_id

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/tasks")
def read_tasks():
    return get_all_tasks()

@app.get("/tasks/{id}")
def read_task(id: int):
    task = get_task_by_id(id)
    if not task:
        raise HTTPException(status_code=404, detail={"error": "Task not found"})
    return task