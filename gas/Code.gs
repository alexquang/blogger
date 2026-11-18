/**
 * GOOGLE APPS SCRIPT: Blogger-Web
 * Backend API cho Cổng thông tin & Mạng xã hội TayNinhInfo.com
 */

// CẤU HÌNH HỆ THỐNG
const CONFIG = {
  BLOG_ID: PropertiesService.getScriptProperties().getProperty('BLOG_ID') || '8492019482019283741',
  ADMIN_EMAIL: PropertiesService.getScriptProperties().getProperty('ADMIN_EMAIL') || 'ptquang0968@gmail.com',
  UPLOAD_FOLDER_ID: PropertiesService.getScriptProperties().getProperty('UPLOAD_FOLDER_ID') || '1AbCdEfGhIjKlMnOpQrStUvWxYz123456'
};

/**
 * Xử lý CORS và Response Helper
 */
function createJsonResponse(data) {
  return ContentService.createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}

/**
 * Xử lý OPTIONS Preflight Request (CORS)
 */
function doOptions(e) {
  return ContentService.createTextOutput('')
    .setMimeType(ContentService.MimeType.TEXT);
}

/**
 * Endpoint GET: Kiểm tra trạng thái API & Đọc thông tin tóm tắt
 */
function doGet(e) {
  return createJsonResponse({
    status: 'success',
    service: 'Blogger-Web API for TayNinhInfo.com',
    timestamp: new Date().toISOString()
  });
}

/**
 * Endpoint POST: Tiếp nhận Đăng bài Blogger, Upload File Drive, Ứng tuyển tuyển dụng
 */
function doPost(e) {
  try {
    let payload = {};
    if (e.postData && e.postData.contents) {
      payload = JSON.parse(e.postData.contents);
    } else if (e.parameter) {
      payload = e.parameter;
    }

    const action = payload.action;

    switch (action) {
      case 'create_blogger_post':
        return createJsonResponse(handleCreateBloggerPost(payload));

      case 'upload_image':
      case 'upload_cv':
        return createJsonResponse(handleSaveFileToDrive(payload));

      case 'apply_job':
        return createJsonResponse(handleJobApplication(payload));

      case 'publish_place':
      case 'create_place_post':
        return createJsonResponse(handlePublishPlaceToBlogger(payload));

      default:
        return createJsonResponse({
          status: 'error',
          message: 'Invalid action: ' + action
        });
    }
  } catch (error) {
    return createJsonResponse({
      status: 'error',
      message: error.toString()
    });
  }
}

/**
 * CHỨC NĂNG 1: Tạo bài viết trên Google Blogger qua Blogger API v3
 */
function handleCreateBloggerPost(payload) {
  const blogId = CONFIG.BLOG_ID;
  const isDraft = payload.isDraft !== undefined ? payload.isDraft : false;
  
  const postResource = {
    kind: 'blogger#post',
    title: payload.title || 'Bài viết mới từ TayNinhInfo',
    content: payload.content || '<p>Nội dung đang được cập nhật...</p>',
    labels: payload.labels || ['TayNinhInfo', 'CongDong']
  };

  // Sử dụng Advanced Service Blogger v3 hoặc UrlFetchApp trực tiếp với OAuth token
  const token = ScriptApp.getOAuthToken();
  const url = 'https://www.googleapis.com/blogger/v3/blogs/' + blogId + '/posts' + (isDraft ? '?isDraft=true' : '');

  const response = UrlFetchApp.fetch(url, {
    method: 'post',
    contentType: 'application/json',
    headers: {
      Authorization: 'Bearer ' + token
    },
    payload: JSON.stringify(postResource),
    muteHttpExceptions: true
  });

  const resJson = JSON.parse(response.getContentText());

  // Gửi email thông báo cho Admin kiểm duyệt nội dung
  if (CONFIG.ADMIN_EMAIL) {
    MailApp.sendEmail({
      to: CONFIG.ADMIN_EMAIL,
      subject: '[TayNinhInfo] Có bài viết mới được xuất bản: ' + postResource.title,
      htmlBody: `
        <div style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
          <h2 style="color: #059669;">[TayNinhInfo] Bài viết mới trên Blogger</h2>
          <p><strong>Tiêu đề:</strong> ${postResource.title}</p>
          <p><strong>Chuyên mục:</strong> ${(postResource.labels || []).join(', ')}</p>
          <p><strong>Trạng thái:</strong> ${isDraft ? 'Bản nháp (Draft)' : 'Đã xuất bản (Published)'}</p>
          <p><strong>Liên kết bài viết:</strong> <a href="${resJson.url || '#'}">${resJson.url || 'Đang cập nhật'}</a></p>
          <hr style="border: 0; border-top: 1px solid #eee; margin: 20px 0;"/>
          <p style="font-size: 12px; color: #888;">Thông báo tự động từ hệ thống Blogger-Web.</p>
        </div>
      `
    });
  }

  return {
    status: 'success',
    data: resJson
  };
}

