from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase

async def get_raw_store(db: AsyncIOMotorDatabase):
    collection = db.yenom_careerstore
    store = await collection.find_one({"_id": 1})
    if not store:
        await collection.insert_one({"_id": 1})
        store = {"_id": 1}
    return store

async def list_career(db: AsyncIOMotorDatabase):
    store = await get_raw_store(db)
    active_entries = {}
    for k, v in store.items():
        if k.isdigit() and isinstance(v, dict) and v.get('deleted_at') is None:
            active_entries[k] = v
    return active_entries

async def create_career(
    db: AsyncIOMotorDatabase, 
    name: str, 
    email: str, 
    phone_number: str, 
    subject: str, 
    message: str, 
    filename: str
):
    store = await get_raw_store(db)
    
    indices = [int(k) for k in store.keys() if k.isdigit()]
    next_idx = str(max(indices) + 1) if indices else "0"
    next_id = (max(indices) + 1) if indices else 1
    
    now = datetime.utcnow().isoformat()
    
    new_entry = {
        "id": next_id,
        "name": name,
        "email": email,
        "phone_number": phone_number,
        "cv": f"cvs/{filename}",
        "subject": subject,
        "message": message,
        "created_at": now,
        "updated_at": now,
        "deleted_at": None
    }
    
    await db.yenom_careerstore.update_one({"_id": store["_id"]}, {"$set": {next_idx: new_entry}})
    return new_entry

async def get_career(db: AsyncIOMotorDatabase, idx: str):
    store = await get_raw_store(db)
    entry = store.get(idx)
    if entry and isinstance(entry, dict) and entry.get('deleted_at') is None:
        return entry
    return None
