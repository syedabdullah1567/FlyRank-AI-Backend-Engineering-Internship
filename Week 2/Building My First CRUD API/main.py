from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

tasks = [
    {"id": 1, "title": "Buy groceries", "done": False},
    {"id": 2, "title": "Read FastAPI docs", "done": True},
    {"id": 3, "title": "Complete Stage 2", "done": False},
]

# Stage 1 Endpoints

@app.get("/")
async def get_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Stage 2 Endpoints

@app.get("/tasks")
async def get_all_tasks():
    return tasks

@app.get("/tasks/{id}")
async def get_task_by_id(id: int):
    for task in tasks:
        if task["id"] == id:
            return task
    
    raise HTTPException(status_code=404, detail=f"Task {id} not found")

# Stage 3 Endpoints

class TaskCreate(BaseModel):
    title: str

@app.post("/tasks", status_code=201)
async def post_task(task_data: TaskCreate) :
 
    if not task_data.title or task_data.title.strip() == "":
        raise HTTPException(
            status_code=400, detail="Title is required and cannot be empty"
        )

    new_id = len(tasks) + 1

    new_task = {
        "id": new_id,
        "title": task_data.title,
        "done": False, 
    }

    tasks.append(new_task)
    return new_task

# Stage 4 Endpoints

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None



@app.put("/tasks/{id}")
async def update_task(id: int, update_data: TaskUpdate):

    if update_data.title is None and update_data.done is None:
        raise HTTPException(
            status_code=400,
            detail="Request body must include 'title' or 'done'",
        )

    if update_data.title is not None and update_data.title.strip() == "":
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    for task in tasks:
        if task["id"] == id:
            if update_data.title is not None:
                task["title"] = update_data.title.strip()
            if update_data.done is not None:
                task["done"] = update_data.done

            return task

    raise HTTPException(status_code=404, detail=f"Task {id} not found")


@app.delete("/tasks/{id}", status_code=204)
async def delete_task(id: int):
    for task in tasks:
        if task["id"] == id:
            tasks.remove(task)
            return

    raise HTTPException(status_code=404, detail=f"Task {id} not found")