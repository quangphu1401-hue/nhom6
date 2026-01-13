#!/bin/bash
# Script chạy Frontend server với đúng địa chỉ localhost

cd /Users/tophu/HTKDTM
echo "🚀 Đang khởi động Frontend server..."
echo "📍 URL: http://localhost:5500"
echo "📁 Thư mục: $(pwd)"
echo ""
echo "Nhấn Ctrl+C để dừng server"
echo ""

# Chạy server với localhost thay vì [::]
python3 -m http.server 5500 --bind 127.0.0.1

