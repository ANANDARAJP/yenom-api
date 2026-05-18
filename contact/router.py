# contact/router.py
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from motor.motor_asyncio import AsyncIOMotorDatabase

from database import get_database
from contact import crud, schemas
from utils.email import (
    send_admin_notification,
    send_auto_reply
)

router = APIRouter(
    prefix="/contact",
    tags=["Contact"]
)

@router.post(
    "/",
    summary="Submit Contact Us Form",
    description="Submit a new contact us form"
)
async def create_contact_us(
    contact_us: schemas.ContactUsCreate,
    background_tasks: BackgroundTasks,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    try:
        # Save Contact Data
        result_id = await crud.create_contact_us(db, contact_us)

        # Offload Emails to Background
        background_tasks.add_task(send_admin_notification, contact_us)
        background_tasks.add_task(send_auto_reply, contact_us)

        return {
            "success": True,
            "message": "Contact form submitted successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get(
    "/",
    summary="Get All Contact Us Submissions"
)
async def get_all_contact_us(
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    try:
        return await crud.get_all_contact_us(db)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get(
    "/{index}",
    summary="Get Contact Us Submission by Index"
)
async def get_contact_us_by_index(
    index: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    try:
        result = await crud.get_contact_us_by_index(db, index)
        if result is None:
            raise HTTPException(
                status_code=404,
                detail="Given Id is not found"
            )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )