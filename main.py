from fastapi import FastAPI, APIRouter, HTTPException
from configurations import collection
from database.schemas import all_data
from database.models import ToDo
from bson.objectid import ObjectId
from datetime import datetime

app = FastAPI()
router = APIRouter(
    tags= ["ToDo"]
)

@router.get("/",response_model=list[ToDo])
async def get_all_todos():
     data = collection.find({"is_deleted":False})
     return all_data(data)

@router.post("/")
async def create_task(new_task:ToDo):
    try:
        response = collection.insert_one(dict(new_task))
        return {"status_code":200, "id": str(response.inserted_id) }
    except Exception as ex:
        raise HTTPException(status_code=500, detail="some error ocurred {ex}")
        
@router.put("/{task_id}")
async def update_task(task_id: str, updated_task: ToDo):
    try:
        id = ObjectId(task_id)
        existing_doc = collection.find_one({"_id": id, "is_deleted": False})
        if not existing_doc:
            raise HTTPException(status_code=404, detail="Task doesn’t exist")
        
        updated_task.updated_at = datetime.timestamp(datetime.now())
        response = collection.update_one({"_id": id}, {"$set": dict(updated_task)})
        
        if response.modified_count == 0:
            raise HTTPException(status_code=404, detail="No changes made to the task")
        
        return {"status_code": 200, "message": "Task updated successfully"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Some error occurred: {ex}")

@router.delete("/{task_id}")
async def delete_task(task_id: str):
    try:
        id = ObjectId(task_id)
        existing_doc = collection.find_one({"_id": id, "is_deleted": False})
        if not existing_doc:
            raise HTTPException(status_code=404, detail="Task doesn’t exist")
        
        response = collection.update_one({"_id": id}, {"$set": {"is_deleted": True}})
        
        if response.modified_count == 0:
            raise HTTPException(status_code=404, detail="No changes made to the task")
        
        return {"status_code": 200, "message": "Task deleted successfully"}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Some error occurred: {ex}")
      
    
app.include_router(router=router)