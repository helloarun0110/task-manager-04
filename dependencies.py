from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from utils.jwt_handler import decode_token
from schemas.user import CurrentUser


security = HTTPBearer()


async def get_current_user(token=Depends(security)) -> CurrentUser:
    try:
        payload = decode_token(token.credentials)
        return CurrentUser(**payload)
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"invalid token: {e}")
    