/**
 * CHỨC NĂNG 2: Nhận file đính kèm Base64 (Ảnh/CV) -> Lưu vào Google Drive và trả về public link
 */
function handleSaveFileToDrive(payload) {
  if (!payload.fileBase64) {
    throw new Error('Missing fileBase64 data in payload');
  }

  let folder;
  try {
    folder = DriveApp.getFolderById(CONFIG.UPLOAD_FOLDER_ID);
  } catch (e) {
    folder = DriveApp.getRootFolder();
  }

  // Phân tích định dạng Base64
  const parts = payload.fileBase64.split(',');
  const contentType = parts[0].split(';')[0].replace('data:', '') || 'application/octet-stream';
  const base64Data = parts[1] || parts[0];
  const decodedBlob = Utilities.newBlob(Utilities.base64Decode(base64Data), contentType, payload.fileName || ('upload_' + Date.now()));

  // Tạo file trong thư mục
  const driveFile = folder.createFile(decodedBlob);
  driveFile.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);

  const fileId = driveFile.getId();
  const fileUrl = 'https://lh3.googleusercontent.com/d/' + fileId;
  const downloadUrl = driveFile.getDownloadUrl();

  return {
    status: 'success',
    fileId: fileId,
    fileUrl: fileUrl,
    viewUrl: driveFile.getUrl(),
    downloadUrl: downloadUrl
  };
}

/**
 * CHỨC NĂNG 3: Tiếp nhận đơn ứng tuyển 1-Click Apply & Gửi email thông báo tự động
 */
function handleJobApplication(payload) {
  let cvLink = 'Không đính kèm file';

  // Lưu file CV nếu có
  if (payload.fileBase64) {
    const uploadRes = handleSaveFileToDrive({
      fileBase64: payload.fileBase64,
      fileName: 'CV_' + (payload.fullName || 'Candidate').replace(/\s+/g, '_') + '_' + Date.now() + '_' + (payload.fileName || 'cv.pdf')
    });
    cvLink = `<a href="${uploadRes.viewUrl}" target="_blank" style="color: #2563eb; font-weight: bold;">Tải về / Xem CV ứng viên</a>`;
  }

  // Gửi Email tức thì cho Nhà tuyển dụng / Ban quản trị
  const recipient = CONFIG.ADMIN_EMAIL;
  const jobTitle = payload.jobTitle || 'Vị trí tuyển dụng Tây Ninh';

  MailApp.sendEmail({
    to: recipient,
    subject: `[ỨNG TUYỂN 1-CLICK] Hồ sơ ứng tuyển vị trí: ${jobTitle} - ${payload.fullName}`,
    htmlBody: `
      <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; border: 1px solid #e2e8f0; border-radius: 12px; padding: 24px; background-color: #ffffff;">
        <div style="border-bottom: 2px solid #10b981; padding-bottom: 12px; margin-bottom: 20px;">
          <h2 style="color: #047857; margin: 0;">TayNinhInfo - Thông Báo Ứng Tuyển Mới</h2>
          <span style="font-size: 13px; color: #64748b;">Hệ thống nộp CV 1-Click Fast Apply</span>
        </div>

        <table style="width: 100%; border-collapse: collapse; font-size: 14px; margin-bottom: 20px;">
          <tr>
            <td style="padding: 8px 0; color: #64748b; width: 140px;">Vị trí tuyển dụng:</td>
            <td style="padding: 8px 0; font-weight: bold; color: #1e293b;">${jobTitle}</td>
          </tr>
          <tr>
            <td style="padding: 8px 0; color: #64748b;">Họ và tên ứng viên:</td>
            <td style="padding: 8px 0; font-weight: bold; color: #1e293b;">${payload.fullName}</td>
          </tr>
          <tr>
            <td style="padding: 8px 0; color: #64748b;">Số điện thoại / Zalo:</td>
            <td style="padding: 8px 0; color: #1e293b;"><a href="tel:${payload.phone}" style="color: #059669; font-weight: bold;">${payload.phone}</a></td>
          </tr>
          <tr>
            <td style="padding: 8px 0; color: #64748b;">Email:</td>
            <td style="padding: 8px 0; color: #1e293b;"><a href="mailto:${payload.email}">${payload.email}</a></td>
          </tr>
          <tr>
            <td style="padding: 8px 0; color: #64748b;">Hồ sơ đính kèm (CV):</td>
            <td style="padding: 8px 0;">${cvLink}</td>
          </tr>
          <tr>
            <td style="padding: 8px 0; color: #64748b; vertical-align: top;">Ghi chú / Thư ngỏ:</td>
            <td style="padding: 8px 0; color: #334155; background: #f8fafc; padding: 10px; border-radius: 6px;">${payload.note || 'Không có ghi chú thêm.'}</td>
          </tr>
        </table>

        <div style="background-color: #ecfdf5; border-left: 4px solid #10b981; padding: 12px; font-size: 13px; color: #065f46;">
          <strong>Hành động:</strong> Nhà tuyển dụng có thể liên hệ trực tiếp với ứng viên qua số điện thoại hoặc phản hồi qua email trên.
        </div>

        <p style="font-size: 11px; color: #94a3b8; text-align: center; margin-top: 30px;">
          Bản quyền © 2026 TayNinhInfo.com - Cổng Thông Tin & Mạng Xã Hội Tỉnh Tây Ninh.
        </p>
      </div>
    `
  });

  return {
    status: 'success',
    message: 'Application recorded and email sent successfully'
  };
}

