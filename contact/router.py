from fastapi import APIRouter, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from database import get_database
from contact import crud, schemas

router = APIRouter()

@router.post("/", summary="Submit Contact Us Form")
async def create_contact_us(
    contact_us: schemas.ContactUsCreate, 
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    await crud.create_contact_us(db, contact_us)
    return {"message": "Contact us form submitted successfully"}

@router.get("/", summary="Get All Contact Us Submissions")
async def get_all_contact_us(db: AsyncIOMotorDatabase = Depends(get_database)):
    return await crud.get_all_contact_us(db)

@router.get("/{index}", summary="Get Contact Us Submission by Index")
async def get_contact_us_by_index(index: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    result = await crud.get_contact_us_by_index(db, index)
    if result is None:
        raise HTTPException(status_code=404, detail="Submission not found")
    return result
