import os
from fastapi import FastAPI, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from contextlib import asynccontextmanager

from database import connect_to_mongo, close_mongo_connection, get_database
from database import connect_to_mongo, close_mongo_connection, get_database
from contact import router as contact_router
from career import router as career_router

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

app.include_router(contact_router.router, prefix="/contact-us", tags=["Contact Us"])
app.include_router(career_router.router, prefix="/api/careers", tags=["Careers"])



@app.get("/", tags=["Health"])
async def health_check():
    return {"status": "ok", "message": "Yenom API is running"}
