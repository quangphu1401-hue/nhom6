from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.database import get_db
from app.models.pest_model import PestIdentification
from app.models.crop_model import Crop
from app.schemas.pest_schema import PestIdentificationCreate, PestIdentificationResponse
from app.services.ai_service import ai_service
import base64

router = APIRouter()

@router.post("/identify", response_model=PestIdentificationResponse)
async def identify_pest(pest_data: PestIdentificationCreate, db: Session = Depends(get_db)):
    """Nhận diện sâu bệnh dựa trên mô tả (WP3)"""
    # Kiểm tra crop tồn tại
    crop = db.query(Crop).filter(Crop.id == pest_data.crop_id).first()
    if not crop:
        raise HTTPException(status_code=404, detail="Crop not found")
    
    # Sử dụng AI để nhận diện
    ai_result = await ai_service.identify_pest(
        pest_data.description,
        crop.crop_type.value
    )
    
    # Lưu kết quả vào database
    is_beneficial = ai_result.get("is_beneficial")
    # Convert boolean to string for database
    is_beneficial_str = str(is_beneficial).lower() if is_beneficial is not None else None
    
    db_pest = PestIdentification(
        crop_id=pest_data.crop_id,
        description=pest_data.description,
        location=pest_data.location,
        identified_pest_name=ai_result.get("identified_pest_name"),
        confidence_score=ai_result.get("confidence_score"),
        pest_type=ai_result.get("pest_type"),
        severity=ai_result.get("severity"),
        is_beneficial=is_beneficial_str,  # WP3 - Phân loại có lợi/hại
        recommendation=ai_result.get("recommendation")
    )
    
    db.add(db_pest)
    db.commit()
    db.refresh(db_pest)
    return db_pest

@router.get("/crop/{crop_id}", response_model=List[PestIdentificationResponse])
async def get_pests_by_crop(crop_id: int, db: Session = Depends(get_db)):
    """Lấy lịch sử nhận diện sâu bệnh của một mùa vụ"""
    pests = db.query(PestIdentification).filter(
        PestIdentification.crop_id == crop_id
    ).order_by(PestIdentification.identified_at.desc()).all()
    return pests

@router.get("/", response_model=List[PestIdentificationResponse])
async def get_all_pests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lấy tất cả lịch sử nhận diện sâu bệnh"""
    pests = db.query(PestIdentification).offset(skip).limit(limit).all()
    return pests

@router.post("/identify-image")
async def identify_pest_from_image(
    file: UploadFile = File(...),
    crop_id: Optional[int] = Form(None),
    location: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Nhận diện côn trùng/sâu bệnh từ ảnh (WP3 - Mở rộng)"""
    # Kiểm tra crop nếu có
    if crop_id:
        crop = db.query(Crop).filter(Crop.id == crop_id).first()
        if not crop:
            raise HTTPException(status_code=404, detail="Crop not found")
        crop_type = crop.crop_type.value
    else:
        crop_type = "coffee_robusta"
    
    # Đọc ảnh
    try:
        image_data = await file.read()
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        mime_type = file.content_type or "image/jpeg"
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Lỗi đọc ảnh: {str(e)}")
    
    # Sử dụng AI để phân tích ảnh
    ai_result = await ai_service.identify_pest_from_image(
        image_base64, mime_type, crop_type
    )
    
    # Lưu kết quả vào database (chỉ lưu nếu có crop_id hợp lệ)
    result_data = {
        **ai_result,
        "image_filename": file.filename
    }
    
    # Chỉ lưu vào DB nếu có crop_id hợp lệ
    if crop_id:
        try:
            db_pest = PestIdentification(
                crop_id=crop_id,
                description=f"Phân tích từ ảnh: {file.filename}",
                location=location,
                identified_pest_name=ai_result.get("identified_pest_name"),
                confidence_score=ai_result.get("confidence_score"),
                pest_type=ai_result.get("pest_type"),
                severity=ai_result.get("severity"),
                recommendation=ai_result.get("recommendation"),
                affected_area=ai_result.get("affected_area")
            )
            db.add(db_pest)
            db.commit()
            db.refresh(db_pest)
            result_data["id"] = db_pest.id
        except Exception as e:
            print(f"Lỗi lưu vào database: {e}")
            # Vẫn trả về kết quả dù không lưu được
    
    return result_data

