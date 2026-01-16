"""
Script khởi tạo database và tạo các bảng
Chạy: python init_db.py
"""
from app.database.database import engine, Base
from app.models import crop_model, weather_model, care_log_model, pest_model, season_history_model, season_model, shi_daily_model

def init_database():
    """Tạo tất cả các bảng trong database"""
    print("Đang tạo các bảng trong database...")
    Base.metadata.create_all(bind=engine)
    print("✅ Đã tạo database thành công!")
    print("\nCác bảng đã được tạo:")
    print("- crops (Mùa vụ)")
    print("- season (Mùa vụ - theo PDF)")
    print("- weather_data (Dữ liệu thời tiết)")
    print("- care_logs (Nhật ký chăm sóc)")
    print("- pest_identifications (Nhận diện sâu bệnh)")
    print("- season_history (Lịch sử mùa vụ)")
    print("- shi_daily (SHI theo ngày - Data Warehouse)")

if __name__ == "__main__":
    init_database()

