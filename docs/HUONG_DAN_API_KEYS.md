# HƯỚNG DẪN LẤY API KEYS

## 1. OpenWeatherMap API Key (Thời tiết)

### Bước 1: Đăng ký tài khoản
1. Truy cập: https://openweathermap.org/api
2. Click vào nút **"Sign Up"** hoặc **"Sign In"** nếu đã có tài khoản
3. Điền thông tin đăng ký (Email, Username, Password)
4. Xác nhận email

### Bước 2: Lấy API Key
1. Sau khi đăng nhập, vào trang **Dashboard**: https://home.openweathermap.org/api_keys
2. Bạn sẽ thấy một API key mặc định (hoặc tạo mới)
3. Copy API key này
4. **Lưu ý**: API key miễn phí có giới hạn:
   - 60 calls/phút
   - 1,000,000 calls/tháng
   - Đủ cho dự án demo

### Bước 3: Cấu hình
Thêm vào file `backend/.env`:
```
OPENWEATHER_API_KEY=your_api_key_here
```

---

## 2. Google Gemini API Key (AI Assistant)

### Bước 1: Truy cập Google AI Studio
1. Truy cập: https://makersuite.google.com/app/apikey
   Hoặc: https://aistudio.google.com/app/apikey
2. Đăng nhập bằng tài khoản Google của bạn

### Bước 2: Tạo API Key
1. Click vào nút **"Create API Key"**
2. Chọn project Google Cloud (hoặc tạo mới)
3. API key sẽ được tạo tự động
4. Copy API key này ngay lập tức (chỉ hiển thị 1 lần)

### Bước 3: Cấu hình
Thêm vào file `backend/.env`:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

### Lưu ý:
- Gemini API miễn phí có giới hạn: 15 requests/phút
- Đủ cho demo và testing
- Nếu cần nhiều hơn, có thể nâng cấp

---

## 3. Database PostgreSQL

### Cách 1: Cài đặt PostgreSQL Local

#### Trên macOS:
```bash
# Sử dụng Homebrew
brew install postgresql@14
brew services start postgresql@14

# Tạo database
createdb agrobi_db

# Tạo user (tùy chọn)
createuser -s your_username
```

#### Trên Windows:
1. Tải PostgreSQL từ: https://www.postgresql.org/download/windows/
2. Cài đặt và nhớ password cho user `postgres`
3. Mở pgAdmin hoặc psql
4. Tạo database: `CREATE DATABASE agrobi_db;`

#### Trên Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo -u postgres createdb agrobi_db
```

### Cách 2: Sử dụng Cloud Database (Miễn phí)

#### Option A: Supabase (Khuyến nghị)
1. Truy cập: https://supabase.com
2. Đăng ký tài khoản miễn phí
3. Tạo project mới
4. Vào **Settings > Database**
5. Copy **Connection String** (URI)
6. Format: `postgresql://postgres:[YOUR-PASSWORD]@db.xxx.supabase.co:5432/postgres`

#### Option B: Neon (Khuyến nghị)
1. Truy cập: https://neon.tech
2. Đăng ký tài khoản miễn phí
3. Tạo project mới
4. Copy **Connection String**

### Cấu hình Database URL
Thêm vào file `backend/.env`:
```
DATABASE_URL=postgresql://username:password@localhost:5432/agrobi_db
```

Hoặc nếu dùng Supabase/Neon:
```
DATABASE_URL=postgresql://postgres:password@db.xxx.supabase.co:5432/postgres
```

---

## 4. Tạo file .env

1. Copy file `.env.example` thành `.env`:
```bash
cd backend
cp .env.example .env
```

2. Mở file `.env` và điền các thông tin:
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/agrobi_db

# API Keys
OPENWEATHER_API_KEY=your_openweather_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

# Application
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:5500
```

---

## 5. Kiểm tra API Keys

Sau khi cấu hình, chạy backend và kiểm tra:
```bash
cd backend
python -m app.main
```

Truy cập: http://localhost:8000/docs để xem API documentation.

---

## Tóm tắt các API Keys cần:

| API | URL | Miễn phí? | Giới hạn |
|-----|-----|-----------|----------|
| OpenWeatherMap | https://openweathermap.org/api | ✅ Có | 60 calls/phút |
| Google Gemini | https://aistudio.google.com/app/apikey | ✅ Có | 15 requests/phút |
| PostgreSQL | Local hoặc Supabase/Neon | ✅ Có | Tùy chọn |

---

## Hỗ trợ

Nếu gặp vấn đề, vui lòng kiểm tra:
1. API keys đã được copy đúng chưa (không có khoảng trắng)
2. Database đã được tạo và đang chạy
3. File `.env` nằm trong thư mục `backend/`
4. Đã cài đặt các dependencies: `pip install -r requirements.txt`

