#!/bin/bash
# Script chạy Backend server

cd /Users/tophu/HTKDTM/backend
echo "🚀 Đang khởi động Backend server..."
echo "📍 URL: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "📁 Thư mục: $(pwd)"
echo ""
echo "Nhấn Ctrl+C để dừng server"
echo ""

python3 -m app.main

