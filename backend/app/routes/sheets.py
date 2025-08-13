from fastapi import APIRouter, Depends, HTTPException, Body
from typing import List, Any, Dict
from bson import ObjectId
from ..models import LSSSheet, LSSCreate, LSSPublic
from ..utils import get_db, get_current_user
from datetime import datetime

router = APIRouter(prefix="/sheets", tags=["sheets"])

def obj_to_public(doc: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "_id": str(doc["_id"]),
        "name": doc.get("name"),
        "owner": doc.get("owner"),
        "created_at": doc.get("created_at"),
        "payload": doc.get("payload"),
    }

@router.get("/", response_model=List[LSSPublic])
async def list_sheets(db = Depends(get_db), user: dict = Depends(get_current_user)):
    cursor = db.sheets.find({"owner": user["username"]}).sort("created_at", -1)
    return [obj_to_public(x) for x in await cursor.to_list(length=1000)]

@router.post("/", response_model=LSSPublic)
async def create_sheet(data: LSSCreate, db = Depends(get_db), user: dict = Depends(get_current_user)):
    sheet = LSSSheet(payload=data.payload, name=data.name or None, owner=user["username"])
    doc = sheet.dict()
    res = await db.sheets.insert_one(doc)
    doc["_id"] = res.inserted_id
    return obj_to_public(doc)

@router.get("/{sheet_id}", response_model=LSSPublic)
async def get_sheet(sheet_id: str, db = Depends(get_db), user: dict = Depends(get_current_user)):
    try:
        _id = ObjectId(sheet_id)
    except Exception:
        raise HTTPException(404, "Sheet not found")
    doc = await db.sheets.find_one({"_id": _id, "owner": user["username"]})
    if not doc:
        raise HTTPException(404, "Sheet not found")
    return obj_to_public(doc)

@router.patch("/{sheet_id}", response_model=LSSPublic)
async def update_sheet(sheet_id: str, data: LSSCreate = Body(...), db = Depends(get_db), user: dict = Depends(get_current_user)):
    try:
        _id = ObjectId(sheet_id)
    except Exception:
        raise HTTPException(404, "Sheet not found")
    from ..models import LSSSheet as _Tmp
    patch_name = data.name or _Tmp(payload=data.payload, name=None).name
    upd = {"payload": data.payload, "name": patch_name}
    res = await db.sheets.find_one_and_update(
        {"_id": _id, "owner": user["username"]},
        {"$set": upd},
        return_document=True
    )
    if not res:
        raise HTTPException(404, "Sheet not found")
    return obj_to_public(res)

@router.delete("/{sheet_id}")
async def delete_sheet(sheet_id: str, db = Depends(get_db), user: dict = Depends(get_current_user)):
    try:
        _id = ObjectId(sheet_id)
    except Exception:
        raise HTTPException(404, "Sheet not found")
    res = await db.sheets.delete_one({"_id": _id, "owner": user["username"]})
    if res.deleted_count == 0:
        raise HTTPException(404, "Sheet not found")
    return {"ok": True}
