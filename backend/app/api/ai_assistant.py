from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.database.database import get_db
from app.models.season_history_model import SeasonHistory
from app.models.crop_model import Crop
from app.services.ai_service import ai_service
import json

router = APIRouter()

class AIQuestionRequest(BaseModel):
    crop_id: Optional[int] = None
    question: str

@router.post("/ask")
async def ask_ai_assistant(request: AIQuestionRequest, db: Session = Depends(get_db)):
    """Trợ lý ảo AI - Phân tích dữ liệu và trả lời câu hỏi (WP4)"""
    
    # Nếu có crop_id, lấy dữ liệu mùa vụ
    season_data = None
    if request.crop_id:
        crop = db.query(Crop).filter(Crop.id == request.crop_id).first()
        if not crop:
            raise HTTPException(status_code=404, detail="Crop not found")
        
        # Lấy lịch sử mùa vụ
        histories = db.query(SeasonHistory).filter(
            SeasonHistory.crop_id == request.crop_id
        ).all()
        
        season_data = {
            "crop_info": {
                "name": crop.name,
                "crop_type": crop.crop_type.value,
                "age_days": crop.age_days,
                "growth_stage": crop.current_growth_stage.value,
                "area_hectares": crop.area_hectares
            },
            "season_history": [
                {
                    "season_name": h.season_name,
                    "yield_tonnes": h.yield_tonnes,
                    "yield_per_hectare": h.yield_per_hectare,
                    "total_cost": h.total_cost,
                    "total_revenue": h.total_revenue,
                    "profit": h.profit,
                    "avg_shi_score": h.avg_shi_score
                }
                for h in histories
            ]
        }
    
    # Gọi AI service
    answer = await ai_service.analyze_season_data(
        season_data or {},
        request.question
    )
    
    return {
        "question": request.question,
        "answer": answer,
        "crop_id": request.crop_id
    }

