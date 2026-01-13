from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional
from app.models.crop_model import CropType, GrowthStage

class CropBase(BaseModel):
    name: str
    crop_type: CropType
    planting_date: date
    area_hectares: float
    location: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    notes: Optional[str] = None

class CropCreate(CropBase):
    pass

class CropUpdate(BaseModel):
    name: Optional[str] = None
    current_growth_stage: Optional[GrowthStage] = None
    notes: Optional[str] = None

class CropResponse(CropBase):
    id: int
    current_growth_stage: GrowthStage
    age_days: int
    expected_harvest_date: Optional[date] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

