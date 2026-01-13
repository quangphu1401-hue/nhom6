from typing import Optional, Dict, Any
from datetime import datetime
from app.models.weather_model import WeatherData
from app.models.care_log_model import CareLog
from sqlalchemy.orm import Session
from sqlalchemy import func

class SHIService:
    """Service tính toán chỉ số sức khỏe mùa vụ (Season Health Index)"""
    
    @staticmethod
    def calculate_shi(
        db: Session,
        crop_id: int,
        weather_data: Optional[Dict[str, Any]] = None,
        recent_care_logs: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Tính toán SHI dựa trên:
        - Điều kiện thời tiết (nhiệt độ, độ ẩm, mưa)
        - Lịch sử chăm sóc (tưới tiêu, bón phân, phòng trừ sâu bệnh)
        - Tần suất chăm sóc
        """
        
        # Lấy dữ liệu thời tiết gần nhất
        if not weather_data:
            latest_weather = db.query(WeatherData).filter(
                WeatherData.crop_id == crop_id,
                WeatherData.is_forecast == 0
            ).order_by(WeatherData.recorded_at.desc()).first()
            
            if latest_weather:
                weather_data = {
                    "temperature": latest_weather.temperature,
                    "humidity": latest_weather.humidity,
                    "precipitation": latest_weather.precipitation or 0
                }
        
        # Lấy lịch sử chăm sóc 30 ngày gần nhất
        if not recent_care_logs:
            thirty_days_ago = datetime.now() - func.timedelta(days=30)
            recent_care_logs = db.query(CareLog).filter(
                CareLog.crop_id == crop_id,
                CareLog.activity_date >= thirty_days_ago
            ).all()
        
        # Tính điểm thời tiết (0-100)
        weather_score = SHIService._calculate_weather_score(weather_data)
        
        # Tính điểm chăm sóc (0-100)
        care_score = SHIService._calculate_care_score(recent_care_logs)
        
        # SHI = Trung bình có trọng số
        # Thời tiết: 60%, Chăm sóc: 40%
        shi_score = (weather_score * 0.6) + (care_score * 0.4)
        
        # Xác định trạng thái
        if shi_score >= 80:
            status = "excellent"
            status_vn = "Xuất sắc"
        elif shi_score >= 60:
            status = "good"
            status_vn = "Tốt"
        elif shi_score >= 40:
            status = "fair"
            status_vn = "Trung bình"
        else:
            status = "poor"
            status_vn = "Kém"
        
        return {
            "shi_score": round(shi_score, 2),
            "status": status,
            "status_vn": status_vn,
            "weather_score": round(weather_score, 2),
            "care_score": round(care_score, 2),
            "details": {
                "weather": weather_data or {},
                "care_activities_count": len(recent_care_logs) if recent_care_logs else 0
            }
        }
    
    @staticmethod
    def _calculate_weather_score(weather_data: Optional[Dict[str, Any]]) -> float:
        """Tính điểm thời tiết (0-100)"""
        if not weather_data:
            return 50.0  # Điểm mặc định nếu không có dữ liệu
        
        score = 100.0
        
        # Nhiệt độ lý tưởng cho cà phê: 20-30°C
        temp = weather_data.get("temperature", 25)
        if temp < 15 or temp > 35:
            score -= 30
        elif temp < 20 or temp > 30:
            score -= 15
        
        # Độ ẩm lý tưởng: 60-80%
        humidity = weather_data.get("humidity", 70)
        if humidity < 40 or humidity > 90:
            score -= 20
        elif humidity < 50 or humidity > 85:
            score -= 10
        
        # Lượng mưa: quá nhiều hoặc quá ít đều không tốt
        precipitation = weather_data.get("precipitation", 0)
        if precipitation > 50:  # Mưa quá nhiều
            score -= 25
        elif precipitation == 0 and humidity < 50:  # Khô hạn
            score -= 20
        
        return max(0, min(100, score))
    
    @staticmethod
    def _calculate_care_score(care_logs: list) -> float:
        """Tính điểm chăm sóc dựa trên tần suất và chất lượng"""
        if not care_logs:
            return 30.0  # Điểm thấp nếu không có chăm sóc
        
        score = 50.0  # Điểm cơ bản
        
        # Tăng điểm dựa trên số lượng hoạt động
        activity_count = len(care_logs)
        if activity_count >= 10:
            score += 30
        elif activity_count >= 5:
            score += 20
        elif activity_count >= 3:
            score += 10
        
        # Kiểm tra các hoạt động quan trọng
        has_watering = any(log.activity_type == "watering" for log in care_logs)
        has_fertilizing = any(log.activity_type == "fertilizing" for log in care_logs)
        has_pest_control = any(log.activity_type == "pest_control" for log in care_logs)
        
        if has_watering:
            score += 10
        if has_fertilizing:
            score += 10
        if has_pest_control:
            score += 10
        
        return min(100, score)

shi_service = SHIService()

