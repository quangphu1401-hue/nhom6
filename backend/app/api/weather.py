from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.database import get_db
from app.models.weather_model import WeatherData
from app.schemas.weather_schema import WeatherDataCreate, WeatherDataResponse
from app.services.weather_service import weather_service

router = APIRouter()

@router.get("/current")
async def get_current_weather(lat: float, lon: float):
    """Lấy thời tiết hiện tại từ OpenWeatherMap"""
    weather = await weather_service.get_current_weather(lat, lon)
    if not weather:
        raise HTTPException(status_code=503, detail="Weather service unavailable")
    return weather

@router.get("/forecast")
async def get_forecast(lat: float, lon: float, days: int = 7):
    """Lấy dự báo thời tiết"""
    forecast = await weather_service.get_forecast(lat, lon, days)
    if not forecast:
        raise HTTPException(status_code=503, detail="Forecast service unavailable")
    return {"forecast": forecast}

@router.post("/", response_model=WeatherDataResponse)
async def create_weather_data(weather: WeatherDataCreate, db: Session = Depends(get_db)):
    """Lưu dữ liệu thời tiết vào database"""
    db_weather = WeatherData(**weather.dict())
    db.add(db_weather)
    db.commit()
    db.refresh(db_weather)
    return db_weather

@router.get("/crop/{crop_id}", response_model=List[WeatherDataResponse])
async def get_weather_by_crop(crop_id: int, db: Session = Depends(get_db)):
    """Lấy lịch sử thời tiết của một mùa vụ"""
    weather_data = db.query(WeatherData).filter(
        WeatherData.crop_id == crop_id
    ).order_by(WeatherData.recorded_at.desc()).limit(30).all()
    return weather_data

