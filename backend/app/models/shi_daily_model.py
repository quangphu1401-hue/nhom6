from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database.database import Base

class SHIDaily(Base):
    """Bảng shi_daily - Tổng hợp SHI theo ngày (Giai đoạn 3)"""
    __tablename__ = "shi_daily"
    
    id = Column(Integer, primary_key=True, index=True)
    season_id = Column(Integer, ForeignKey("season.season_id"), nullable=False)
    date = Column(Date, nullable=False)
    
    # Các thành phần SHI
    weather_score = Column(Float)  # Điểm thời tiết
    care_score = Column(Float)  # Điểm chăm sóc (trung bình)
    growth_score = Column(Float)  # Điểm giai đoạn sinh trưởng
    
    # SHI tổng hợp
    shi_score = Column(Float, nullable=False)  # SHI = Weather × 0.3 + Care × 0.4 + Growth × 0.3
    
    # Cảnh báo
    warning_level = Column(String(20))  # low, medium, high
    warning_message = Column(String(500))  # Nội dung cảnh báo
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())

