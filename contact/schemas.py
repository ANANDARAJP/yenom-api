# contact/schemas.py

from pydantic import BaseModel, EmailStr


class ContactUsCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    service: str
    message: str