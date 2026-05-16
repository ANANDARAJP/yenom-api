import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from contextlib import asynccontextmanager

from database import connect_to_mongo, close_mongo_connection, get_database
from contact import router as contact_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect
    await connect_to_mongo()
    yield
    # Disconnect
    await close_mongo_connection()

app = FastAPI(
    title="FTDS API",
    
    version="1.0.1",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(contact_router.router, prefix="/contact-us", tags=["Contact Us"])


        
@app.get("/", tags=["Health"])
async def health_check():
    return {"status": "ok", "message": "FTDS API is running"}
