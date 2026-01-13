from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from app.database.database import Base

class PestIdentification(Base):
    __tablename__ = "pest_identifications"
    
    id = Column(Integer, primary_key=True, index=True)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=True)  # Cho phép null
    
    # Mô tả côn trùng
    description = Column(Text, nullable=False)  # Mô tả từ người dùng
    identified_pest_name = Column(String(200))  # Tên côn trùng được nhận diện
    confidence_score = Column(Float)  # Độ tin cậy (0-1)
    
    # Thông tin côn trùng
    pest_type = Column(String(50))  # Loại: insect, disease, weed
    severity = Column(String(20))  # Mức độ: low, medium, high
    affected_area = Column(Float)  # Diện tích bị ảnh hưởng (ha)
    
    # Khuyến nghị
    recommendation = Column(Text)  # Khuyến nghị xử lý
    
    # Metadata
    identified_at = Column(DateTime(timezone=True), server_default=func.now())
    location = Column(String(200))

