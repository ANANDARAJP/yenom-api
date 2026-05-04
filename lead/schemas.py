from pydantic import BaseModel
from typing import Optional
from enum import Enum

class ServiceEnum(str, Enum):
    fund_raising = "Fund Raising"
    bridge_funding = "Bridge Funding"
    private_finance = "Private Finance"
    msme_loans = "MSME Loans"
    ipo_advisory = "IPO Advisory"
    cibil_consulting = "CIBIL Consulting"

class LeadCreate(BaseModel):
    full_name: str
    phone_number: str
    service: ServiceEnum
    message: Optional[str] = ""
