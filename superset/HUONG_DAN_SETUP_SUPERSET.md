# 📊 HƯỚNG DẪN SETUP APACHE SUPERSET

## 1. Cài đặt Superset

### Option 1: Docker (Khuyến nghị)

**Cách 1: Dùng script tự động (Khuyến nghị)**

```bash
cd superset
./SETUP_SUPERSET.sh
```

Script sẽ tự động:
- Kiểm tra Docker đã cài chưa
- Tải Superset image
- Khởi động Superset
- Tạo admin user (admin/admin)

**Cách 2: Chạy thủ công**

```bash
cd superset

# Chạy với Docker Compose
docker-compose up -d
# hoặc (nếu dùng Docker Compose v2)
docker compose up -d
```

**Lưu ý:** Nếu chưa có Docker, cài đặt Docker Desktop:
- Tải từ: https://www.docker.com/products/docker-desktop
- Hoặc: `brew install --cask docker` (nếu có Homebrew)

### Option 2: Python Virtual Environment

```bash
# Tạo virtual environment
python3 -m venv venv
source venv/bin/activate  # Trên macOS/Linux
# hoặc: venv\Scripts\activate  # Trên Windows

# Cài đặt Superset
pip install apache-superset

# Khởi tạo database
superset db upgrade

# Tạo admin user
export FLASK_APP=superset
superset fab create-admin \
  --username admin \
  --firstname Admin \
  --lastname User \
  --email admin@example.com \
  --password admin

# Load examples (optional)
superset load_examples

# Khởi động Superset
superset run -p 8088 --with-threads --reload --debugger
```

Truy cập: http://localhost:8088

---

## 2. Kết nối Database PostgreSQL

1. **Vào Superset UI** → **Settings** → **Database Connections** → **+ Database**

2. **Cấu hình:**
   - **Display Name:** `AgroBI PostgreSQL`
   - **SQLAlchemy URI:** `postgresql://tophu@localhost:5432/agrobi_db`
   - **Test Connection** → **Save**

---

## 3. Import SQL Queries

Sử dụng các SQL queries trong thư mục `superset/queries/` để tạo datasets:

### 3.1. Dataset: SHI Daily Trends
- **SQL:** `superset/queries/shi_daily_trends.sql`
- **Table Name:** `shi_daily_trends`

### 3.2. Dataset: Crop Performance
- **SQL:** `superset/queries/crop_performance.sql`
- **Table Name:** `crop_performance`

### 3.3. Dataset: Weather Impact Analysis
- **SQL:** `superset/queries/weather_impact.sql`
- **Table Name:** `weather_impact`

### 3.4. Dataset: Yield Factors
- **SQL:** `superset/queries/yield_factors.sql`
- **Table Name:** `yield_factors`

---

## 4. Tạo Dashboards

### Dashboard 1: SHI Monitoring Dashboard

**Charts:**
1. **SHI Score Over Time** (Line Chart)
   - Dataset: `shi_daily_trends`
   - X-axis: `date`
   - Y-axis: `shi_score`
   - Series: `crop_name`

2. **SHI Components** (Stacked Area Chart)
   - Dataset: `shi_daily_trends`
   - X-axis: `date`
   - Y-axis: `weather_score`, `care_score`, `growth_score`

3. **SHI Status Distribution** (Pie Chart)
   - Dataset: `shi_daily_trends`
   - Group by: `status_vn`

4. **Warnings by Level** (Bar Chart)
   - Dataset: `shi_daily_trends`
   - X-axis: `warning_level`
   - Y-axis: Count

### Dashboard 2: Crop Performance Dashboard

**Charts:**
1. **Yield vs SHI** (Scatter Plot)
   - Dataset: `crop_performance`
   - X-axis: `avg_shi_score`
   - Y-axis: `yield_per_hectare`

2. **Cost vs Profit** (Bar Chart)
   - Dataset: `crop_performance`
   - X-axis: `season_name`
   - Y-axis: `total_cost`, `total_revenue`

3. **Profit Margin** (Line Chart)
   - Dataset: `crop_performance`
   - X-axis: `season_name`
   - Y-axis: `profit_margin`

### Dashboard 3: Weather Impact Dashboard

**Charts:**
1. **Temperature vs SHI** (Line Chart)
   - Dataset: `weather_impact`
   - X-axis: `date`
   - Y-axis: `temperature`, `shi_score`

2. **Precipitation Impact** (Bar Chart)
   - Dataset: `weather_impact`
   - X-axis: `date`
   - Y-axis: `precipitation`, `shi_score`

---

## 5. Tự động hóa với n8n (Optional)

Có thể tích hợp Superset với n8n để:
- Tự động refresh dashboards
- Gửi alerts khi SHI thấp
- Export reports định kỳ

---

## 6. API Integration

Superset có REST API để:
- Tạo dashboards tự động
- Embed charts vào frontend
- Export data

**Example:**
```python
import requests

# Get dashboard
response = requests.get(
    "http://localhost:8088/api/v1/dashboard/1",
    headers={"Authorization": "Bearer YOUR_TOKEN"}
)
```

---

## 7. Troubleshooting

### Lỗi kết nối database:
- Kiểm tra PostgreSQL đang chạy: `pg_isready`
- Kiểm tra credentials trong SQLAlchemy URI
- Kiểm tra firewall/network

### Lỗi import queries:
- Đảm bảo database đã có dữ liệu
- Kiểm tra table names trong queries
- Test queries trực tiếp trong Superset SQL Lab

---

## 8. Best Practices

1. **Tạo datasets từ SQL queries** thay vì trực tiếp từ tables
2. **Cache datasets** để tăng performance
3. **Sử dụng filters** để tối ưu queries
4. **Schedule refresh** cho datasets quan trọng
5. **Export dashboards** để backup

---

## 9. Resources

- [Superset Documentation](https://superset.apache.org/docs/)
- [SQL Lab Guide](https://superset.apache.org/docs/using-sql-lab)
- [Dashboard Guide](https://superset.apache.org/docs/creating-charts-dashboards)

