from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import json
app = FastAPI()

TASKS_FILE = "tasks.json"

# Each task should look like  {"id": 1, "task": "Buy milk", "done": False}

class TaskBody(BaseModel):
    task: str

class TaskComplate(BaseModel):
    done: bool

# loads the taks
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as file:
        return json.load(file)
# saves em
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=2)

# getsall the tasks in the list and your can filter if done or not by doing smth like /tasks?done=true&
@app.get("/tasks")
async def get_tasks(done: bool = None):
    data = load_tasks()
    new_data = []

    if done is None:
        return data
    elif done:
        for task in data:
            if task["done"]:
                new_data.append(task)
        return new_data
    else:
        for task in data:
            if not task["done"]:
                new_data.append(task)
        return new_data

# Searches for a key word
@app.get("/tasks/search/{keyword}")
async def search_tasks(keyword: str):
    data = load_tasks()
    new_data = []

    for task in data:
        if keyword.lower() in task["task"].lower():
            new_data.append(task)
    return new_data

# ads a new task
@app.post("/tasks")
async def add_tasks(task_input: TaskBody):
    data = load_tasks()
    if not data:
        new_id = 1
    else:
        new_id = data[-1]["id"] + 1
    
    new_task = {
        "task": task_input.task,
        "id" : new_id,
        "done": False,
    }
    data.append(new_task)
    save_tasks(data)
    return new_task
    
# completes a task
@app.patch("/tasks/{task_id}/complete")
async def complete_task(task_id: int):
    data = load_tasks()
    for task in data:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(data)
            return task 
    raise HTTPException(status_code=404, detail="Task ID not found")

# Removes A task
@app.patch("/tasks/{task_id}")
async def delete_task(task_id: int):
    data = load_tasks()
    new_data = []
    for task in data:
        if task["id"] != task_id:
            new_data.append(task)

    if len(data) == len (new_data):
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        data = new_data
        save_tasks(data)
        return { "messsage": f"Deleted Task {task_id}!!!!"}

# Completely wipes out all the completed tasks (new one that wasn't on the list lol)
@app.patch("/tasks/wipe/complete")
async def wipe_task():
    data = load_tasks()
    new_data = []

    for task in data:
            if not task["done"]:
                new_data.append(task)
    if len(data) == len(new_data):
        raise HTTPException(status_code=404, detail="All Tasks are uncomplete")
    else:
        data = new_data
        save_tasks(data)
        return { "messsage": f"Deleted all COmpleted Tasks!!!!!"}



# Route 1: Get all tasks   
# Create a GET route at /tasks that returns all the tasks.
# Some hints:
# Use load_tasks() to get the tasks
# Just return the list directly as FastAPI will convert it to JSON for you!


def main():
    import uvicorn
    uvicorn.run("resolution_week3_doeygirl93.main:app", host="127.0.0.1", port=8000)

if __name__ == "__main__":
    main()