from fastapi import FastAPI
from .routers import users, vehicles

app = FastAPI()

app.include_router(users.router)
app.include_router(vehicles.router)

@app.get("/")
async def root():
    return {"API V1": "BR RENTAL CAR"}

