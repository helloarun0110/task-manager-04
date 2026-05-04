from fastapi import FastAPI
from db import create_db_pool, close_db_pool
from contextlib import asynccontextmanager
from routes import auth, task



@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_pool()
    yield
    await close_db_pool()


app = FastAPI(title="task manager api", lifespan=lifespan)

app.include_router(auth.router)
app.include_router(task.router)