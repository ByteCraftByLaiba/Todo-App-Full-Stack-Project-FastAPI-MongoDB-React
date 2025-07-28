from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from bson import ObjectId
from datetime import datetime
import os

from configurations import collection
from database.schemas import all_tasks
from database.models import Todo

app = FastAPI()

# CORS (for dev or wide access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set correct absolute path to React build
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "../frontend/build"))

# Mount static folder
app.mount("/static", StaticFiles(directory=os.path.join(FRONTEND_DIR, "static")), name="static")


# ------------------- API Routes -------------------

@app.get("/")
def serve_index():
    return FileResponse("../frontend/build/index.html")

@app.get("/todos")
async def read_user():
    data = collection.find()
    return all_tasks(data)

@app.post("/todos")
async def create_post(new_todo: Todo):
    try:
        resp = collection.insert_one(dict(new_todo))
        return {"status code": status.HTTP_201_CREATED, "id": str(resp.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Error occurred: {e}")

@app.put("/todos/{task_id}")
async def update_todos(task_id: str, updated_task: Todo):
    try:
        id = ObjectId(task_id)
        existing_docs = collection.find_one({"_id": id})
        if not existing_docs:
            raise HTTPException(status_code=404, detail="Task doesn't exist.")
        updated_task.updated_at = datetime.timestamp(datetime.now())
        collection.update_one({"_id": id}, {"$set": dict(updated_task)})
        return {"status code": status.HTTP_200_OK, "message": "Task updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Error occurred: {e}")

@app.delete("/todos/{task_id}")
async def delete_todo(task_id: str):
    try:
        id = ObjectId(task_id)
        existing_docs = collection.find_one({"_id": id, "is_deleted": False})
        if not existing_docs:
            raise HTTPException(status_code=404, detail="Task doesn't exist.")
        collection.update_one({"_id": id}, {"$set": {"is_deleted": True}})
        return {"status code": status.HTTP_204_NO_CONTENT, "message": "Task deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Error occurred: {e}")
