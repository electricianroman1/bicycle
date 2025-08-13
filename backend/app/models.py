from pydantic import BaseModel, Field, validator
from typing import Optional, Any, Dict
from datetime import datetime

class LSSSheet(BaseModel):
    payload: Dict[str, Any] = Field(..., description="Полный LSS JSON как есть")
    name: str = Field(..., description="Имя персонажа")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    owner: Optional[str] = None

    @validator("name", pre=True, always=True)
    def ensure_name(cls, v, values):
        if v:
            return v
        payload = values.get("payload") or {}
        data_field = payload.get("data")
        name_value = None
        try:
            if isinstance(data_field, str):
                import json as _json
                data_parsed = _json.loads(data_field)
            elif isinstance(data_field, dict):
                data_parsed = data_field
            else:
                data_parsed = {}
            name_value = (data_parsed.get("name") or {}).get("value")
        except Exception:
            name_value = None
        if isinstance(name_value, str) and name_value.strip():
            return name_value.strip()
        return payload.get("name") or "Безымянный"

class LSSCreate(BaseModel):
    payload: Dict[str, Any]
    name: Optional[str] = None

class LSSPublic(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    owner: Optional[str] = None
    created_at: datetime
    payload: Dict[str, Any]
