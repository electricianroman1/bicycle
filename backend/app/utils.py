from motor.motor_asyncio import AsyncIOMotorClient
import os
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

_client = None
def get_client():
    global _client
    if _client is None:
        uri = os.getenv("MONGO_URI", "mongodb://mongo:27017/dnd")
        _client = AsyncIOMotorClient(uri)
    return _client

async def get_db():
    return get_client().get_default_database()

async def get_current_user(token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {"username": "demo"}
