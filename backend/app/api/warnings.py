from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.models.crop_model import Crop
from app.services.shi_service import shi_service
from app.services.weather_service import weather_service

router = APIRouter()

@router.get("/crop/{crop_id}")
async def get_warnings(crop_id: int, db: Session = Depends(get_db)):
    """Lấy danh sách cảnh báo cho mùa vụ (Rule-based - Giai đoạn 2)"""
    crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    
    # Lấy thời tiết hiện tại
    weather_data = None
    if crop.latitude and crop.longitude:
        weather_data = await weather_service.get_current_weather(
            crop.latitude, crop.longitude
        )
    
    # Tính SHI và lấy cảnh báo
    shi_result = shi_service.calculate_shi(db, crop_id, weather_data)
    
    return {
        "crop_id": crop_id,
        "shi_score": shi_result["shi_score"],
        "warnings": shi_result.get("warnings", []),
        "warning_count": len(shi_result.get("warnings", []))
    }

