from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict, Any, Optional
from datetime import date, datetime, timedelta
from pydantic import BaseModel
from app.database.database import get_db
from app.models.crop_model import Crop
from app.models.care_log_model import CareLog
from app.models.season_history_model import SeasonHistory
from app.models.shi_daily_model import SHIDaily
from app.services.shi_service import shi_service
from app.services.weather_service import weather_service

router = APIRouter()

class SHIDailyCreate(BaseModel):
    crop_id: int
    shi_score: float
    weather_score: float
    care_score: float
    growth_score: float
    recorded_date: Optional[date] = None
    warning_level: Optional[str] = None
    warning_message: Optional[str] = None

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

@router.post("/shi-daily")
async def save_shi_daily(data: SHIDailyCreate, db: Session = Depends(get_db)):
    """Lưu SHI daily (cho n8n workflow tự động)"""
    crop = db.query(Crop).filter(Crop.id == data.crop_id).first()
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    
    # Tìm season_id từ crop (nếu có bảng season)
    # Tạm thời dùng crop_id làm season_id
    season_id = data.crop_id
    
    recorded_date = data.recorded_date or date.today()
    
    # Kiểm tra xem đã có record cho ngày này chưa
    existing = db.query(SHIDaily).filter(
        SHIDaily.season_id == season_id,
        SHIDaily.date == recorded_date
    ).first()
    
    if existing:
        # Cập nhật
        existing.shi_score = data.shi_score
        existing.weather_score = data.weather_score
        existing.care_score = data.care_score
        existing.growth_score = data.growth_score
        existing.warning_level = data.warning_level
        existing.warning_message = data.warning_message
        db.commit()
        db.refresh(existing)
        return {"message": "Updated", "id": existing.id}
    else:
        # Tạo mới
        shi_daily = SHIDaily(
            season_id=season_id,
            date=recorded_date,
            shi_score=data.shi_score,
            weather_score=data.weather_score,
            care_score=data.care_score,
            growth_score=data.growth_score,
            warning_level=data.warning_level,
            warning_message=data.warning_message
        )
        db.add(shi_daily)
        db.commit()
        db.refresh(shi_daily)
        return {"message": "Created", "id": shi_daily.id}

@router.get("/shi-daily/{crop_id}")
async def get_shi_daily_history(crop_id: int, days: int = 30, db: Session = Depends(get_db)):
    """Lấy lịch sử SHI daily (cho Superset visualization)"""
    crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    
    season_id = crop_id  # Tạm thời
    cutoff_date = date.today() - timedelta(days=days)
    
    records = db.query(SHIDaily).filter(
        SHIDaily.season_id == season_id,
        SHIDaily.date >= cutoff_date
    ).order_by(SHIDaily.date.desc()).all()
    
    return [{
        "date": r.date.isoformat() if r.date else None,
        "shi_score": r.shi_score,
        "weather_score": r.weather_score,
        "care_score": r.care_score,
        "growth_score": r.growth_score,
        "warning_level": r.warning_level,
        "warning_message": r.warning_message
    } for r in records]

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

@router.get("/yield-factors/{crop_id}")
async def analyze_yield_factors(crop_id: int, db: Session = Depends(get_db)):
    """Phân tích yếu tố ảnh hưởng đến năng suất (WP4 - Cải thiện)"""
    crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    
    # Lấy lịch sử mùa vụ
    histories = db.query(SeasonHistory).filter(
        SeasonHistory.crop_id == crop_id
    ).order_by(SeasonHistory.start_date.desc()).limit(10).all()
    
    if not histories:
        return {
            "crop_id": crop_id,
            "message": "Chưa có dữ liệu lịch sử mùa vụ",
            "factors": []
        }
    
    # Phân tích correlation
    factors = []
    
    # 1. Phân tích SHI vs Năng suất
    shi_yield_data = [
        {"shi": h.avg_shi_score or 0, "yield": h.yield_per_hectare or 0}
        for h in histories if h.avg_shi_score and h.yield_per_hectare
    ]
    
    if len(shi_yield_data) >= 2:
        avg_shi = sum(d["shi"] for d in shi_yield_data) / len(shi_yield_data)
        avg_yield = sum(d["yield"] for d in shi_yield_data) / len(shi_yield_data)
        
        # Tính correlation đơn giản
        high_shi_yields = [d["yield"] for d in shi_yield_data if d["shi"] >= avg_shi]
        low_shi_yields = [d["yield"] for d in shi_yield_data if d["shi"] < avg_shi]
        
        if high_shi_yields and low_shi_yields:
            avg_high = sum(high_shi_yields) / len(high_shi_yields)
            avg_low = sum(low_shi_yields) / len(low_shi_yields)
            
            if avg_high > avg_low * 1.1:  # Chênh lệch > 10%
                factors.append({
                    "factor": "SHI Score",
                    "impact": "positive",
                    "description": f"SHI cao (>={avg_shi:.1f}) có năng suất trung bình {avg_high:.2f} tấn/ha, cao hơn {((avg_high/avg_low - 1) * 100):.1f}% so với SHI thấp",
                    "recommendation": "Duy trì SHI >= 70 để đạt năng suất tối ưu"
                })
    
    # 2. Phân tích Chi phí vs Lợi nhuận
    cost_profit_data = [
        {"cost": h.total_cost or 0, "profit": h.profit or 0, "yield": h.yield_per_hectare or 0}
        for h in histories if h.total_cost and h.profit
    ]
    
    if len(cost_profit_data) >= 2:
        high_cost = [d for d in cost_profit_data if d["cost"] >= sum(d["cost"] for d in cost_profit_data) / len(cost_profit_data)]
        if high_cost:
            avg_profit_high_cost = sum(d["profit"] for d in high_cost) / len(high_cost)
            factors.append({
                "factor": "Chi phí chăm sóc",
                "impact": "positive" if avg_profit_high_cost > 0 else "negative",
                "description": f"Đầu tư chăm sóc cao có lợi nhuận trung bình {avg_profit_high_cost:,.0f} VND",
                "recommendation": "Cân bằng chi phí chăm sóc với năng suất dự kiến"
            })
    
    # 3. Phân tích vấn đề thời tiết
    weather_issues = [h.weather_issues for h in histories if h.weather_issues]
    if weather_issues:
        factors.append({
            "factor": "Thời tiết",
            "impact": "negative",
            "description": f"{len(weather_issues)}/{len(histories)} mùa vụ có vấn đề về thời tiết",
            "recommendation": "Theo dõi dự báo thời tiết và có biện pháp phòng ngừa"
        })
    
    # 4. Phân tích sâu bệnh
    pest_issues = [h.pest_issues for h in histories if h.pest_issues]
    if pest_issues:
        factors.append({
            "factor": "Sâu bệnh",
            "impact": "negative",
            "description": f"{len(pest_issues)}/{len(histories)} mùa vụ có vấn đề về sâu bệnh",
            "recommendation": "Tăng cường phòng trừ sâu bệnh định kỳ"
        })
    
    return {
        "crop_id": crop_id,
        "total_seasons": len(histories),
        "factors": factors,
        "summary": f"Phân tích {len(histories)} mùa vụ, tìm thấy {len(factors)} yếu tố ảnh hưởng"
    }

