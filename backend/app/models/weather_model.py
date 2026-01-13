from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.database import Base

class WeatherData(Base):
    __tablename__ = "weather_data"
    
    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=True)
    
    # Thông tin vị trí
    location = Column(String(200), nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Dữ liệu thời tiết
    temperature = Column(Float)  # Nhiệt độ (°C)
    humidity = Column(Float)  # Độ ẩm (%)
    precipitation = Column(Float)  # Lượng mưa (mm)
    wind_speed = Column(Float)  # Tốc độ gió (m/s)
    pressure = Column(Float)  # Áp suất (hPa)
    weather_description = Column(String(200))  # Mô tả thời tiết
    
    # Dự báo
    forecast_date = Column(DateTime(timezone=True))
    is_forecast = Column(Integer, default=0)  # 0 = dữ liệu thực, 1 = dự báo
    
    # Metadata
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    source = Column(String(50), default="openweather")  # Nguồn dữ liệu

