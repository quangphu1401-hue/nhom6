from datetime import date, timedelta
from app.models.crop_model import Crop, GrowthStage, CropType
from sqlalchemy.orm import Session
from typing import Optional

class CropService:
    @staticmethod
    def calculate_age_days(planting_date: date) -> int:
        """Tính tuổi cây tính bằng ngày"""
        return (date.today() - planting_date).days
    
    @staticmethod
    def determine_growth_stage(age_days: int, crop_type: CropType) -> GrowthStage:
        """Xác định giai đoạn sinh trưởng dựa trên tuổi cây và loại cây"""
        if crop_type == CropType.COFFEE_ROBUSTA:
            if age_days < 30:
                return GrowthStage.SEEDLING
            elif age_days < 180:
                return GrowthStage.VEGETATIVE
            elif age_days < 270:
                return GrowthStage.FLOWERING
            elif age_days < 330:
                return GrowthStage.FRUITING
            elif age_days < 365:
                return GrowthStage.MATURE
            else:
                return GrowthStage.HARVEST
        elif crop_type == CropType.RICE:
            if age_days < 20:
                return GrowthStage.SEEDLING
            elif age_days < 60:
                return GrowthStage.VEGETATIVE
            elif age_days < 90:
                return GrowthStage.FLOWERING
            elif age_days < 120:
                return GrowthStage.FRUITING
            elif age_days < 150:
                return GrowthStage.MATURE
            else:
                return GrowthStage.HARVEST
        else:
            # Default cho các loại cây khác
            if age_days < 30:
                return GrowthStage.SEEDLING
            elif age_days < 90:
                return GrowthStage.VEGETATIVE
            elif age_days < 150:
                return GrowthStage.FLOWERING
            elif age_days < 200:
                return GrowthStage.FRUITING
            elif age_days < 250:
                return GrowthStage.MATURE
            else:
                return GrowthStage.HARVEST
    
    @staticmethod
    def estimate_harvest_date(planting_date: date, crop_type: CropType) -> date:
        """Ước tính ngày thu hoạch"""
        if crop_type == CropType.COFFEE_ROBUSTA:
            # Cà phê Robusta: ~365 ngày
            return planting_date + timedelta(days=365)
        elif crop_type == CropType.RICE:
            # Lúa: ~120-150 ngày
            return planting_date + timedelta(days=135)
        else:
            # Default: 200 ngày
            return planting_date + timedelta(days=200)
    
    @staticmethod
    def update_crop_digital_twin(db: Session, crop: Crop) -> Crop:
        """Cập nhật Digital Twin cho cây trồng"""
        age_days = CropService.calculate_age_days(crop.planting_date)
        crop.age_days = age_days
        crop.current_growth_stage = CropService.determine_growth_stage(age_days, crop.crop_type)
        
        if not crop.expected_harvest_date:
            crop.expected_harvest_date = CropService.estimate_harvest_date(
                crop.planting_date, crop.crop_type
            )
        
        return crop

crop_service = CropService()

