from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Text, Enum
from sqlalchemy.sql import func
from app.database.database import Base
import enum

class CropType(str, enum.Enum):
    COFFEE_ROBUSTA = "coffee_robusta"
    RICE = "rice"
    VEGETABLE = "vegetable"
    INDUSTRIAL = "industrial"

class GrowthStage(str, enum.Enum):
    SEEDLING = "seedling"  # Giai đoạn cây con
    VEGETATIVE = "vegetative"  # Giai đoạn sinh trưởng
    FLOWERING = "flowering"  # Giai đoạn ra hoa
    FRUITING = "fruiting"  # Giai đoạn đậu quả
    MATURE = "mature"  # Giai đoạn chín
    HARVEST = "harvest"  # Thu hoạch

class Crop(Base):
    __tablename__ = "crops"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    crop_type = Column(Enum(CropType), nullable=False)
    planting_date = Column(Date, nullable=False)
    area_hectares = Column(Float, nullable=False)  # Diện tích (ha)
    location = Column(String(200))  # Vị trí canh tác
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Digital Twin - Thông tin số hóa
    current_growth_stage = Column(Enum(GrowthStage), default=GrowthStage.SEEDLING)
    age_days = Column(Integer, default=0)  # Tuổi cây tính bằng ngày
    expected_harvest_date = Column(Date)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    notes = Column(Text)

