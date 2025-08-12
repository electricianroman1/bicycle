from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from datetime import datetime
from ..db import db
from ..models import SheetIn, SheetOut, UpdateSheet
from ..dependencies import get_current_user
from ..models import UserPublic

router = APIRouter(prefix="/sheets", tags=["Sheets"])

def serialize_sheet(sheet) -> dict:
    return {
        "id": str(sheet["_id"]),
        "name": sheet["name"],
        "data": sheet["data"],
        "created_at": sheet["created_at"],
        "updated_at": sheet["updated_at"]
    }

@router.post("/", response_model=SheetOut)
async def create_sheet(sheet: SheetIn, current_user: UserPublic = Depends(get_current_user)):
    doc = sheet.dict()
    doc["created_at"] = datetime.utcnow()
    doc["updated_at"] = datetime.utcnow()
    doc["owner_id"] = ObjectId(current_user.id)
    res = await db.sheets.insert_one(doc)
    new_sheet = await db.sheets.find_one({"_id": res.inserted_id})
    return serialize_sheet(new_sheet)

@router.get("/", response_model=list[SheetOut])
async def list_sheets(current_user: UserPublic = Depends(get_current_user)):
    sheets = await db.sheets.find({"owner_id": ObjectId(current_user.id)}).to_list(100)
    return [serialize_sheet(s) for s in sheets]

@router.get("/{sheet_id}", response_model=SheetOut)
async def get_sheet(sheet_id: str, current_user: UserPublic = Depends(get_current_user)):
    if not ObjectId.is_valid(sheet_id):
        raise HTTPException(400, "Invalid ID")
    sheet = await db.sheets.find_one({"_id": ObjectId(sheet_id)})
    if not sheet:
        raise HTTPException(404, "Not found")
    if str(sheet.get("owner_id")) != current_user.id:
        raise HTTPException(403, "Not permitted")
    return serialize_sheet(sheet)

@router.put("/{sheet_id}", response_model=SheetOut)
async def update_sheet(sheet_id: str, update: UpdateSheet, current_user: UserPublic = Depends(get_current_user)):
    if not ObjectId.is_valid(sheet_id):
        raise HTTPException(400, "Invalid ID")
    sheet = await db.sheets.find_one({"_id": ObjectId(sheet_id)})
    if not sheet:
        raise HTTPException(404, "Not found")
    if str(sheet.get("owner_id")) != current_user.id:
        raise HTTPException(403, "Not permitted")
    update_data = {k: v for k, v in update.dict().items() if v is not None}
    if update_data:
        update_data["updated_at"] = datetime.utcnow()
        await db.sheets.update_one({"_id": ObjectId(sheet_id)}, {"$set": update_data})
    sheet = await db.sheets.find_one({"_id": ObjectId(sheet_id)})
    return serialize_sheet(sheet)

@router.delete("/{sheet_id}")
async def delete_sheet(sheet_id: str, current_user: UserPublic = Depends(get_current_user)):
    if not ObjectId.is_valid(sheet_id):
        raise HTTPException(400, "Invalid ID")
    sheet = await db.sheets.find_one({"_id": ObjectId(sheet_id)})
    if not sheet:
        raise HTTPException(404, "Not found")
    if str(sheet.get("owner_id")) != current_user.id:
        raise HTTPException(403, "Not permitted")
    res = await db.sheets.delete_one({"_id": ObjectId(sheet_id)})
    if res.deleted_count == 0:
        raise HTTPException(404, "Not found")
    return {"status": "deleted"}
