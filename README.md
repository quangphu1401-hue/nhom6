# AgroBI - Hệ Thống Kinh Doanh Thông Minh Nông Nghiệp

## 📋 Giới thiệu

AgroBI là nền tảng hệ thống kinh doanh thông minh được thiết kế đặc biệt cho lĩnh vực nông nghiệp. Hệ thống tích hợp công nghệ AI (Trí tuệ nhân tạo), BI (Business Intelligence) và Tự động hóa dữ liệu để hỗ trợ nông dân và doanh nghiệp nông nghiệp trong:

- Quản lý mùa vụ với Digital Twin
- Dự báo thời tiết và cảnh báo rủi ro
- Nhận diện sâu bệnh bằng AI
- Phân tích dữ liệu lịch sử và trợ lý ảo
- Tính toán chỉ số sức khỏe mùa vụ (SHI)

## 🏗️ Kiến trúc hệ thống

```
┌─────────────┐
│  Frontend   │  (HTML/CSS/JavaScript)
│  (Static)   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Backend   │  (FastAPI - Python)
│   REST API  │
└──────┬──────┘
       │
       ├──► PostgreSQL Database
       ├──► OpenWeatherMap API
       └──► Google Gemini API
```

## 📁 Cấu trúc dự án

```
HTKDTM/
├── assets/              # Frontend assets (CSS, images, fonts)
├── backend/             # Backend FastAPI
│   ├── app/
│   │   ├── api/        # API endpoints
│   │   ├── models/     # Database models
│   │   ├── schemas/    # Pydantic schemas
│   │   ├── services/   # Business logic
│   │   └── database/   # Database configuration
│   ├── .env            # Environment variables (tạo từ .env.example)
│   └── requirements.txt
├── docs/               # Tài liệu
├── index.html          # Frontend chính
└── README.md
```

## 🚀 Hướng dẫn cài đặt

### Yêu cầu hệ thống

- Python 3.9+
- PostgreSQL 12+ (hoặc sử dụng Supabase/Neon cloud)
- Node.js (không bắt buộc, chỉ để chạy frontend)

### Bước 1: Clone repository

```bash
git clone https://github.com/Hoan110504/HTKDTM.git
cd HTKDTM
```

### Bước 2: Cài đặt Backend

```bash
cd backend

# Tạo virtual environment (khuyến nghị)
python -m venv venv
source venv/bin/activate  # Trên Windows: venv\Scripts\activate

# Cài đặt dependencies
pip install -r requirements.txt
```

### Bước 3: Cấu hình Database và API Keys

Xem chi tiết trong file: [docs/HUONG_DAN_API_KEYS.md](docs/HUONG_DAN_API_KEYS.md)

**Tóm tắt:**
1. Lấy OpenWeatherMap API key: https://openweathermap.org/api
2. Lấy Google Gemini API key: https://aistudio.google.com/app/apikey
3. Cài đặt PostgreSQL hoặc dùng Supabase/Neon (miễn phí)
4. Tạo file `backend/.env` từ `backend/.env.example` và điền thông tin

### Bước 4: Khởi tạo Database

```bash
cd backend
python init_db.py
```

### Bước 5: Chạy Backend

```bash
cd backend
python -m app.main
```

Hoặc:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend sẽ chạy tại: http://localhost:8000

API Documentation: http://localhost:8000/docs

### Bước 6: Chạy Frontend

Mở file `index.html` trong trình duyệt hoặc sử dụng local server:

```bash
# Sử dụng Python
python -m http.server 5500

# Hoặc sử dụng Node.js
npx http-server -p 5500
```

Frontend sẽ chạy tại: http://localhost:5500

## 📚 Các tính năng chính

### WP1: Quản lý Mùa Vụ & Digital Twin
- Tạo và quản lý mùa vụ
- Tính toán tự động tuổi cây (age_days)
- Xác định giai đoạn sinh trưởng (seedling, vegetative, flowering, fruiting, mature, harvest)
- Ước tính ngày thu hoạch

**API Endpoints:**
- `POST /api/crops/` - Tạo mùa vụ mới
- `GET /api/crops/` - Lấy danh sách mùa vụ
- `GET /api/crops/{id}` - Lấy chi tiết mùa vụ
- `PUT /api/crops/{id}` - Cập nhật mùa vụ

### WP2: Chỉ số SHI & Phân tích Thời tiết
- Tính toán chỉ số sức khỏe mùa vụ (Season Health Index)
- Tích hợp OpenWeatherMap API
- Dự báo thời tiết 7 ngày
- Cảnh báo rủi ro thời tiết

**API Endpoints:**
- `GET /api/weather/current?lat={lat}&lon={lon}` - Thời tiết hiện tại
- `GET /api/weather/forecast?lat={lat}&lon={lon}&days=7` - Dự báo thời tiết
- `GET /api/analytics/shi/{crop_id}` - Tính SHI cho mùa vụ

### WP3: Nhận diện Sâu bệnh
- Nhận diện sâu bệnh dựa trên mô tả (knowledge-based)
- Sử dụng Google Gemini API
- Đưa ra khuyến nghị xử lý

**API Endpoints:**
- `POST /api/pests/identify` - Nhận diện sâu bệnh
- `GET /api/pests/crop/{crop_id}` - Lịch sử nhận diện

### WP4: Phân tích Lịch sử & Trợ lý ảo
- Lưu trữ dữ liệu nhiều mùa vụ
- Phân tích yếu tố ảnh hưởng đến năng suất
- Trợ lý ảo AI truy vấn và diễn giải dữ liệu
- Trả lời dưới dạng khuyến nghị và giải thích số liệu

**API Endpoints:**
- `POST /api/ai/ask` - Hỏi trợ lý AI
- `GET /api/analytics/season-history/{crop_id}` - Lịch sử mùa vụ

## 🔧 Công nghệ sử dụng

| Thành phần | Công nghệ |
|------------|-----------|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python (FastAPI) |
| Database | PostgreSQL |
| AI | Google Gemini API |
| Weather API | OpenWeatherMap |
| BI Platform | (Tích hợp Superset trong tương lai) |
| Automation | (Tích hợp n8n trong tương lai) |

## 📖 API Documentation

Sau khi chạy backend, truy cập:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🧪 Testing

```bash
# Test API endpoints
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

## 👥 Nhóm thực hiện

- **Nguyễn Năng Đông** (2251161978) - WP1: Quản lý Mùa Vụ & Digital Twin
- **Đặng Thị Thu Thủy** (2251162168) - WP2: SHI & Phân tích Thời tiết
- **Tô Quang Phú** (2251162110) - WP3: Nhận diện Sâu bệnh
- **Nguyễn Ngọc Hoàn** (2251162013) - WP4: Phân tích Lịch sử & Trợ lý ảo

## 📝 License

Dự án này được phát triển cho mục đích học tập và nghiên cứu.

## 🔗 Tài liệu tham khảo

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenWeatherMap API](https://openweathermap.org/api)
- [Google Gemini API](https://ai.google.dev/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## 📞 Liên hệ

- Email: NguyenNgocHoan@gmail.com
- Điện thoại: 0866816201

---

**Lưu ý:** Đây là phiên bản prototype. Các tính năng nâng cao như tích hợp Superset, n8n, và Mobile App sẽ được phát triển trong tương lai.

