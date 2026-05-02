import os
from fastapi import FastAPI, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from contextlib import asynccontextmanager

from database import connect_to_mongo, close_mongo_connection, get_database
from models import ContactUsCreate

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect
    await connect_to_mongo()
    yield
    # Disconnect
    await close_mongo_connection()

app = FastAPI(
    title="Yenom Market API",
    description="API for Yenom Market Contact Us and Careers forms",
    version="1.0.0",
    lifespan=lifespan
)

@app.post("/contact-us/", summary="Submit Contact Us Form", tags=["Contact Us"])
async def create_contact_us(
    contact_us: ContactUsCreate, 
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    contact_dict = contact_us.model_dump()
    doc = await db.yenom_contact_us.find_one({"is_main": True})
    
    if not doc:
        await db.yenom_contact_us.insert_one({"is_main": True, "0": contact_dict})
    else:
        keys = [int(k) for k in doc.keys() if k.isdigit()]
        next_index = str(max(keys) + 1 if keys else 0)
        await db.yenom_contact_us.update_one({"is_main": True}, {"$set": {next_index: contact_dict}})
        
    return {"message": "Contact us form submitted successfully"}

@app.get("/contact-us/", summary="Get All Contact Us Submissions", tags=["Contact Us"])
async def get_all_contact_us(db: AsyncIOMotorDatabase = Depends(get_database)):
    doc = await db.yenom_contact_us.find_one({"is_main": True})
    if not doc:
        return {}
    return {k: v for k, v in doc.items() if k.isdigit()}

@app.get("/contact-us/{index}", summary="Get Contact Us Submission by Index", tags=["Contact Us"])
async def get_contact_us_by_index(index: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    doc = await db.yenom_contact_us.find_one({"is_main": True})
    if not doc or index not in doc:
        raise HTTPException(status_code=404, detail="Submission not found")
    return doc[index]



@app.get("/", tags=["Health"])
async def health_check():
    return {"status": "ok", "message": "Yenom API is running"}
