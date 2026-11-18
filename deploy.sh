#!/usr/bin/env bash
# ==============================================================================
# SCRIPT TỰ ĐỘNG DEPLOY TOÀN BỘ HỆ THỐNG TAYNINHINFO.COM
# Target: Firebase Project 'Blogger' & Google Apps Script 'Blogger-Web'
# ==============================================================================

set -e

echo "=========================================================="
echo ">>> [1/4] KIỂM TRA MÔI TRƯỜNG & CÔNG CỤ CLI..."
echo "=========================================================="

# Kiểm tra Node.js & npm
if ! command -v npm &> /dev/null; then
    echo "[LỖI] Node.js và npm chưa được cài đặt. Vui lòng cài đặt trước."
    exit 1
fi

# Cài đặt tự động firebase-tools và clasp nếu chưa có
if ! command -v firebase &> /dev/null; then
    echo ">> Đang cài đặt firebase-tools toàn cục..."
    npm install -g firebase-tools
fi

if ! command -v clasp &> /dev/null; then
    echo ">> Đang cài đặt @google/clasp toàn cục..."
    npm install -g @google/clasp
fi

echo "=========================================================="
echo ">>> [2/4] TRIỂN KHAI FIREBASE RULES (PROJECT: Blogger)..."
echo "=========================================================="

cd firebase

# Kiểm tra đăng nhập Firebase
if ! firebase projects:list &> /dev/null; then
    echo ">> Vui lòng đăng nhập Firebase CLI..."
    firebase login
fi

# Liên kết với Project ID: fir-1b417
echo ">> Chọn Firebase Project: fir-1b417..."
firebase use fir-1b417 2>/dev/null || firebase use --add fir-1b417

# Đẩy Firestore Rules, Realtime Database Rules và Hosting
echo ">> Triển khai Security Rules & Hosting (Tây Ninh Go) lên Firebase Cloud..."
firebase deploy --only firestore:rules,database,hosting

cd ..

echo "=========================================================="
echo ">>> [3/4] TRIỂN KHAI GOOGLE APPS SCRIPT (Blogger-Web)..."
echo "=========================================================="

cd gas

# Kiểm tra đăng nhập Google Clasp
if [ ! -f ~/.clasprc.json ]; then
    echo ">> Vui lòng đăng nhập tài khoản Google cho Clasp CLI..."
    clasp login
fi

# Khởi tạo file cấu hình clasp nếu chưa có
if [ ! -f .clasp.json ]; then
    echo ">> Nhập Script ID của Google Apps Script 'Blogger-Web' (hoặc nhấn Enter để tự tạo mới):"
    read -r SCRIPT_ID
    if [ -z "$SCRIPT_ID" ]; then
        echo ">> Đang tạo Google Apps Script Project mới tên 'Blogger-Web'..."
        clasp create --title "Blogger-Web" --type webapp --rootDir .
    else
        cat <<EOF > .clasp.json
{
  "scriptId": "$SCRIPT_ID",
  "rootDir": "."
}
EOF
    fi
fi

# Đẩy toàn bộ code Code.gs và appsscript.json lên Google Cloud
echo ">> Đang đẩy mã nguồn Code.gs lên Google Apps Script..."
clasp push --force

# Triển khai phiên bản Web App mới nhất
echo ">> Đang phát hành phiên bản Web App công khai..."
DEPLOY_OUTPUT=$(clasp deploy --description "Production Release $(date +'%Y-%m-%d %H:%M:%S')")
echo "$DEPLOY_OUTPUT"

cd ..

echo "=========================================================="
echo ">>> [4/4] HOÀN TẤT TRIỂN KHAI THÀNH CÔNG!"
echo "=========================================================="
echo "1. File Blogger Theme: theme.xml đã sẵn sàng."
echo "   -> Mở Blogger.com -> Chủ đề (Theme) -> Chỉnh sửa HTML -> Dán nội dung theme.xml."
echo "2. Firebase Rules: Đã cập nhật trên dự án 'Blogger'."
echo "3. Google Apps Script: Đã cập nhật và phát hành Web App."
echo "=========================================================="
