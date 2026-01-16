from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PestIdentificationBase(BaseModel):
    crop_id: int
    description: str
    location: Optional[str] = None

class PestIdentificationCreate(PestIdentificationBase):
    pass

class PestIdentificationResponse(PestIdentificationBase):
    id: int
    identified_pest_name: Optional[str] = None
    confidence_score: Optional[float] = None
    pest_type: Optional[str] = None
    severity: Optional[str] = None
    affected_area: Optional[float] = None
    is_beneficial: Optional[str] = None  # WP3 - Phân loại có lợi/hại
    recommendation: Optional[str] = None
    identified_at: datetime
    
    class Config:
        from_attributes = True

