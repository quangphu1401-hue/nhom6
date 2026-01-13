from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database.database import get_db
from app.models.care_log_model import CareLog
from app.schemas.care_log_schema import CareLogCreate, CareLogResponse

router = APIRouter()

@router.post("/", response_model=CareLogResponse)
async def create_care_log(care_log: CareLogCreate, db: Session = Depends(get_db)):
    """Tạo nhật ký chăm sóc"""
    db_care_log = CareLog(**care_log.dict())
    db.add(db_care_log)
    db.commit()
    db.refresh(db_care_log)
    return db_care_log

@router.get("/crop/{crop_id}", response_model=List[CareLogResponse])
async def get_care_logs_by_crop(crop_id: int, db: Session = Depends(get_db)):
    """Lấy nhật ký chăm sóc của một mùa vụ"""
    care_logs = db.query(CareLog).filter(
        CareLog.crop_id == crop_id
    ).order_by(CareLog.activity_date.desc()).all()
    return care_logs

@router.get("/", response_model=List[CareLogResponse])
async def get_all_care_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lấy tất cả nhật ký chăm sóc"""
    care_logs = db.query(CareLog).offset(skip).limit(limit).all()
    return care_logs

@router.delete("/{log_id}")
async def delete_care_log(log_id: int, db: Session = Depends(get_db)):
    """Xóa nhật ký chăm sóc"""
    care_log = db.query(CareLog).filter(CareLog.id == log_id).first()
    if not care_log:
        raise HTTPException(status_code=404, detail="Care log not found")
    
    db.delete(care_log)
    db.commit()
    return {"message": "Care log deleted successfully"}

