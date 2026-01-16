# 🚀 QUICK START - SETUP SUPERSET

## Bước 1: Cài đặt Docker Desktop

### Nếu chưa có Docker:

**Option 1: Tải thủ công (Khuyến nghị)**
1. Truy cập: https://www.docker.com/products/docker-desktop
2. Tải Docker Desktop cho macOS
3. Mở file `.dmg` và kéo Docker vào Applications
4. Mở Docker Desktop từ Applications
5. Chờ Docker khởi động (icon Docker xuất hiện trên menu bar)

**Option 2: Cài bằng Homebrew (Cần password)**
```bash
brew install --cask docker
# Sau đó mở Docker Desktop từ Applications
```

---

## Bước 2: Chạy Superset

### Cách 1: Dùng script tự động (Khuyến nghị)

```bash
cd superset
./SETUP_SUPERSET.sh
```

### Cách 2: Chạy thủ công

```bash
cd superset
docker-compose up -d
```

**Đợi 30-60 giây** để Superset khởi động hoàn toàn.

---

## Bước 3: Truy cập Superset

1. Mở trình duyệt: **http://localhost:8088**

2. **Đăng nhập:**
   - Username: `admin`
   - Password: `admin`

---

## Bước 4: Kết nối Database

1. Vào **Settings** → **Database Connections** → **+ Database**

2. **Cấu hình:**
   - **Display Name:** `AgroBI PostgreSQL`
   - **SQLAlchemy URI:** `postgresql://tophu@host.docker.internal:5432/agrobi_db`
   - **Test Connection** → **Save**

   **Lưu ý:** Dùng `host.docker.internal` thay vì `localhost` để Docker container có thể kết nối PostgreSQL trên máy host.

---

## Bước 5: Import SQL Queries

1. Vào **SQL Lab** → **SQL Editor**

2. Copy nội dung từ các file trong `superset/queries/`:
   - `shi_daily_trends.sql`
   - `crop_performance.sql`
   - `weather_impact.sql`
   - `yield_factors.sql`

3. Chạy query và **Save as Dataset**

---

## Bước 6: Tạo Dashboards

Theo hướng dẫn trong `HUONG_DAN_SETUP_SUPERSET.md` phần 4.

---

## Troubleshooting

### Docker không chạy:
```bash
# Mở Docker Desktop từ Applications
# Hoặc kiểm tra:
docker info
```

### Lỗi kết nối database:
- Đảm bảo PostgreSQL đang chạy: `pg_isready`
- Dùng `host.docker.internal` thay vì `localhost` trong SQLAlchemy URI
- Kiểm tra firewall

### Superset không khởi động:
```bash
# Xem logs:
cd superset
docker-compose logs

# Restart:
docker-compose restart
```

### Dừng Superset:
```bash
cd superset
docker-compose down
```

---

## ✅ Hoàn thành!

Sau khi setup xong, bạn có thể:
- Tạo dashboards để visualize SHI, crop performance, weather impact
- Export reports
- Embed charts vào frontend

