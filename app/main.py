from fastapi import FastAPI
from .routers import user, vehicles, employee, rental
from contextlib import asynccontextmanager
from .database.db import get_db_pool

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Code to run on startup ---
    print("INFO:     Starting up and creating DB pool...")
    # Create the pool and store it in the application's state.
    # The 'state' is a special object to share resources.
    app.state.db_pool = await get_db_pool()
    
    yield # The application runs here

    # --- Code to run on shutdown ---
    print("INFO:     Shutting down and closing DB pool...")
    app.state.db_pool.close()
    await app.state.db_pool.wait_closed()


app = FastAPI(lifespan=lifespan)


app.include_router(user.router)
app.include_router(vehicles.router)
app.include_router(employee.router)
app.include_router(rental.router)

@app.get("/")
async def root():
    return {"API V1": "BR RENTAL CAR"}

