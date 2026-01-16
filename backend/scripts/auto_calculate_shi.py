#!/usr/bin/env python3
"""
Script tự động tính SHI cho tất cả crops (Thay thế n8n)
Chạy bằng cron job: 0 6 * * * /path/to/auto_calculate_shi.py
"""

import sys
import os
from datetime import date

# Thêm backend vào path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database.database import SessionLocal, engine
from app.models.crop_model import Crop
from app.services.shi_service import shi_service
from app.services.weather_service import weather_service
from app.models.shi_daily_model import SHIDaily
import requests
import json

# URL backend (có thể config qua env)
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

def calculate_shi_for_all_crops():
    """Tính SHI cho tất cả crops và lưu vào shi_daily"""
    db: Session = SessionLocal()
    
    try:
        # Lấy tất cả crops (không có field status, lấy tất cả)
        crops = db.query(Crop).all()
        
        print(f"Tìm thấy {len(crops)} mùa vụ cần tính SHI...")
        
        results = []
        
        for crop in crops:
            try:
                # Lấy thời tiết hiện tại (từ database hoặc API)
                weather_data = None
                if crop.latitude and crop.longitude:
                    try:
                        # Thử lấy từ database trước
                        from app.models.weather_model import WeatherData
                        latest_weather = db.query(WeatherData).filter(
                            WeatherData.crop_id == crop.id,
                            WeatherData.is_forecast == 0
                        ).order_by(WeatherData.recorded_at.desc()).first()
                        
                        if latest_weather:
                            weather_data = {
                                "temperature": latest_weather.temperature,
                                "humidity": latest_weather.humidity,
                                "precipitation": latest_weather.precipitation or 0
                            }
                    except Exception as e:
                        print(f"  ⚠️  Lỗi lấy thời tiết cho crop {crop.id}: {e}")
                
                # Tính SHI
                shi_result = shi_service.calculate_shi(db, crop.id, weather_data)
                
                # Xác định warning level
                warning_level = None
                warning_message = None
                if shi_result["warnings"]:
                    high_warnings = [w for w in shi_result["warnings"] if w.get("level") == "high"]
                    if high_warnings:
                        warning_level = "high"
                        warning_message = "; ".join([w["message"] for w in high_warnings])
                    else:
                        warning_level = "medium"
                        warning_message = "; ".join([w["message"] for w in shi_result["warnings"]])
                
                # Lưu vào shi_daily
                season_id = crop.id  # Tạm thời dùng crop_id
                recorded_date = date.today()
                
                # Kiểm tra xem đã có record cho ngày này chưa
                existing = db.query(SHIDaily).filter(
                    SHIDaily.season_id == season_id,
                    SHIDaily.date == recorded_date
                ).first()
                
                if existing:
                    existing.shi_score = shi_result["shi_score"]
                    existing.weather_score = shi_result["weather_score"]
                    existing.care_score = shi_result["care_score"]
                    existing.growth_score = shi_result["growth_score"]
                    existing.warning_level = warning_level
                    existing.warning_message = warning_message
                else:
                    shi_daily = SHIDaily(
                        season_id=season_id,
                        date=recorded_date,
                        shi_score=shi_result["shi_score"],
                        weather_score=shi_result["weather_score"],
                        care_score=shi_result["care_score"],
                        growth_score=shi_result["growth_score"],
                        warning_level=warning_level,
                        warning_message=warning_message
                    )
                    db.add(shi_daily)
                
                results.append({
                    "crop_id": crop.id,
                    "crop_name": crop.name,
                    "shi_score": shi_result["shi_score"],
                    "status": shi_result["status_vn"],
                    "warnings": len(shi_result["warnings"])
                })
                
                print(f"  ✅ Crop {crop.id} ({crop.name}): SHI = {shi_result['shi_score']:.1f} ({shi_result['status_vn']})")
                
            except Exception as e:
                print(f"  ❌ Lỗi tính SHI cho crop {crop.id}: {e}")
                continue
        
        db.commit()
        
        # Tổng kết
        print(f"\n✅ Hoàn thành! Đã tính SHI cho {len(results)} mùa vụ")
        print(f"   - SHI trung bình: {sum(r['shi_score'] for r in results) / len(results):.1f}" if results else "")
        print(f"   - Có cảnh báo: {sum(1 for r in results if r['warnings'] > 0)} mùa vụ")
        
        # Gửi alert nếu có SHI thấp (optional - có thể tích hợp Slack/Email)
        low_shi_crops = [r for r in results if r["shi_score"] < 50]
        if low_shi_crops:
            print(f"\n⚠️  CẢNH BÁO: {len(low_shi_crops)} mùa vụ có SHI < 50:")
            for r in low_shi_crops:
                print(f"   - {r['crop_name']}: SHI = {r['shi_score']:.1f}")
        
        return results
        
    except Exception as e:
        db.rollback()
        print(f"❌ Lỗi: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 BẮT ĐẦU TÍNH SHI TỰ ĐỘNG")
    print("=" * 60)
    print(f"Thời gian: {date.today()}\n")
    
    try:
        calculate_shi_for_all_crops()
        print("\n✅ Thành công!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        sys.exit(1)

