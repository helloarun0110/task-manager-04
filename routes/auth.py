from fastapi import APIRouter, HTTPException, Depends, Body
from db import get_conn
from utils.jwt_handler import create_token
from utils.security import verify_password, hash_password
import aiomysql
from schemas.user import MessageResponse, TokenResponse, UserRegister, UserLogin, UserResponse
from typing import Annotated

router = APIRouter(prefix="/auth", tags=["Auth"])



@router.post("/register", response_model = MessageResponse)
async def register(user: Annotated[UserRegister,Body()], conn: Annotated[object, Depends(get_conn)]):
    async with conn.cursor() as cursor:
        hashed = await hash_password(user["password"])

        try:
            await cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (user.username, user.email, hashed)
            )
        except Exception as e:
            raise HTTPException(f"registration failed: {str(e)}")
    
    return MessageResponse(message="User registered successfully")




@router.post("/login", response_model=TokenResponse)
async def login(user:Annotated[UserLogin, Body()], conn:Annotated[object, Depends(get_conn)]):
    async with conn.cursor(aiomysql.DictCursor) as cursor:
        await cursor.execute(
            "SELECT * FROM users WHERE email=%s",(user.email,)
        )

        db_user = await cursor.fetchone()

    if not db_user or not await verify_password(user.password, db_user["password"]):
        raise HTTPException(401, "invalid credentials..")
    
    token = create_token({
        "user_id": db_user["id"],
        "role": db_user["role"]
    })

    return TokenResponse(access_token=token)