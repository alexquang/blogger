---
title: Quy Tắc & Chuẩn Phát Triển Dự Án Tây Ninh Info (Blogger TN Hub)
version: 1.0.0
author: Pham Thanh Quang (ptquang0968@gmail.com)
updated: 2026-11-19
---

# Quy Tắc Phát Triển Dự Án Tây Ninh Info (www.tayninhinfo.com)

## 1. Tổng quan Kiến trúc Hệ thống
- **Nền tảng chính:** Google Blogger Template XML (`/data/projects/blogger/theme.xml`).
- **Tên miền hoạt động:** `https://www.tayninhinfo.com`.
- **Backend & Cơ sở dữ liệu:** Google Cloud Firestore (Project `fir-1b417`).
- **Quyền Quản trị viên tối cao (Admin):** `ptquang0968@gmail.com`.
- **Mã nguồn Git:** `alexquang/blogger.git` (nhánh `main`).

---

## 2. Quy chuẩn Công nghệ & Thư viện (Tech Stack)
- **Framework UI:** Vue 3 (Composition API qua CDN).
- **Styling:** Tailwind CSS v3 với bảng màu Oracle Redwood sang trọng:
  - Màu chủ đạo: Đỏ mận Oracle `#C74634` (hover: `#B13C2C`).
  - Nền & Viền: `#FAF9F8`, `#F1EFED`, viền `#E0DDD8`, chữ `#161513`.
- **Icons:** FontAwesome 6.5.1 (`fa-solid`, `fa-regular`, `fa-brands`).
- **Bản đồ:** Tích hợp Google Maps Embed và Leaflet Raster Tiles tốc độ cao, hoàn toàn miễn phí, không yêu cầu Google API Key.
- **Firebase SDK:** v10.9.0, luôn khởi tạo với `experimentalForceLongPolling: true` để đảm bảo kết nối realtime ổn định tuyệt đối trên mọi mạng và mọi trình duyệt.

---

## 3. Quy tắc Bắt buộc khi Chỉnh sửa `theme.xml`
1. **Tính Hợp lệ Cú pháp XML 100%:**
   - Tuyệt đối không để dấu `&` đơn lẻ trong template HTML; luôn mã hóa thành `&amp;` (ví dụ: `?auto=format&amp;fit=crop`).
   - Toàn bộ code JavaScript và CSS tùy biến phải được bao bọc bên trong thẻ CDATA: `//<![CDATA[ ... //]]>`.
   - Sau mỗi lần chỉnh sửa `theme.xml`, BẮT BUỘC kiểm tra lại bằng script Python `xml.etree.ElementTree.parse()` trước khi lưu/push.

2. **Chống Tải Lại Trang (Zero Reload UX):**
   - Mọi nút bấm, icon thao tác (Like, Comment, Phân trang, Mở Modal) phải có thuộc tính `type='button'` và gắn cờ `@click.prevent` hoặc `@click.stop`.
   - Khi cập nhật dữ liệu qua `onSnapshot`, bắt buộc phải lưu giữ trạng thái UI của người dùng (`showComments`, `newCommentText`, `likedByMe`) qua `stateMap` để khung bình luận không bị sập hay mất nội dung đang nhập dở.

3. **Chống Lỗi Ảnh (Image Error Fallback):**
   - Mọi thẻ `<img>` hiển thị nội dung động từ Firestore phải có sự kiện `@error='handleImgError'` để tự động gán ảnh mặc định sắc nét, tránh lỗi ảnh vỡ hoặc lỗi 404 từ máy chủ ảnh bên thứ ba.

4. **Phân quyền Quản Trị Viên (Admin Security):**
   - Biến `isAdmin` xác thực nghiêm ngặt tài khoản Google đăng nhập: `currentUser.value && currentUser.value.uid && currentUser.value.email === 'ptquang0968@gmail.com'`.
   - Nút **"Xóa bài đăng"** chỉ được hiển thị khi `isAdmin === true`.
   - Mọi hành động xóa phải có modal xác nhận cảnh báo trước khi gọi lệnh `deleteDoc` trên Cloud Firestore.

---

## 4. Cấu trúc Dữ liệu Firestore
- **`listings`:** Lưu trữ 200+ tin đăng địa điểm, dịch vụ, nhà đất, tuyển dụng tại Tây Ninh.
- **`messages`:** Lưu trữ tin nhắn và thông báo đẩy realtime cho cộng đồng Tây Ninh.
- **`place_reviews`:** Lưu trữ các đánh giá trải nghiệm thực tế từ người dùng.
- **Quy tắc Rules:** Đặt tại `/data/projects/blogger/firebase/firestore.rules`.

---

## 5. Tự động Upload / Đồng bộ Giao diện lên Blogger
- Sau khi chỉnh sửa và kiểm tra cú pháp XML thành công, Antigravity có thể tự động đồng bộ giao diện lên Blogger bằng lệnh:
  ```bash
  ~/blogger-bot/.venv/bin/python ~/blogger-bot/upload_blogger.py /data/projects/blogger/theme.xml
  ```
- Script sử dụng Playwright và profile Chrome lưu tại `~/blogger-bot/chrome-profile` để tự động vào mục Theme -> More options -> Restore và nạp file `theme.xml`.
