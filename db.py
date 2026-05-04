import aiomysql
from typing import AsyncGenerator
from dotenv import load_dotenv
import os

load_dotenv()

pool = None

async def create_db_pool():
    global pool
    pool = await aiomysql.create_pool(
        host = os.getenv("DB_HOST"),
        port = int(os.getenv("PORT", 3306)),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        db = os.getenv("DB_NAME"),
        minsize = 1,
        maxsize = 5,
        autocommit = True
    )
    print("db pool created!!")


async def close_db_pool():
    global pool
    if pool:
        pool.close()
        await pool.wait_closed()


async def get_conn() -> AsyncGenerator:
    async with pool.acquire() as conn:
        yield conn