from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CareLogBase(BaseModel):
    crop_id: int
    activity_type: str
    activity_date: datetime
    description: Optional[str] = None
    amount: Optional[float] = None
    unit: Optional[str] = None
    cost: Optional[float] = None
    performed_by: Optional[str] = None
    notes: Optional[str] = None

class CareLogCreate(CareLogBase):
    pass

class CareLogResponse(CareLogBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

