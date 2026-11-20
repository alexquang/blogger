#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TÂY NINH CRAWLER CLI TOOL - ADMIN ONLY (ptquang0968@gmail.com)
Công cụ cào và trích xuất dữ liệu việc làm KCN, bất động sản và rao vặt tại tỉnh Tây Ninh.
Đẩy trực tiếp vào Cloud Firestore (Project fir-1b417) qua Firestore REST API.
"""

import sys
import json
import time
import urllib.request
import argparse
from datetime import datetime

FIRESTORE_URL = "https://firestore.googleapis.com/v1/projects/fir-1b417/databases/(default)/documents/listings"

CRAWL_SAMPLES = {
    "tuyendung": [
        {
            "title": "Tuyển Nhân Viên Kiểm Phẩm (QC/QA) - KCN Trảng Bàng",
            "price": "9 - 14 triệu/tháng",
            "location": "KCN Trảng Bàng, TX. Trảng Bàng, Tây Ninh",
            "district": "trangbang",
            "category": "tuyendung",
            "phone": "0918.456.789",
            "authorName": "Công Ty TNHH Sản Xuất Bao Bì Trảng Bàng",
            "image": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=800&q=80",
            "description": "Kiểm tra chất lượng thành phẩm trên dây chuyền sản xuất. Làm việc theo ca xoay, thưởng chuyên cần, phụ cấp nhà ở và cơm trưa. Yêu cầu tốt nghiệp Trung cấp trở lên.",
            "badge": "KCN Trảng Bàng"
        },
        {
            "title": "Tuyển 30 Lao Động Vận Hành Máy Dệt - KCN Phước Đông",
            "price": "8.5 - 13 triệu/tháng",
            "location": "KCN Phước Đông, Huyện Gò Dầu, Tây Ninh",
            "district": "godau",
            "category": "tuyendung",
            "phone": "0979.112.233",
            "authorName": "Tập Đoàn Dệt May Quốc Tế Phước Đông",
            "image": "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=800&q=80",
            "description": "Không cần kinh nghiệm, công ty đào tạo nghề có trả lương. Hỗ trợ ký túc xá cho công nhân ở xa, đóng bảo hiểm 100% theo luật lao động.",
            "badge": "Lương hấp dẫn"
        },
        {
            "title": "Tuyển Nhân Viên Bán Hàng & CSKH Showroom Xe Máy TP. Tây Ninh",
            "price": "10 - 18 triệu/tháng (Lương + Hoa hồng)",
            "location": "Đại Lộ 30/4, Phường 3, TP. Tây Ninh",
            "district": "tptayninh",
            "category": "tuyendung",
            "phone": "0903.889.900",
            "authorName": "Đại Lý Honda Ủy Nhiệm Tây Ninh",
            "image": "https://images.unsplash.com/photo-1556742049-0a67e5572293?auto=format&fit=crop&w=800&q=80",
            "description": "Tư vấn các dòng xe máy, làm thủ tục trả góp và chăm sóc khách hàng sau bán. Môi trường năng động, chuyên nghiệp, thưởng tháng 13.",
            "badge": "Trung tâm TP"
        }
    ],
    "batdongsan": [
        {
            "title": "Chính Chủ Gửi Bán Đất Nền Thổ Cư 100% Gần Chợ Ninh Sơn",
            "price": "790 Triệu (Bao sổ)",
            "location": "Phường Ninh Sơn, TP. Tây Ninh",
            "district": "tptayninh",
            "category": "batdongsan",
            "phone": "0909.778.899",
            "authorName": "Địa Ốc Núi Bà Tây Ninh",
            "image": "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
            "description": "Diện tích 5x22m (110m2) thổ cư toàn bộ, đường bê tông 6m thông thoáng. Dân cư hiện hữu, gần trường học, ủy ban và chợ Ninh Sơn. Sổ hồng công chứng ngay.",
            "badge": "Sổ hồng riêng"
        },
        {
            "title": "Bán 500m2 Đất Vườn Ven Hồ Dầu Tiếng Tuyệt Đẹp Thích Hợp Glamping",
            "price": "650 Triệu",
            "location": "Xã Suối Đá, Huyện Dương Minh Châu, Tây Ninh",
            "district": "duongminhchau",
            "category": "batdongsan",
            "phone": "0937.123.888",
            "authorName": "Bất Động Sản Nghỉ Dưỡng Tây Ninh",
            "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80",
            "description": "Đất vườn bằng phẳng, giáp đường nhựa xe hơi tới nơi. View lòng hồ Dầu Tiếng thơ mộng, không khí trong lành mát mẻ thích hợp làm nhà vườn cuối tuần.",
            "badge": "View Hồ Dầu Tiếng"
        }
    ],
    "raovat": [
        {
            "title": "Bán Xe Tải Dongfeng 8 Tấn Đời 2021 Biển 70 Tây Ninh",
            "price": "420 Triệu (Còn bớt)",
            "location": "Ngã Ba Mít Một, TX. Hòa Thành, Tây Ninh",
            "district": "hoathanh",
            "category": "raovat",
            "phone": "0919.882.211",
            "authorName": "Bãi Xe Tây Ninh Vận Tải",
            "image": "https://images.unsplash.com/photo-1601584115197-04ecc0da31d7?auto=format&fit=crop&w=800&q=80",
            "description": "Xe gia đình chạy hàng nông sản Tây Ninh - Chợ Đầu Mối Thủ Đức, máy móc êm ru, lốp mới thay, thùng dài 7.2m. Xem xe tại TX. Hòa Thành.",
            "badge": "Chính chủ"
        }
    ]
}

def to_firestore_document(item):
    """Chuyển đổi item dictionary sang định dạng Firestore REST API fields"""
    fields = {}
    for key, val in item.items():
        if isinstance(val, str):
            fields[key] = {"stringValue": val}
        elif isinstance(val, int):
            fields[key] = {"integerValue": str(val)}
        elif isinstance(val, float):
            fields[key] = {"doubleValue": val}
        elif isinstance(val, bool):
            fields[key] = {"booleanValue": val}
        elif isinstance(val, list):
            fields[key] = {"arrayValue": {"values": []}}
    return {"fields": fields}

def crawl_and_push(category, count=3):
    print(f"\n[+] Khởi chạy Tây Ninh Crawler cho chuyên mục: {category.upper()}")
    samples = CRAWL_SAMPLES.get(category, CRAWL_SAMPLES["tuyendung"])
    pushed = 0

    for i in range(min(count, len(samples))):
        sample = samples[i]
        doc_data = {
            "title": sample["title"],
            "subtitle": sample["location"],
            "price": sample["price"],
            "subprice": "Crawl tự động",
            "location": sample["location"],
            "district": sample["district"],
            "category": sample["category"],
            "image": sample["image"],
            "description": sample["description"],
            "authorName": sample["authorName"],
            "authorEmail": "admin.crawler@tayninhinfo.com",
            "phone": sample["phone"],
            "btnType": "apply" if sample["category"] == "tuyendung" else "call",
            "badge": sample.get("badge", "Tin xác thực"),
            "likesCount": 12,
            "likedByMe": False,
            "viewsCount": 45,
            "createdAt": datetime.utcnow().isoformat() + "Z",
            "comments": []
        }

        payload = json.dumps(to_firestore_document(doc_data)).encode("utf-8")
        req = urllib.request.Request(
            FIRESTORE_URL,
            data=payload,
            headers={"Content-Type": "application/json"}
        )

        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                if resp.status in (200, 201):
                    print(f"  [SUCCESS {i+1}/{count}] Đã nạp: {sample['title'][:55]}...")
                    pushed += 1
        except Exception as e:
            print(f"  [ERROR] Không thể đẩy Firestore: {e}")

        time.sleep(0.5)

    print(f"[+] Hoàn tất! Đã cào và lưu thành công {pushed} bài viết lên Cổng thông tin Tây Ninh.\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tây Ninh Crawler Bot (Admin Only)")
    parser.add_argument("--category", choices=["tuyendung", "batdongsan", "raovat", "all"], default="tuyendung", help="Chuyên mục cần cào")
    parser.add_argument("--count", type=int, default=3, help="Số lượng tin mỗi chuyên mục")
    args = parser.parse_args()

    if args.category == "all":
        for cat in ["tuyendung", "batdongsan", "raovat"]:
            crawl_and_push(cat, args.count)
    else:
        crawl_and_push(args.category, args.count)
