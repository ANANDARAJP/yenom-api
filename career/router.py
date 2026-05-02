import os
import shutil
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import EmailStr
from database import get_database
from career import crud

router = APIRouter()

MEDIA_DIR = "media/cvs"
os.makedirs(MEDIA_DIR, exist_ok=True)

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx", ".jpg", ".jpeg", ".png"}

@router.get("/career/", summary="List Careers")
async def list_career(db: AsyncIOMotorDatabase = Depends(get_database)):
    return await crud.list_career(db)

@router.post("/career/", summary="Create Career Submission")
async def create_career(
    name: str = Form(...),
    email: EmailStr = Form(...),
    phone_number: str = Form(...),
    subject: str = Form(""),
    message: str = Form(""),
    cv: UploadFile = File(...),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    # Validate file extension
    ext = os.path.splitext(cv.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Only PDF, DOC, DOCX, JPG, JPEG, and PNG files are allowed.")
    
    # Validate file size
    cv.file.seek(0, 2)
    file_size = cv.file.tell()
    cv.file.seek(0)
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Maximum size is 5MB.")

    # Save file
    file_path = os.path.join(MEDIA_DIR, cv.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(cv.file, buffer)
        
    return await crud.create_career(
        db=db,
        name=name,
        email=email,
        phone_number=phone_number,
        subject=subject,
        message=message,
        filename=cv.filename
    )

@router.get("/career/{idx}", summary="Get Career Submission")
async def get_career(idx: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    entry = await crud.get_career(db, idx)
    if not entry:
        raise HTTPException(status_code=404, detail="Not found")
    return entry

