from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, Enum
from sqlalchemy.sql import func
from app.database.database import Base
import enum

class GrowthStage(str, enum.Enum):
    SEEDLING = "seedling"  # Cây con
    VEGETATIVE = "vegetative"  # Sinh trưởng
    FLOWERING = "flowering"  # Ra hoa
    FRUITING = "fruiting"  # Đậu quả
    MATURE = "mature"  # Chín
    HARVEST = "harvest"  # Thu hoạch

class Season(Base):
    """Bảng season theo yêu cầu PDF - Giai đoạn 1"""
    __tablename__ = "season"
    
    season_id = Column(Integer, primary_key=True, index=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    plant_age = Column(Integer)  # Tuổi cây (năm)
    growth_stage = Column(Enum(GrowthStage))  # Giai đoạn sinh trưởng
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    notes = Column(Text)

