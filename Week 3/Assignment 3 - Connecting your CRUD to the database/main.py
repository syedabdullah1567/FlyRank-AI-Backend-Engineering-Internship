from typing import Optional
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from db import (
    init_db,
    get_all_tasks,
    get_task_by_id,
    create_task,
    update_task,
    delete_task
)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

@app.get("/tasks")
def read_tasks():
    return get_all_tasks()

@app.get("/tasks/{id}")
def read_task(id: int):
    task = get_task_by_id(id)
    if not task:
        raise HTTPException(status_code=404, detail={"error": "Task not found"})
    return task

@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def post_task(task_data: TaskCreate):
    if not task_data.title or task_data.title.strip() == "":
        raise HTTPException(
            status_code=400,
            detail={"error": "Title is required and cannot be empty"}
        )
    return create_task(task_data.title.strip())

@app.put("/tasks/{id}")
def put_task(id: int, update_data: TaskUpdate):
    if update_data.title is None and update_data.done is None:
        raise HTTPException(
            status_code=400,
            detail={"error": "Request body must include 'title' or 'done'"}
        )
    if update_data.title is not None and update_data.title.strip() == "":
        raise HTTPException(
            status_code=400,
            detail={"error": "Title cannot be empty"}
        )
    
    updated = update_task(
        id,
        update_data.title.strip() if update_data.title else None,
        update_data.done
    )
    if not updated:
        raise HTTPException(status_code=404, detail={"error": "Task not found"})
    return updated

@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_task(id: int):
    success = delete_task(id)
    if not success:
        raise HTTPException(status_code=404, detail={"error": "Task not found"})
    return Response(status_code=status.HTTP_204_NO_CONTENT)