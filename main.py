from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database import connect_to_mongo, close_mongo_connection
from contact.router import router as contact_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to Database
    await connect_to_mongo()
    yield
    # Shutdown: Close Connection
    await close_mongo_connection()

app = FastAPI(
    title="FTDS Contact API",
    description="Production-ready API for managing contact form submissions and notifications.",
    version="1.1.0",
    lifespan=lifespan
)

# CORS Middleware for Frontend Access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(contact_router)

@app.get("/", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "service": "FTDS Contact API",
        "version": "1.1.0"
    }