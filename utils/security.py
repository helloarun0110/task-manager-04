import bcrypt
from fastapi.concurrency import run_in_threadpool


async def hash_password(password: str) -> str:
    hashed = await run_in_threadpool(
        bcrypt.hashpw,
        password.encode(),
        bcrypt.gensalt()
    )

    return hashed.decode()




async def verify_password(password: str, hashed: str) -> bool:
    return await run_in_threadpool(
        bcrypt.checkpw,
        password.encode(),
        hashed.encode()
    )