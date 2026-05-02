from motor.motor_asyncio import AsyncIOMotorDatabase
from contact.schemas import ContactUsCreate

async def create_contact_us(db: AsyncIOMotorDatabase, contact_us: ContactUsCreate):
    contact_dict = contact_us.model_dump()
    doc = await db.yenom_contact_us.find_one({"is_main": True})
    
    if not doc:
        await db.yenom_contact_us.insert_one({"is_main": True, "0": contact_dict})
    else:
        keys = [int(k) for k in doc.keys() if k.isdigit()]
        next_index = str(max(keys) + 1 if keys else 0)
        await db.yenom_contact_us.update_one({"is_main": True}, {"$set": {next_index: contact_dict}})

async def get_all_contact_us(db: AsyncIOMotorDatabase):
    doc = await db.yenom_contact_us.find_one({"is_main": True})
    if not doc:
        return {}
    return {k: v for k, v in doc.items() if k.isdigit()}

async def get_contact_us_by_index(db: AsyncIOMotorDatabase, index: str):
    doc = await db.yenom_contact_us.find_one({"is_main": True})
    if not doc or index not in doc:
        return None
    return doc[index]
