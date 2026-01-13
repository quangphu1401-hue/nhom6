# 🚀 HƯỚNG DẪN NHANH - BẮT ĐẦU TRONG 5 PHÚT

## Bước 1: Cài đặt Dependencies

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Bước 2: Lấy API Keys (Miễn phí)

### OpenWeatherMap API:
1. Truy cập: https://openweathermap.org/api
2. Đăng ký tài khoản miễn phí
3. Copy API key từ Dashboard

### Google Gemini API:
1. Truy cập: https://aistudio.google.com/app/apikey
2. Đăng nhập bằng Google
3. Click "Create API Key" và copy

### Database (Chọn 1 trong 2):

**Option A: Supabase (Khuyến nghị - Dễ nhất)**
1. Truy cập: https://supabase.com
2. Đăng ký và tạo project mới
3. Vào Settings > Database > Copy Connection String

**Option B: PostgreSQL Local**
```bash
# macOS
brew install postgresql@14
brew services start postgresql@14
createdb agrobi_db

# Database URL sẽ là:
# postgresql://your_username@localhost:5432/agrobi_db
```

## Bước 3: Cấu hình .env

```bash
cd backend
cp .env.example .env
```

Mở file `.env` và điền:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/agrobi_db
OPENWEATHER_API_KEY=your_openweather_key_here
GEMINI_API_KEY=your_gemini_key_here
SECRET_KEY=your-secret-key-here
DEBUG=True
```

## Bước 4: Khởi tạo Database

```bash
cd backend
python init_db.py
```

## Bước 5: Chạy Backend

```bash
cd backend
python -m app.main
```

Hoặc:
```bash
uvicorn app.main:app --reload
```

Backend chạy tại: http://localhost:8000
API Docs: http://localhost:8000/docs

## Bước 6: Mở Frontend

Mở file `index.html` trong trình duyệt hoặc:

```bash
# Từ thư mục gốc HTKDTM
python -m http.server 5500
```

Truy cập: http://localhost:5500

## ✅ Kiểm tra

1. Mở http://localhost:8000/docs - Xem API documentation
2. Mở http://localhost:5500 - Xem frontend
3. Click nút "🤖" ở góc dưới bên phải để test AI Assistant
4. Click "Cập nhật" ở các card trong Dashboard để test API

## 🐛 Xử lý lỗi thường gặp

### Lỗi: "Connection refused" khi gọi API
→ Backend chưa chạy. Chạy `python -m app.main` trong thư mục backend

### Lỗi: "API key invalid"
→ Kiểm tra lại API keys trong file `.env`

### Lỗi: "Database connection failed"
→ Kiểm tra PostgreSQL đang chạy và DATABASE_URL đúng chưa

### Lỗi: "Module not found"
→ Chạy `pip install -r requirements.txt` trong virtual environment

## 📝 Test API nhanh

```bash
# Test health check
curl http://localhost:8000/health

# Tạo mùa vụ mới
curl -X POST "http://localhost:8000/api/crops/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Cà phê Robusta 2025",
    "crop_type": "coffee_robusta",
    "planting_date": "2025-01-01",
    "area_hectares": 2.5,
    "location": "Đắk Lắk",
    "latitude": 12.6667,
    "longitude": 108.0500
  }'
```

## 🎉 Hoàn thành!

Bây giờ bạn có thể:
- Tạo mùa vụ qua API
- Xem thời tiết và dự báo
- Sử dụng AI Assistant
- Tính toán SHI cho mùa vụ
- Nhận diện sâu bệnh

Xem chi tiết trong [README.md](README.md) và [docs/HUONG_DAN_API_KEYS.md](docs/HUONG_DAN_API_KEYS.md)

