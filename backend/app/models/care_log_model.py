from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.database import Base
import enum

class CareActivityType(str, enum.Enum):
    WATERING = "watering"  # Tưới tiêu
    FERTILIZING = "fertilizing"  # Bón phân
    PEST_CONTROL = "pest_control"  # Phòng trừ sâu bệnh
    PRUNING = "pruning"  # Tỉa cành
    HARVESTING = "harvesting"  # Thu hoạch
    OTHER = "other"  # Khác

class CareLog(Base):
    __tablename__ = "care_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    
    # Thông tin hoạt động
    activity_type = Column(String(50), nullable=False)
    activity_date = Column(DateTime(timezone=True), nullable=False)
    description = Column(Text)
    
    # Chi tiết hoạt động
    amount = Column(Float)  # Số lượng (kg, lít, etc.)
    unit = Column(String(20))  # Đơn vị
    cost = Column(Float)  # Chi phí (VND)
    
    # Người thực hiện
    performed_by = Column(String(100))
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text)

