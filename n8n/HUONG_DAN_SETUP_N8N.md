# 🔄 HƯỚNG DẪN SETUP N8N

## 1. Cài đặt n8n

### Option 1: Docker (Khuyến nghị)

```bash
# Chạy n8n với Docker
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

Truy cập: http://localhost:5678

### Option 2: npm

```bash
# Cài đặt n8n globally
npm install n8n -g

# Chạy n8n
n8n start
```

### Option 3: npx (Quick test)

```bash
npx n8n
```

---

## 2. Import Workflows

### 2.1. Auto Calculate SHI Daily

1. **Vào n8n UI** → **Workflows** → **Import from File**
2. **Chọn file:** `n8n/workflows/auto-calculate-shi.json`
3. **Cấu hình Environment Variables:**
   - `BACKEND_URL`: `http://localhost:8000` (hoặc URL backend của bạn)
   - `WEBHOOK_URL`: (Optional) Slack/Email webhook để nhận alerts

4. **Kích hoạt workflow:**
   - Click **Active** toggle
   - Workflow sẽ chạy tự động mỗi ngày lúc 6:00 AM

### 2.2. Collect Weather Data Hourly

1. **Import file:** `n8n/workflows/collect-weather-data.json`
2. **Cấu hình:** `BACKEND_URL`
3. **Kích hoạt:** Workflow sẽ chạy mỗi giờ

---

## 3. Cấu hình Environment Variables

### Tạo file `.env` trong n8n:

```bash
# Backend API URL
BACKEND_URL=http://localhost:8000

# Optional: Slack Webhook
WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# Optional: Email SMTP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-password
```

### Load env trong Docker:

```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  --env-file .env \
  n8nio/n8n
```

---

## 4. Test Workflows

### Test Auto Calculate SHI:

1. **Manual Trigger:**
   - Click **Execute Workflow** button
   - Xem kết quả trong **Execution Log**

2. **Kiểm tra kết quả:**
   - Vào backend API: `GET /api/analytics/shi-daily/{crop_id}`
   - Kiểm tra database: `SELECT * FROM shi_daily WHERE date = CURRENT_DATE;`

### Test Weather Collection:

1. **Manual Trigger** workflow
2. **Kiểm tra:** `GET /api/weather/` hoặc database `weather_data`

---

## 5. Tùy chỉnh Workflows

### Thêm Email Alert:

1. Thêm node **Email** sau node **Check SHI < 50**
2. Cấu hình SMTP credentials
3. Gửi email khi SHI thấp

### Thêm Slack Notification:

1. Thêm node **Slack** 
2. Cấu hình Slack webhook URL
3. Gửi message khi có cảnh báo

### Thêm Database Logging:

1. Thêm node **PostgreSQL**
2. Lưu execution logs vào database
3. Track workflow performance

---

## 6. Schedule & Automation

### Cron Expression Examples:

- **Mỗi ngày 6:00 AM:** `0 6 * * *`
- **Mỗi giờ:** `0 * * * *`
- **Mỗi 30 phút:** `*/30 * * * *`
- **Mỗi ngày 2 lần (6AM và 6PM):** `0 6,18 * * *`
- **Chỉ thứ 2-6:** `0 6 * * 1-5`

### Timezone:

- Mặc định: UTC
- Đổi timezone: Settings → Timezone → Asia/Ho_Chi_Minh

---

## 7. Monitoring & Debugging

### Execution History:

- Vào **Executions** tab
- Xem lịch sử chạy workflows
- Debug errors trong execution logs

### Error Handling:

- Thêm **Error Trigger** node
- Gửi alerts khi workflow fail
- Retry failed executions

---

## 8. Alternative: Cron Job Script

Nếu không muốn dùng n8n, có thể dùng script Python:

```bash
# Thêm vào crontab
crontab -e

# Thêm dòng này (chạy mỗi ngày 6:00 AM)
0 6 * * * /path/to/backend/scripts/auto_calculate_shi.py >> /var/log/auto_shi.log 2>&1
```

Script: `backend/scripts/auto_calculate_shi.py`

---

## 9. Best Practices

1. **Test workflows** trước khi activate
2. **Monitor executions** thường xuyên
3. **Set up alerts** cho failed executions
4. **Backup workflows** định kỳ
5. **Use environment variables** cho sensitive data
6. **Log important data** để debug

---

## 10. Troubleshooting

### Workflow không chạy:
- Kiểm tra **Active** toggle
- Kiểm tra cron expression
- Kiểm tra execution logs

### API calls fail:
- Kiểm tra `BACKEND_URL` đúng chưa
- Kiểm tra backend đang chạy
- Kiểm tra CORS settings

### Database errors:
- Kiểm tra database connection
- Kiểm tra table exists
- Kiểm tra permissions

---

## 11. Resources

- [n8n Documentation](https://docs.n8n.io/)
- [n8n Workflows](https://n8n.io/workflows/)
- [Cron Expression Guide](https://crontab.guru/)

