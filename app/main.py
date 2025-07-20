from fastapi import FastAPI
from .routers import user, vehicles, employee, rental




app = FastAPI()


app.include_router(user.router)
app.include_router(vehicles.router)
app.include_router(employee.router)
app.include_router(rental.router)

@app.get("/")
async def root():
    return {"API V1": "BR RENTAL CAR"}

