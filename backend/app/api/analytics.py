from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, Any
from app.database.database import get_db
from app.models.crop_model import Crop
from app.models.care_log_model import CareLog
from app.models.season_history_model import SeasonHistory
from app.services.shi_service import shi_service
from app.services.weather_service import weather_service

router = APIRouter()

@router.get("/shi/{crop_id}")
async def get_shi_score(crop_id: int, db: Session = Depends(get_db)):
    """Tính toán chỉ số SHI (Season Health Index) cho mùa vụ (WP2)"""
    crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    
    # Lấy thời tiết hiện tại nếu có tọa độ
    weather_data = None
    if crop.latitude and crop.longitude:
        weather_data = await weather_service.get_current_weather(
            crop.latitude, crop.longitude
        )
    
    # Tính SHI
    shi_result = shi_service.calculate_shi(db, crop_id, weather_data)
    
    return {
        "crop_id": crop_id,
        "crop_name": crop.name,
        **shi_result,
        "formula": "SHI = Weather × 0.3 + Care × 0.4 + Growth × 0.3"
    }

@router.get("/crop/{crop_id}/summary")
async def get_crop_summary(crop_id: int, db: Session = Depends(get_db)):
    """Tổng hợp thông tin mùa vụ"""
    crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    
    # Đếm số lượng hoạt động chăm sóc
    care_count = db.query(func.count(CareLog.id)).filter(
        CareLog.crop_id == crop_id
    ).scalar()
    
    # Tính tổng chi phí chăm sóc
    total_cost = db.query(func.sum(CareLog.cost)).filter(
        CareLog.crop_id == crop_id,
        CareLog.cost.isnot(None)
    ).scalar() or 0
    
    # Lấy SHI
    shi_result = shi_service.calculate_shi(db, crop_id)
    
    return {
        "crop": {
            "id": crop.id,
            "name": crop.name,
            "crop_type": crop.crop_type.value,
            "age_days": crop.age_days,
            "growth_stage": crop.current_growth_stage.value,
            "area_hectares": crop.area_hectares
        },
        "statistics": {
            "care_activities_count": care_count,
            "total_care_cost": float(total_cost),
            "shi_score": shi_result["shi_score"],
            "shi_status": shi_result["status_vn"]
        }
    }

@router.get("/season-history/{crop_id}")
async def get_season_history(crop_id: int, db: Session = Depends(get_db)):
    """Lấy lịch sử các mùa vụ trước"""
    histories = db.query(SeasonHistory).filter(
        SeasonHistory.crop_id == crop_id
    ).order_by(SeasonHistory.start_date.desc()).all()
    
    return [{
        "id": h.id,
        "season_name": h.season_name,
        "start_date": h.start_date.isoformat() if h.start_date else None,
        "end_date": h.end_date.isoformat() if h.end_date else None,
        "yield_tonnes": h.yield_tonnes,
        "yield_per_hectare": h.yield_per_hectare,
        "total_cost": h.total_cost,
        "total_revenue": h.total_revenue,
        "profit": h.profit,
        "avg_shi_score": h.avg_shi_score
    } for h in histories]

