# 📖 HƯỚNG DẪN SETUP DỰ ÁN AGROBI

Hướng dẫn đơn giản để clone và chạy dự án từ đầu.

---

## 🚀 BƯỚC 1: CLONE DỰ ÁN

```bash
git clone https://github.com/quangphu1401-hue/nhom6.git
cd nhom6
```

---

## 🐍 BƯỚC 2: CÀI ĐẶT PYTHON VÀ POSTGRESQL

### Python 3.9+
Kiểm tra Python đã cài:
```bash
python3 --version
```

Nếu chưa có, cài đặt:
- **macOS**: `brew install python3`
- **Windows**: Tải từ https://www.python.org/downloads/
- **Linux**: `sudo apt install python3 python3-pip`

### PostgreSQL
**macOS:**
```bash
brew install postgresql@14
brew services start postgresql@14
createdb agrobi_db
```

**Windows:**
- Tải từ https://www.postgresql.org/download/windows/
- Cài đặt và tạo database `agrobi_db`

**Linux:**
```bash
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo -u postgres createdb agrobi_db
```

---

## 🔑 BƯỚC 3: LẤY API KEYS (MIỄN PHÍ)

### 1. OpenWeatherMap API Key
1. Truy cập: https://openweathermap.org/api
2. Đăng ký tài khoản miễn phí
3. Vào Dashboard → Copy API key

### 2. Google Gemini API Key
1. Truy cập: https://aistudio.google.com/app/apikey
2. Đăng nhập bằng Google
3. Click "Create API Key" → Copy

---

## ⚙️ BƯỚC 4: CẤU HÌNH BACKEND

```bash
cd backend

# Tạo virtual environment (khuyến nghị)
python3 -m venv venv

# Kích hoạt virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Cài đặt dependencies
pip install -r requirements.txt

# Tạo file .env từ .env.example
cp .env.example .env

# Mở file .env và điền thông tin
nano .env  # hoặc dùng editor khác
```

**Nội dung file `.env`:**
```env
DATABASE_URL=postgresql://your_username@localhost:5432/agrobi_db
OPENWEATHER_API_KEY=your_openweather_key_here
GEMINI_API_KEY=your_gemini_key_here
SECRET_KEY=your-secret-key-here
DEBUG=True
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:5500,http://localhost:5500
```

**Lưu ý:** 
- Thay `your_username` bằng username PostgreSQL của bạn
- Nếu PostgreSQL không có password, bỏ phần `:password`
- Điền API keys đã lấy ở Bước 3

---

## 🗄️ BƯỚC 5: KHỞI TẠO DATABASE

```bash
cd backend
python3 init_db.py
```

Bạn sẽ thấy:
```
✅ Đã tạo database thành công!
Các bảng đã được tạo:
- crops (Mùa vụ)
- weather_data (Dữ liệu thời tiết)
- care_logs (Nhật ký chăm sóc)
- pest_identifications (Nhận diện sâu bệnh)
- season_history (Lịch sử mùa vụ)
```

---

## 🎯 BƯỚC 6: CHẠY BACKEND

```bash
cd backend
python3 -m app.main
```

Hoặc:
```bash
uvicorn app.main:app --reload
```

**Backend sẽ chạy tại:** http://localhost:8000

**API Documentation:** http://localhost:8000/docs

**Kiểm tra:** Mở trình duyệt vào http://localhost:8000/health

---

## 🌐 BƯỚC 7: CHẠY FRONTEND

Mở **Terminal mới** (giữ Terminal chạy backend):

```bash
# Từ thư mục gốc của dự án
cd nhom6  # hoặc cd HTKDTM nếu bạn đã đổi tên

# Chạy local server
python3 -m http.server 5500 --bind 127.0.0.1
```

**Frontend sẽ chạy tại:** http://localhost:5500

**Hoặc:** Mở trực tiếp file `index.html` trong trình duyệt

---

## ✅ KIỂM TRA

1. **Backend:** http://localhost:8000/health → Phải hiển thị `{"status":"healthy"}`
2. **API Docs:** http://localhost:8000/docs → Xem tất cả API endpoints
3. **Frontend:** http://localhost:5500 → Xem giao diện web

---

## 🧪 TEST NHANH

### Tạo mùa vụ mới:
1. Mở http://localhost:8000/docs
2. Tìm `POST /api/crops/`
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

### Test AI Assistant:
- Mở frontend → Click nút 🤖 ở góc dưới
- Hỏi: "Tôi nên làm gì để tăng năng suất cà phê?"

---

## 🐛 XỬ LÝ LỖI THƯỜNG GẶP

### Lỗi: "Module not found"
```bash
cd backend
pip install -r requirements.txt
```

### Lỗi: "Database connection failed"
- Kiểm tra PostgreSQL đang chạy:
  ```bash
  # macOS
  brew services list | grep postgresql
  
  # Linux
  sudo systemctl status postgresql
  ```
- Kiểm tra DATABASE_URL trong `.env` đúng chưa
- Kiểm tra database `agrobi_db` đã tạo chưa

### Lỗi: "Port 8000 already in use"
```bash
# Tìm và kill process
lsof -ti:8000 | xargs kill -9
```

### Lỗi: "API key invalid"
- Kiểm tra lại API keys trong file `.env`
- Đảm bảo không có khoảng trắng thừa
- Test API key bằng cách gọi trực tiếp API

### Lỗi: "CORS error" trong frontend
- Đảm bảo backend đang chạy
- Kiểm tra CORS_ORIGINS trong `.env` có chứa URL frontend

---

## 📋 TÓM TẮT CÁC LỆNH

```bash
# 1. Clone
git clone https://github.com/quangphu1401-hue/nhom6.git
cd nhom6

# 2. Setup Backend
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Điền API keys vào .env
python3 init_db.py

# 3. Chạy Backend (Terminal 1)
python3 -m app.main

# 4. Chạy Frontend (Terminal 2)
cd ..  # Về thư mục gốc
python3 -m http.server 5500 --bind 127.0.0.1
```

---

## 📚 TÀI LIỆU THAM KHẢO

- **README.md** - Tổng quan dự án
- **QUICK_START.md** - Hướng dẫn nhanh 5 phút
- **docs/HUONG_DAN_API_KEYS.md** - Chi tiết cách lấy API keys

---

## 💡 LƯU Ý

- **Backend phải chạy trước** khi frontend gọi API
- **Giữ cả 2 Terminal đang chạy** (1 cho backend, 1 cho frontend)
- **API keys là miễn phí** nhưng có giới hạn:
  - OpenWeatherMap: 60 calls/phút
  - Gemini: 15 requests/phút
- **File `.env` không được commit** lên Git (đã có trong .gitignore)

---

## 🎉 HOÀN THÀNH!

Bây giờ bạn có thể:
- ✅ Tạo và quản lý mùa vụ
- ✅ Xem thời tiết và dự báo
- ✅ Sử dụng AI Assistant
- ✅ Upload ảnh để nhận diện côn trùng
- ✅ Tính toán chỉ số SHI

**Chúc bạn thành công!** 🚀

