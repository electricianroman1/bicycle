from pydantic import BaseModel, Field
from typing import Any, Optional
from datetime import datetime

# --- Sheets ---
class SheetIn(BaseModel):
    name: str = Field(..., example="Thorin Oakenshield")
    data: dict[str, Any] = Field(..., description="Полный JSON листа персонажа")

class SheetOut(SheetIn):
    id: str
    created_at: datetime
    updated_at: datetime

class UpdateSheet(BaseModel):
    name: Optional[str]
    data: Optional[dict[str, Any]]

# --- Users & Auth ---
class UserCreate(BaseModel):
    username: str
    password: str

class UserInDB(BaseModel):
    id: Optional[str]
    username: str
    hashed_password: str
    created_at: Optional[datetime]

class UserPublic(BaseModel):
    id: str
    username: str
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None
