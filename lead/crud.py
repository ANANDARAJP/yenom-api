from motor.motor_asyncio import AsyncIOMotorDatabase
from lead.schemas import LeadCreate

async def create_lead(db: AsyncIOMotorDatabase, lead: LeadCreate):
    lead_dict = lead.model_dump()
    doc = await db.yenom_leads.find_one({"is_main": True})
    
    if not doc:
        await db.yenom_leads.insert_one({"is_main": True, "0": lead_dict})
    else:
        keys = [int(k) for k in doc.keys() if k.isdigit()]
        next_index = str(max(keys) + 1 if keys else 0)
        await db.yenom_leads.update_one({"is_main": True}, {"$set": {next_index: lead_dict}})

async def get_all_leads(db: AsyncIOMotorDatabase):
    doc = await db.yenom_leads.find_one({"is_main": True})
    if not doc:
        return {}
    return {k: v for k, v in doc.items() if k.isdigit()}

async def get_lead_by_index(db: AsyncIOMotorDatabase, index: str):
    doc = await db.yenom_leads.find_one({"is_main": True})
    if not doc or index not in doc:
        return None
    return doc[index]
