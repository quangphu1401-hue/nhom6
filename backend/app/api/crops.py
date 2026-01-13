from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.models.crop_model import Crop
from app.schemas.crop_schema import CropCreate, CropUpdate, CropResponse
from app.services.crop_service import crop_service

router = APIRouter()

@router.post("/", response_model=CropResponse)
async def create_crop(crop: CropCreate, db: Session = Depends(get_db)):
    """Tạo mùa vụ mới"""
    db_crop = Crop(**crop.dict())
    
    # Tính toán Digital Twin
    db_crop = crop_service.update_crop_digital_twin(db, db_crop)
    
    db.add(db_crop)
    db.commit()
    db.refresh(db_crop)
    return db_crop

@router.get("/", response_model=List[CropResponse])
async def get_crops(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lấy danh sách mùa vụ"""
    crops = db.query(Crop).offset(skip).limit(limit).all()
    
    # Cập nhật Digital Twin cho tất cả crops
    for crop in crops:
        crop = crop_service.update_crop_digital_twin(db, crop)
        db.commit()
    
    return crops

@router.get("/{crop_id}", response_model=CropResponse)
async def get_crop(crop_id: int, db: Session = Depends(get_db)):
    """Lấy thông tin chi tiết mùa vụ"""
    crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    
    # Cập nhật Digital Twin
    crop = crop_service.update_crop_digital_twin(db, crop)
    db.commit()
    
    return crop

@router.put("/{crop_id}", response_model=CropResponse)
async def update_crop(crop_id: int, crop_update: CropUpdate, db: Session = Depends(get_db)):
    """Cập nhật thông tin mùa vụ"""
    crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    
    update_data = crop_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(crop, field, value)
    
    # Cập nhật Digital Twin
    crop = crop_service.update_crop_digital_twin(db, crop)
    db.commit()
    db.refresh(crop)
    return crop

@router.delete("/{crop_id}")
async def delete_crop(crop_id: int, db: Session = Depends(get_db)):
    """Xóa mùa vụ"""
    crop = db.query(Crop).filter(Crop.id == crop_id).first()
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    
    db.delete(crop)
    db.commit()
    return {"message": "Crop deleted successfully"}

