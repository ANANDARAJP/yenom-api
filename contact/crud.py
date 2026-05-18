from datetime import datetime
from bson import ObjectId

COLLECTION_NAME = "contact_us"

async def create_contact_us(db, contact_us):
    contact_data = {
        "name": contact_us.name,
        "email": contact_us.email,
        "phone": contact_us.phone,
        "service": contact_us.service,
        "message": contact_us.message,
        "created_at": datetime.utcnow()
    }
    result = await db[COLLECTION_NAME].insert_one(contact_data)
    return str(result.inserted_id)

async def get_all_contact_us(db):
    contacts = []
    async for contact in db[COLLECTION_NAME].find():
        contact["_id"] = str(contact["_id"])
        contacts.append(contact)
    return contacts

async def get_contact_us_by_index(db, index: str):
    try:
        idx = int(index)
        # Using skip and limit for efficient indexing
        cursor = db[COLLECTION_NAME].find().skip(idx).limit(1)
        async for contact in cursor:
            contact["_id"] = str(contact["_id"])
            return contact
        return None
    except (ValueError, TypeError):
        return None