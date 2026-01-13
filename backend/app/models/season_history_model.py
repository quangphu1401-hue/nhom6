from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Date
from sqlalchemy.sql import func
from app.database.database import Base

class SeasonHistory(Base):
    __tablename__ = "season_history"
    
    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    
    # Thông tin mùa vụ
    season_name = Column(String(100))  # Tên mùa vụ (VD: "Mùa vụ 2024-2025")
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    
    # Kết quả mùa vụ
    yield_tonnes = Column(Float)  # Năng suất (tấn)
    yield_per_hectare = Column(Float)  # Năng suất/ha
    total_cost = Column(Float)  # Tổng chi phí (VND)
    total_revenue = Column(Float)  # Tổng doanh thu (VND)
    profit = Column(Float)  # Lợi nhuận (VND)
    
    # Chỉ số sức khỏe mùa vụ (SHI)
    avg_shi_score = Column(Float)  # Điểm SHI trung bình
    
    # Yếu tố ảnh hưởng
    weather_issues = Column(Text)  # Vấn đề về thời tiết
    pest_issues = Column(Text)  # Vấn đề về sâu bệnh
    other_issues = Column(Text)  # Vấn đề khác
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text)

