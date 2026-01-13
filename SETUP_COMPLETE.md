# ✅ SETUP HOÀN TẤT!

## Đã cấu hình thành công:

### 1. ✅ API Keys
- **OpenWeatherMap API Key**: `50de83e453e430b74813ebe3e9b2b8bf` ✅
- **Google Gemini API Key**: `AIzaSyD4gxMO1MMuev1Ckvxq0LmDbB3lUscZSvU` ✅
- Đã lưu vào file: `backend/.env`

### 2. ✅ PostgreSQL Database
- **Đã cài đặt**: PostgreSQL 14
- **Đã khởi động**: Service đang chạy
- **Database**: `agrobi_db` đã được tạo
- **Connection**: `postgresql://tophu@localhost:5432/agrobi_db`

### 3. ✅ Database Tables
Các bảng đã được tạo thành công:
- ✅ `crops` - Quản lý mùa vụ
- ✅ `weather_data` - Dữ liệu thời tiết
- ✅ `care_logs` - Nhật ký chăm sóc
- ✅ `pest_identifications` - Nhận diện sâu bệnh
- ✅ `season_history` - Lịch sử mùa vụ

### 4. ✅ Dependencies
- Tất cả Python packages đã được cài đặt

---

## 🚀 BƯỚC TIẾP THEO - CHẠY ỨNG DỤNG

### Chạy Backend:

```bash
cd /Users/tophu/HTKDTM/backend
python3 -m app.main
```

Hoặc:
```bash
cd /Users/tophu/HTKDTM/backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend sẽ chạy tại: **http://localhost:8000**
API Documentation: **http://localhost:8000/docs**

### Chạy Frontend:

Mở file `index.html` trong trình duyệt hoặc:

```bash
cd /Users/tophu/HTKDTM
python3 -m http.server 5500
```

Frontend sẽ chạy tại: **http://localhost:5500**

---

## 🧪 TEST NHANH

### 1. Test Health Check:
```bash
curl http://localhost:8000/health
```

### 2. Test API Documentation:
Mở trình duyệt: http://localhost:8000/docs

### 3. Tạo mùa vụ mới:
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

### 4. Test Thời tiết:
```bash
curl "http://localhost:8000/api/weather/current?lat=21.0285&lon=105.8542"
```

### 5. Test AI Assistant:
Mở frontend, click vào nút 🤖 ở góc dưới bên phải và hỏi:
- "Tôi nên làm gì để tăng năng suất cà phê?"
- "Cách phòng trừ sâu bệnh cho cà phê Robusta?"

---

## 📋 KIỂM TRA

### Kiểm tra PostgreSQL đang chạy:
```bash
brew services list | grep postgresql
```

### Kiểm tra database:
```bash
/usr/local/opt/postgresql@14/bin/psql -d agrobi_db -c "\dt"
```

### Kiểm tra API Keys trong .env:
```bash
cd /Users/tophu/HTKDTM/backend
cat .env | grep -E "(OPENWEATHER|GEMINI)"
```

---

## 🎉 SẴN SÀNG SỬ DỤNG!

Bây giờ bạn có thể:
1. ✅ Chạy backend và frontend
2. ✅ Tạo mùa vụ qua API
3. ✅ Xem thời tiết và dự báo
4. ✅ Sử dụng AI Assistant
5. ✅ Tính toán SHI cho mùa vụ
6. ✅ Nhận diện sâu bệnh

Xem chi tiết trong [README.md](README.md) và [QUICK_START.md](QUICK_START.md)

---

**Lưu ý**: 
- PostgreSQL service sẽ tự động khởi động khi đăng nhập (đã cấu hình với brew services)
- Nếu cần dừng PostgreSQL: `brew services stop postgresql@14`
- Nếu cần khởi động lại: `brew services restart postgresql@14`

