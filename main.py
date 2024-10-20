from fastapi import FastAPI,WebSocket
from app.db import models
from app.db.database import engine
from app.api.endpoints import tasks, users


app = FastAPI()


models.Base.metadata.create_all(bind=engine)

@app.websocket("/ws/tasks")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Task update: {data}")


app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
app.include_router(users.router, prefix="/users", tags=["users"])

@app.get("/")
async def root():
    return {"message": "Task Manager is running"}
