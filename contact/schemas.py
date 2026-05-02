from pydantic import BaseModel, EmailStr

class ContactUsCreate(BaseModel):
    full_name: str
    email: EmailStr
    subject: str
    message: str
