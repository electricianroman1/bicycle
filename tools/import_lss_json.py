import os, sys, json
from datetime import datetime
from pymongo import MongoClient

def extract_name(payload: dict) -> str:
    data_field = payload.get("data")
    try:
        if isinstance(data_field, str):
            data_parsed = json.loads(data_field)
        elif isinstance(data_field, dict):
            data_parsed = data_field
        else:
            data_parsed = {}
        name_value = (data_parsed.get("name") or {}).get("value")
        if isinstance(name_value, str) and name_value.strip():
            return name_value.strip()
    except Exception:
        pass
    return payload.get("name") or "Безымянный"

def main(path):
    uri = os.getenv("MONGO_URI", "mongodb://mongo:27017/dnd")
    client = MongoClient(uri)
    db = client.get_default_database()
    with open(path, "r", encoding="utf-8") as f:
        payload = json.load(f)
    doc = {
        "payload": payload,
        "name": extract_name(payload),
        "owner": os.getenv("IMPORT_OWNER", "demo"),
        "created_at": datetime.utcnow()
    }
    res = db.sheets.insert_one(doc)
    print("Inserted sheet id:", res.inserted_id)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python import_lss_json.py <path_to_json>")
        sys.exit(1)
    main(sys.argv[1])
