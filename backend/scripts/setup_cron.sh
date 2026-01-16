#!/bin/bash
# Script setup cron job cho auto_calculate_shi.py

SCRIPT_PATH="$(cd "$(dirname "$0")" && pwd)/auto_calculate_shi.py"
CRON_JOB="0 6 * * * cd $(dirname "$SCRIPT_PATH") && python3 auto_calculate_shi.py >> /var/log/auto_shi.log 2>&1"

echo "🔧 Setting up cron job for auto_calculate_shi.py"
echo ""
echo "Script path: $SCRIPT_PATH"
echo "Cron schedule: 0 6 * * * (Every day at 6:00 AM)"
echo ""

# Kiểm tra script có tồn tại không
if [ ! -f "$SCRIPT_PATH" ]; then
    echo "❌ Error: Script not found at $SCRIPT_PATH"
    exit 1
fi

# Thêm vào crontab
(crontab -l 2>/dev/null | grep -v "auto_calculate_shi.py"; echo "$CRON_JOB") | crontab -

echo "✅ Cron job đã được thêm!"
echo ""
echo "Để xem cron jobs:"
echo "  crontab -l"
echo ""
echo "Để xóa cron job:"
echo "  crontab -e"
echo "  (Xóa dòng chứa auto_calculate_shi.py)"
echo ""
echo "Để test script ngay:"
echo "  python3 $SCRIPT_PATH"

