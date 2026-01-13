#!/bin/bash
# Script để fix lỗi "Address already in use"

echo "🔍 Đang kiểm tra port 5500..."

# Tìm process đang dùng port 5500
PID=$(lsof -ti:5500 2>/dev/null)

if [ -z "$PID" ]; then
    echo "✅ Port 5500 đang trống"
else
    echo "⚠️  Tìm thấy process $PID đang dùng port 5500"
    echo "🛑 Đang dừng process..."
    kill -9 $PID 2>/dev/null
    sleep 1
    echo "✅ Đã dừng process"
fi

echo ""
echo "🚀 Bây giờ bạn có thể chạy:"
echo "   python3 -m http.server 5500 --bind 127.0.0.1"

