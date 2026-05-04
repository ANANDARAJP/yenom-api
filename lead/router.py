from fastapi import APIRouter, HTTPException, Depends, Form
from motor.motor_asyncio import AsyncIOMotorDatabase
from database import get_database
from lead import crud, schemas

router = APIRouter()

@router.post("/", summary="Submit Lead Form")
async def create_lead(
    full_name: str = Form(...),
    phone_number: str = Form(...),
    service: schemas.ServiceEnum = Form(...),
    message: str = Form(""),
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    lead = schemas.LeadCreate(
        full_name=full_name,
        phone_number=phone_number,
        service=service,
        message=message
    )
    await crud.create_lead(db, lead)
    return {"message": "Lead submitted successfully"}

@router.get("/", summary="Get All Leads")
async def get_all_leads(db: AsyncIOMotorDatabase = Depends(get_database)):
    return await crud.get_all_leads(db)

@router.get("/{index}", summary="Get Lead by Index")
async def get_lead_by_index(index: str, db: AsyncIOMotorDatabase = Depends(get_database)):
    result = await crud.get_lead_by_index(db, index)
    if result is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return result
