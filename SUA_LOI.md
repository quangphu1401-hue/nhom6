# 🔧 SỬA LỖI: "[::]:5500" - Địa chỉ không hợp lệ

## ❌ Vấn đề:
Safari không thể mở trang `[::]:5500` vì đây là địa chỉ IPv6, không hợp lệ.

## ✅ Giải pháp:

### Cách 1: Chạy server với đúng địa chỉ localhost

```bash
cd /Users/tophu/HTKDTM
python3 -m http.server 5500 --bind 127.0.0.1
```

**Lưu ý:** Phải thêm `--bind 127.0.0.1` để bind với localhost thay vì IPv6

### Cách 2: Sử dụng script có sẵn

```bash
cd /Users/tophu/HTKDTM
./start_frontend.sh
```

### Cách 3: Mở trực tiếp file HTML

Đơn giản nhất là mở trực tiếp file `index.html` trong trình duyệt:
- Tìm file: `/Users/tophu/HTKDTM/index.html`
- Double-click để mở trong Safari
- Hoặc kéo thả vào Safari

---

## 🚀 CHẠY LẠI HỆ THỐNG ĐÚNG CÁCH

### Terminal 1 - Backend:
```bash
cd /Users/tophu/HTKDTM/backend
python3 -m app.main
```

### Terminal 2 - Frontend (QUAN TRỌNG: Phải có --bind):
```bash
cd /Users/tophu/HTKDTM
python3 -m http.server 5500 --bind 127.0.0.1
```

Sau đó mở trình duyệt: **http://localhost:5500**

---

## ✅ Kiểm tra:

1. Server đang chạy:
```bash
lsof -ti:5500
```

2. Test trong trình duyệt:
- Mở: http://localhost:5500
- Hoặc: http://127.0.0.1:5500

---

## 💡 Lưu ý:

- **KHÔNG** dùng `[::]:5500` - đây là IPv6
- **DÙNG** `localhost:5500` hoặc `127.0.0.1:5500` - đây là IPv4
- Luôn thêm `--bind 127.0.0.1` khi chạy `python3 -m http.server`

