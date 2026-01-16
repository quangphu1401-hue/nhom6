#!/bin/bash
# Script tự động setup Superset

echo "🚀 BẮT ĐẦU SETUP SUPERSET"
echo "=========================="
echo ""

# Kiểm tra Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker chưa được cài đặt!"
    echo ""
    echo "📦 Cài đặt Docker Desktop cho macOS:"
    echo "   1. Tải Docker Desktop: https://www.docker.com/products/docker-desktop"
    echo "   2. Hoặc cài bằng Homebrew:"
    echo "      brew install --cask docker"
    echo ""
    echo "   Sau khi cài xong, mở Docker Desktop và chạy lại script này."
    exit 1
fi

echo "✅ Docker đã được cài đặt"
docker --version
echo ""

# Kiểm tra Docker đang chạy
if ! docker info &> /dev/null; then
    echo "⚠️  Docker chưa chạy!"
    echo "   Vui lòng mở Docker Desktop và chạy lại script này."
    exit 1
fi

echo "✅ Docker đang chạy"
echo ""

# Kiểm tra docker-compose
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    echo "❌ docker-compose chưa được cài đặt!"
    exit 1
fi

echo "✅ docker-compose đã sẵn sàng"
echo ""

# Di chuyển vào thư mục superset
cd "$(dirname "$0")"

echo "📂 Đang ở thư mục: $(pwd)"
echo ""

# Kiểm tra file docker-compose.yml
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Không tìm thấy docker-compose.yml"
    exit 1
fi

echo "✅ Tìm thấy docker-compose.yml"
echo ""

# Pull image và chạy Superset
echo "📥 Đang tải Superset image (có thể mất vài phút)..."
docker pull apache/superset:latest

echo ""
echo "🚀 Đang khởi động Superset..."
$COMPOSE_CMD up -d

echo ""
echo "⏳ Đợi Superset khởi động (30 giây)..."
sleep 30

# Kiểm tra container đang chạy
if docker ps | grep -q superset; then
    echo ""
    echo "✅ Superset đã khởi động thành công!"
    echo ""
    echo "🌐 Truy cập Superset tại:"
    echo "   http://localhost:8088"
    echo ""
    echo "👤 Thông tin đăng nhập:"
    echo "   Username: admin"
    echo "   Password: admin"
    echo ""
    echo "📊 Bước tiếp theo:"
    echo "   1. Mở http://localhost:8088"
    echo "   2. Đăng nhập với admin/admin"
    echo "   3. Kết nối database PostgreSQL:"
    echo "      Settings → Database Connections → + Database"
    echo "      URI: postgresql://tophu@localhost:5432/agrobi_db"
    echo "   4. Import SQL queries từ thư mục queries/"
    echo ""
    echo "🛑 Để dừng Superset:"
    echo "   cd $(pwd) && $COMPOSE_CMD down"
    echo ""
else
    echo ""
    echo "⚠️  Superset container chưa sẵn sàng. Kiểm tra logs:"
    echo "   $COMPOSE_CMD logs"
    echo ""
fi

