from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class WeatherDataBase(BaseModel):
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    precipitation: Optional[float] = None
    wind_speed: Optional[float] = None
    pressure: Optional[float] = None
    weather_description: Optional[str] = None

class WeatherDataCreate(WeatherDataBase):
    crop_id: Optional[int] = None
    forecast_date: Optional[datetime] = None
    is_forecast: int = 0

class WeatherDataResponse(WeatherDataBase):
    id: int
    crop_id: Optional[int] = None
    forecast_date: Optional[datetime] = None
    is_forecast: int
    recorded_at: datetime
    source: str
    
    class Config:
        from_attributes = True

