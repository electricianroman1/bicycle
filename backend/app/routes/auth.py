from fastapi import APIRouter, HTTPException, Depends, status, Form
from datetime import datetime
from ..db import db
from ..models import UserCreate, UserInDB, Token, TokenData
from ..security import hash_password, verify_password, create_access_token
from bson import ObjectId
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserInDB)
async def register(user: UserCreate):
    existing = await db.users.find_one({"username": user.username})
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed = hash_password(user.password)
    doc = {
        "username": user.username,
        "hashed_password": hashed,
        "created_at": datetime.utcnow()
    }
    res = await db.users.insert_one(doc)
    doc["_id"] = res.inserted_id
    return UserInDB(id=str(doc["_id"]), username=doc["username"], hashed_password=doc["hashed_password"], created_at=doc["created_at"])

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    # OAuth2PasswordRequestForm has fields: username, password
    user = await db.users.find_one({"username": form_data.username})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    if not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = create_access_token(subject=str(user["_id"]))
    return {"access_token": access_token, "token_type": "bearer"}