/**
 * CHỨC NĂNG 4: Tự động đăng địa điểm "Tây Ninh Go" lên Blogger chuẩn SEO
 */
function handlePublishPlaceToBlogger(payload) {
  const blogId = CONFIG.BLOG_ID;
  const isDraft = payload.isDraft !== undefined ? payload.isDraft : false;

  const { name, category, address, lat, lng, description } = payload;
  if (!name || !category || !address) {
    throw new Error('Thiếu thông tin bắt buộc: name, category hoặc address.');
  }

  const postTitle = `[Tây Ninh Go] ${name} - Địa điểm ${category} tại Tây Ninh`;
  const labels = ['Tây Ninh Go', category, 'Địa điểm Tây Ninh', 'Du lịch Tây Ninh'];

  // Nội dung HTML tối ưu hóa SEO với Schema.org LocalBusiness
  const postContent = `
    <div class="tayninhgo-place-article" style="font-family: Arial, sans-serif; line-height: 1.7; color: #1e293b;">
      <h2 style="color: #059669; font-size: 22px; border-bottom: 2px solid #10b981; padding-bottom: 8px;">
        📍 ${name}
      </h2>
      
      <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 14px; margin: 16px 0;">
        <p style="margin: 4px 0;"><strong>🏷️ Danh mục:</strong> <span style="background: #e0f2fe; color: #0369a1; padding: 2px 8px; border-radius: 4px; font-weight: 600;">${category}</span></p>
        <p style="margin: 4px 0;"><strong>🏠 Địa chỉ:</strong> ${address}</p>
        ${lat && lng ? `<p style="margin: 4px 0;"><strong>🌐 Tọa độ GPS:</strong> ${lat}, ${lng}</p>` : ''}
      </div>

      <h3 style="color: #047857; margin-top: 20px;">Giới thiệu địa điểm</h3>
      <p style="text-align: justify;">
        ${description ? description : `${name} là một trong những địa điểm ${category.toLowerCase()} uy tín, được ghi nhận và chia sẻ trên bản đồ danh bạ số Tây Ninh Go.`}
      </p>

      ${lat && lng ? `
      <div style="margin: 24px 0; text-align: center;">
        <a href="https://www.google.com/maps?q=${lat},${lng}" target="_blank" rel="noopener noreferrer" 
           style="display: inline-block; background-color: #059669; color: #ffffff; padding: 10px 20px; border-radius: 6px; text-decoration: none; font-weight: bold; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
          🗺️ Xem vị trí và chỉ đường trên Google Maps
        </a>
      </div>
      ` : ''}

      <div style="border-top: 1px solid #e2e8f0; margin-top: 24px; padding-top: 12px; font-size: 13px; color: #64748b;">
        <p>Nguồn dữ liệu: <em>Cộng đồng Tây Ninh Go - Nền tảng kết nối thông tin địa phương Tây Ninh.</em></p>
      </div>

      <!-- Dữ liệu có cấu trúc SEO Schema LocalBusiness -->
      <script type="application/ld+json">
      {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "${name}",
        "address": {
          "@type": "PostalAddress",
          "streetAddress": "${address}",
          "addressRegion": "Tây Ninh",
          "addressCountry": "VN"
        }
        ${lat && lng ? `,"geo": {
          "@type": "GeoCoordinates",
          "latitude": ${lat},
          "longitude": ${lng}
        }` : ''}
      }
      <\/script>
    </div>
  `;

  // Gọi Blogger API v3
  const token = ScriptApp.getOAuthToken();
  const url = 'https://www.googleapis.com/blogger/v3/blogs/' + blogId + '/posts' + (isDraft ? '?isDraft=true' : '');

  const response = UrlFetchApp.fetch(url, {
    method: 'post',
    contentType: 'application/json',
    headers: {
      Authorization: 'Bearer ' + token
    },
    payload: JSON.stringify({
      kind: 'blogger#post',
      title: postTitle,
      content: postContent,
      labels: labels
    }),
    muteHttpExceptions: true
  });

  const resJson = JSON.parse(response.getContentText());

  if (resJson.error) {
    throw new Error('Lỗi Blogger API: ' + (resJson.error.message || JSON.stringify(resJson.error)));
  }

  return {
    status: 'success',
    postId: resJson.id,
    postUrl: resJson.url,
    title: postTitle
  };
}
