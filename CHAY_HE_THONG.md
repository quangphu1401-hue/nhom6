# 🚀 HƯỚNG DẪN CHẠY HỆ THỐNG

## BƯỚC 1: Kiểm tra Database đang chạy

```bash
# Kiểm tra PostgreSQL
brew services list | grep postgresql
```

Nếu chưa chạy, khởi động:
```bash
brew services start postgresql@14
```

---

## BƯỚC 2: Chạy Backend

### Mở Terminal 1:

```bash
cd /Users/tophu/HTKDTM/backend
python3 -m app.main
```

Hoặc sử dụng uvicorn (khuyến nghị):
```bash
cd /Users/tophu/HTKDTM/backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Backend sẽ chạy tại:** http://localhost:8000

**API Documentation:** http://localhost:8000/docs

**Kiểm tra:** Mở trình duyệt và vào http://localhost:8000/health

---

## BƯỚC 3: Chạy Frontend

### Mở Terminal 2 (Terminal mới):

```bash
cd /Users/tophu/HTKDTM
python3 -m http.server 5500
```

**Frontend sẽ chạy tại:** http://localhost:5500

**Hoặc:** Mở trực tiếp file `index.html` trong trình duyệt

---

## ✅ KIỂM TRA HỆ THỐNG

### 1. Test Backend:
```bash
curl http://localhost:8000/health
```

Kết quả mong đợi: `{"status":"healthy"}`

### 2. Test API Documentation:
Mở trình duyệt: http://localhost:8000/docs

### 3. Test Frontend:
Mở trình duyệt: http://localhost:5500

### 4. Test AI Assistant:
- Click vào nút 🤖 ở góc dưới bên phải
- Hỏi: "Tôi nên làm gì để tăng năng suất cà phê?"

---

## 🧪 TEST TẠO MÙA VỤ MỚI

### Cách 1: Qua API Documentation
1. Mở http://localhost:8000/docs
2. Tìm endpoint `POST /api/crops/`
3. Click "Try it out"
4. Điền dữ liệu:
```json
{
  "name": "Cà phê Robusta 2025",
  "crop_type": "coffee_robusta",
  "planting_date": "2025-01-01",
  "area_hectares": 2.5,
  "location": "Đắk Lắk",
  "latitude": 12.6667,
  "longitude": 108.0500
}
```
5. Click "Execute"

### Cách 2: Qua Terminal
```bash
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

---

## 📋 TÓM TẮT CÁC LỆNH

### Terminal 1 - Backend:
```bash
cd /Users/tophu/HTKDTM/backend
python3 -m app.main
```

### Terminal 2 - Frontend:
```bash
cd /Users/tophu/HTKDTM
python3 -m http.server 5500
```

---

## 🐛 XỬ LÝ LỖI

### Lỗi: "Module not found"
```bash
cd /Users/tophu/HTKDTM/backend
pip3 install -r requirements.txt
```

### Lỗi: "Database connection failed"
```bash
# Kiểm tra PostgreSQL đang chạy
brew services list | grep postgresql

# Nếu chưa chạy
brew services start postgresql@14
```

### Lỗi: "Port 8000 already in use"
```bash
# Tìm process đang dùng port 8000
lsof -ti:8000

# Kill process
kill -9 $(lsof -ti:8000)
```

### Lỗi: "CORS error" trong frontend
- Đảm bảo backend đang chạy
- Kiểm tra CORS_ORIGINS trong `.env` có chứa URL frontend

---

## 🎯 CÁC TÍNH NĂNG CÓ THỂ TEST

1. ✅ **Tạo mùa vụ** - POST /api/crops/
2. ✅ **Xem thời tiết** - GET /api/weather/current
3. ✅ **Dự báo thời tiết** - GET /api/weather/forecast
4. ✅ **Tính SHI** - GET /api/analytics/shi/{crop_id}
5. ✅ **Nhận diện sâu bệnh** - POST /api/pests/identify
6. ✅ **Hỏi AI Assistant** - POST /api/ai/ask
7. ✅ **Xem dashboard** - Frontend tự động load dữ liệu

---

## 📞 HỖ TRỢ

Nếu gặp vấn đề, kiểm tra:
1. Backend đang chạy ở Terminal 1
2. Frontend đang chạy ở Terminal 2
3. PostgreSQL đang chạy
4. API keys đã được cấu hình trong `.env`

