import os
from motor.motor_asyncio import AsyncIOMotorClient

class Database:
    client: AsyncIOMotorClient = None

db = Database()

async def connect_to_mongo():
    MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
    db.client = AsyncIOMotorClient(MONGO_URL)
    print("Connected to MongoDB at", MONGO_URL)

async def close_mongo_connection():
    if db.client:
        db.client.close()
        print("Closed MongoDB connection")

def get_database():
    return db.client.yenom
