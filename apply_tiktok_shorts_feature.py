with open('/data/projects/blogger/theme.xml', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Thêm nút Shorts TikTok vào Sidebar (dòng ~255)
old_sidebar_btn = """          <!-- Video YouTube Tây Ninh Menu Item -->
          <button v-on:click='activeTab = "video"' v-bind:class='activeTab === "video" ? "bg-[#F1EFED] text-[#C74634] font-bold border-l-2 border-[#C74634]" : "text-slate-700 hover:bg-[#F1EFED]"' class='w-full flex items-center justify-between px-3 py-2 transition text-xs'>
            <div class='flex items-center gap-3 min-w-0'>
              <i class='fa-brands fa-youtube text-red-600 text-xs shrink-0'></i>
              <span class='whitespace-nowrap font-medium'>{{ t('videoTN') }}</span>
            </div>
            <span class='text-[9px] bg-red-100 text-red-700 px-2 py-0.5 font-bold uppercase shrink-0 ml-2'>YouTube</span>
          </button>"""

new_sidebar_btn = """          <!-- Video YouTube Tây Ninh Menu Item -->
          <button v-on:click='activeTab = "video"' v-bind:class='activeTab === "video" ? "bg-[#F1EFED] text-[#C74634] font-bold border-l-2 border-[#C74634]" : "text-slate-700 hover:bg-[#F1EFED]"' class='w-full flex items-center justify-between px-3 py-2 transition text-xs'>
            <div class='flex items-center gap-3 min-w-0'>
              <i class='fa-brands fa-youtube text-red-600 text-xs shrink-0'></i>
              <span class='whitespace-nowrap font-medium'>{{ t('videoTN') }}</span>
            </div>
            <span class='text-[9px] bg-red-100 text-red-700 px-2 py-0.5 font-bold uppercase shrink-0 ml-2'>YouTube</span>
          </button>
          <!-- Shorts TikTok Tây Ninh Menu Item -->
          <button v-on:click='openShortsPage' v-bind:class='activeTab === "shorts" ? "bg-[#F1EFED] text-[#FE2C55] font-bold border-l-2 border-[#FE2C55]" : "text-slate-700 hover:bg-[#F1EFED]"' class='w-full flex items-center justify-between px-3 py-2 transition text-xs'>
            <div class='flex items-center gap-3 min-w-0'>
              <i class='fa-brands fa-tiktok text-sm text-[#FE2C55] shrink-0'></i>
              <span class='whitespace-nowrap font-medium'>Shorts TikTok</span>
            </div>
            <span class='text-[9px] bg-rose-100 text-rose-700 px-2 py-0.5 font-bold uppercase shrink-0 ml-2'>HOT 9:16</span>
          </button>"""

assert old_sidebar_btn in content, 'Cannot find old_sidebar_btn'
content = content.replace(old_sidebar_btn, new_sidebar_btn, 1)

# 2. Thêm nút Shorts TikTok vào Header Top Bar (dòng ~595)
old_top_nav = """        <button v-on:click='activeTab = "video"' v-bind:class='activeTab === "video" ? "text-[#C74634] border-b-2 border-[#C74634] pb-2 -mb-2.5 font-black" : "text-slate-500 hover:text-slate-900 pb-2 transition"' class='flex items-center gap-2 shrink-0'>
          <i class='fa-brands fa-youtube text-red-600 text-sm'></i>
          <span>{{ t('videoTN') }} ({{ tayNinhVideos.length }})</span>
          <span class='bg-red-100 text-red-700 text-[9px] px-1 py-0.2 font-black'>YOUTUBE</span>
        </button>"""

new_top_nav = """        <button v-on:click='activeTab = "video"' v-bind:class='activeTab === "video" ? "text-[#C74634] border-b-2 border-[#C74634] pb-2 -mb-2.5 font-black" : "text-slate-500 hover:text-slate-900 pb-2 transition"' class='flex items-center gap-2 shrink-0'>
          <i class='fa-brands fa-youtube text-red-600 text-sm'></i>
          <span>{{ t('videoTN') }} ({{ tayNinhVideos.length }})</span>
          <span class='bg-red-100 text-red-700 text-[9px] px-1 py-0.2 font-black'>YOUTUBE</span>
        </button>
        <button v-on:click='openShortsPage' v-bind:class='activeTab === "shorts" ? "text-[#FE2C55] border-b-2 border-[#FE2C55] pb-2 -mb-2.5 font-black" : "text-slate-500 hover:text-slate-900 pb-2 transition"' class='flex items-center gap-1.5 shrink-0'>
          <i class='fa-brands fa-tiktok text-sm text-[#FE2C55]'></i>
          <span>Shorts TikTok</span>
          <span class='bg-[#FE2C55] text-white text-[9px] px-1.5 py-0.2 font-black uppercase tracking-wider rounded-xs'>TIKTOK</span>
        </button>"""

assert old_top_nav in content, 'Cannot find old_top_nav'
content = content.replace(old_top_nav, new_top_nav, 1)

# 3. Thêm nút Shorts TikTok vào Mobile Bottom Bar (dòng ~4735)
old_mobile_bottom = """      <button type='button' v-on:click='activeTab = "video"' v-bind:class='activeTab === "video" ? "text-[#C74634]" : "text-slate-500 hover:text-slate-800"' class='flex flex-col items-center justify-center flex-1 py-1 transition'>
        <i class='fa-brands fa-youtube text-base mb-0.5' v-bind:class='activeTab === "video" ? "text-red-600" : "text-slate-400"'></i>
        <span class='text-[10px] font-bold'>Video</span>
      </button>"""

new_mobile_bottom = """      <button type='button' v-on:click='activeTab = "video"' v-bind:class='activeTab === "video" ? "text-[#C74634]" : "text-slate-500 hover:text-slate-800"' class='flex flex-col items-center justify-center flex-1 py-1 transition'>
        <i class='fa-brands fa-youtube text-base mb-0.5' v-bind:class='activeTab === "video" ? "text-red-600" : "text-slate-400"'></i>
        <span class='text-[10px] font-bold'>Video</span>
      </button>
      <button type='button' v-on:click='openShortsPage' v-bind:class='activeTab === "shorts" ? "text-[#FE2C55]" : "text-slate-500 hover:text-slate-800"' class='flex flex-col items-center justify-center flex-1 py-1 transition'>
        <i class='fa-brands fa-tiktok text-base mb-0.5' v-bind:class='activeTab === "shorts" ? "text-[#FE2C55]" : "text-slate-400"'></i>
        <span class='text-[10px] font-bold'>TikTok</span>
      </button>"""

assert old_mobile_bottom in content, 'Cannot find old_mobile_bottom'
content = content.replace(old_mobile_bottom, new_mobile_bottom, 1)

# 4. Thêm Section Shorts TikTok Video Player vào khu vực main content (trước activeTab === "video")
old_video_section = """      <!-- 3B. YOUTUBE VIDEO SECTION (CHỈ LẤY VIDEO TỈNH TÂY NINH) -->
      <div v-else-if='activeTab === "video"' class='space-y-5'>"""

new_shorts_section = """      <!-- 3B-2. TIKTOK SHORTS VIDEO SECTION (LƯỚT VIDEO NGẮN CHUẨN TIKTOK 9:16) -->
      <div v-else-if='activeTab === "shorts"' class='space-y-4'>
        
        <!-- Top Toolbar của Shorts: Tiêu đề + Nút Đăng Video (Dành cho VIP Nạp Tiền <= 10MB) -->
        <div class='bg-black text-white p-3 sm:p-4 border border-slate-800 flex flex-wrap items-center justify-between gap-3 shadow-md'>
          <div class='flex items-center gap-2.5'>
            <div class='w-8 h-8 rounded-full bg-gradient-to-tr from-[#FE2C55] to-[#25F4EE] flex items-center justify-center text-black font-black text-sm shadow'>
              <i class='fa-brands fa-tiktok text-white'></i>
            </div>
            <div>
              <h2 class='text-sm sm:text-base font-black uppercase tracking-wider flex items-center gap-2'>
                <span>TÂY NINH SHORTS (TIKTOK STYLE)</span>
                <span class='px-1.5 py-0.2 bg-[#FE2C55] text-white text-[9px] font-black uppercase tracking-wider'>Reels</span>
              </h2>
              <p class='text-[11px] text-slate-400'>
                Lướt xem &amp; chia sẻ khoảnh khắc du lịch, ẩm thực Tây Ninh sinh động 9:16
              </p>
            </div>
          </div>

          <div class='flex items-center gap-2'>
            <!-- Nút Upload Short Video: Chỉ dành cho user đã nạp tiền (<= 10MB) -->
            <button type='button' v-on:click='openShortVideoUploadModal' 
                    class='px-3.5 py-2 bg-gradient-to-r from-[#FE2C55] to-[#E02446] hover:brightness-110 text-white font-black text-xs uppercase tracking-wider flex items-center gap-1.5 shadow-lg transition transform active:scale-95'>
              <i class='fa-solid fa-cloud-arrow-up text-sm'></i>
              <span>+ Đăng Short Video</span>
              <span class='px-1.5 py-0.2 bg-black/40 text-amber-300 text-[9px] font-bold uppercase rounded'>VIP &lt; 10MB</span>
            </button>
            <button type='button' v-on:click='activeTab = "feed"' class='px-3 py-2 bg-slate-800 hover:bg-slate-700 text-white font-bold text-xs transition'>
              Quay lại tin đăng
            </button>
          </div>
        </div>

        <!-- Khung Player Lướt Video Ngắn Chuẩn TikTok 9:16 -->
        <div class='relative w-full max-w-[420px] mx-auto h-[680px] sm:h-[720px] bg-black border border-slate-800 overflow-hidden shadow-2xl flex flex-col justify-between select-none group'>
          
          <!-- Thẻ Video Player chính -->
          <div class='absolute inset-0 bg-black flex items-center justify-center cursor-pointer' v-on:click='togglePlayShortVideo'>
            <video id='tiktokShortPlayer' 
                   v-bind:src='currentShortVideo.url' 
                   v-bind:poster='currentShortVideo.poster'
                   autoplay='true' 
                   loop='true' 
                   playsinline='true'
                   v-bind:muted='isShortMuted'
                   class='w-full h-full object-cover'>
            </video>

            <!-- Gradient bóng mờ trên và dưới để chữ hiển thị rõ -->
            <div class='absolute inset-0 bg-gradient-to-b from-black/50 via-transparent to-black/85 pointer-events-none'></div>

            <!-- Nút Play to ở giữa khi video pause -->
            <div v-if='!isShortPlaying' class='absolute inset-0 flex items-center justify-center bg-black/30 pointer-events-none'>
              <div class='w-16 h-16 rounded-full bg-black/60 text-white flex items-center justify-center text-2xl shadow-xl'>
                <i class='fa-solid fa-play ml-1 text-white'></i>
              </div>
            </div>
          </div>

          <!-- Header Overlay trong Video: Chỉ số video + Nút Âm thanh Mute/Unmute -->
          <div class='relative z-10 p-3.5 flex items-center justify-between text-white'>
            <div class='flex items-center gap-1.5 px-2.5 py-1 bg-black/50 backdrop-blur-md rounded-full text-[11px] font-bold'>
              <span class='w-2 h-2 rounded-full bg-[#FE2C55] animate-pulse'></span>
              <span>{{ activeShortIndex + 1 }} / {{ shortVideosList.length }} Clip</span>
            </div>
            <button type='button' v-on:click.stop='toggleShortMute' class='w-8 h-8 rounded-full bg-black/50 hover:bg-black/80 backdrop-blur-md text-white flex items-center justify-center transition'>
              <i v-bind:class='isShortMuted ? "fa-solid fa-volume-xmark text-slate-400" : "fa-solid fa-volume-high text-emerald-400"'></i>
            </button>
          </div>

          <!-- Right Floating Action Bar (Chuẩn TikTok: Like, Comment, Share, Sound Disc) -->
          <div class='relative z-10 p-3 self-end flex flex-col items-center gap-4 text-white pb-14'>
            
            <!-- Avatar tác giả -->
            <div class='relative mb-1 flex flex-col items-center'>
              <div class='w-10 h-10 rounded-full border-2 border-white overflow-hidden shadow-md bg-slate-800'>
                <img v-bind:src='currentShortVideo.authorAvatar || NO_AVATAR_PLACEHOLDER' class='w-full h-full object-cover' />
              </div>
              <button type='button' v-on:click.stop='followShortAuthor(currentShortVideo)' 
                      class='-mt-2.5 w-5 h-5 rounded-full bg-[#FE2C55] text-white flex items-center justify-center text-[10px] shadow font-bold'>
                <i class='fa-solid fa-plus'></i>
              </button>
            </div>

            <!-- Nút Tim (Like) -->
            <button type='button' v-on:click.stop='toggleLikeShort(currentShortVideo)' class='flex flex-col items-center group/btn transition transform active:scale-125'>
              <div class='w-10 h-10 rounded-full bg-black/40 backdrop-blur-md flex items-center justify-center text-lg shadow transition group-hover/btn:bg-black/60'>
                <i class='fa-solid fa-heart transition' v-bind:class='currentShortVideo.likedByMe ? "text-[#FE2C55] scale-110" : "text-white group-hover/btn:text-rose-300"'></i>
              </div>
              <span class='text-[10px] font-bold mt-1 text-white drop-shadow'>{{ currentShortVideo.likesCount || 0 }}</span>
            </button>

            <!-- Nút Bình luận (Comment) -->
            <button type='button' v-on:click.stop='openShortComments(currentShortVideo)' class='flex flex-col items-center group/btn transition transform active:scale-110'>
              <div class='w-10 h-10 rounded-full bg-black/40 backdrop-blur-md flex items-center justify-center text-lg shadow transition group-hover/btn:bg-black/60'>
                <i class='fa-solid fa-comment-dots text-white group-hover/btn:text-blue-300'></i>
              </div>
              <span class='text-[10px] font-bold mt-1 text-white drop-shadow'>{{ (currentShortVideo.comments || []).length }}</span>
            </button>

            <!-- Nút Chia sẻ (Share) -->
            <button type='button' v-on:click.stop='shareShortVideo(currentShortVideo)' class='flex flex-col items-center group/btn transition transform active:scale-110'>
              <div class='w-10 h-10 rounded-full bg-black/40 backdrop-blur-md flex items-center justify-center text-lg shadow transition group-hover/btn:bg-black/60'>
                <i class='fa-solid fa-share text-white group-hover/btn:text-emerald-300'></i>
              </div>
              <span class='text-[10px] font-bold mt-1 text-white drop-shadow'>Chia sẻ</span>
            </button>

            <!-- Đĩa nhạc quay tròn TikTok -->
            <div class='w-10 h-10 rounded-full bg-slate-900 border-2 border-slate-700 flex items-center justify-center animate-spin' style='animation-duration: 4s;'>
              <i class='fa-solid fa-compact-disc text-amber-400 text-base'></i>
            </div>
          </div>

          <!-- Bottom Left Overlay: Thông tin tác giả, Caption, Âm thanh & Thanh điều hướng -->
          <div class='relative z-10 p-4 text-white space-y-2 pointer-events-auto'>
            <!-- Tên tác giả -->
            <div class='flex items-center gap-2'>
              <span class='font-black text-sm text-white drop-shadow flex items-center gap-1'>
                @{{ currentShortVideo.authorName }}
              </span>
              <span v-if='currentShortVideo.isVip' class='px-1.5 py-0.2 bg-gradient-to-r from-amber-500 to-amber-600 text-slate-950 text-[9px] font-black uppercase rounded shadow-xs'>
                ⭐ VIP Nạp tiền
              </span>
            </div>

            <!-- Caption / Hashtags -->
            <p class='text-xs text-slate-100 leading-snug line-clamp-2 drop-shadow font-medium'>
              {{ currentShortVideo.caption }}
            </p>

            <!-- Nhạc nền & Địa điểm -->
            <div class='flex items-center justify-between text-[11px] text-amber-300 pt-1'>
              <div class='flex items-center gap-1.5 truncate max-w-[240px]'>
                <i class='fa-solid fa-music text-[10px] animate-pulse'></i>
                <span class='truncate'>{{ currentShortVideo.sound || 'Âm thanh gốc - Tây Ninh' }}</span>
              </div>
              <span class='text-slate-300 text-[10px] flex items-center gap-1 shrink-0'>
                <i class='fa-solid fa-location-dot text-[#FE2C55]'></i>
                {{ currentShortVideo.location || 'Tây Ninh' }}
              </span>
            </div>

            <!-- Thanh Progress Bar thanh mảnh chạy theo video -->
            <div class='w-full bg-white/20 h-1 rounded-full overflow-hidden'>
              <div class='bg-[#FE2C55] h-full transition-all duration-200' v-bind:style='{ width: shortVideoProgress + "%" }'></div>
            </div>

            <!-- Nút Điều Hướng Next / Prev Video tiện lợi -->
            <div class='flex items-center justify-between pt-1 text-xs'>
              <button type='button' v-on:click.stop='prevShortVideo' v-bind:disabled='activeShortIndex <= 0' 
                      class='px-3 py-1 bg-white/20 hover:bg-white/30 disabled:opacity-30 disabled:pointer-events-none text-white font-bold backdrop-blur-md rounded transition flex items-center gap-1 text-[11px]'>
                <i class='fa-solid fa-arrow-up'></i> Video trước
              </button>
              <button type='button' v-on:click.stop='nextShortVideo' v-bind:disabled='activeShortIndex >= shortVideosList.length - 1' 
                      class='px-3 py-1 bg-[#FE2C55] hover:bg-[#E02446] disabled:opacity-30 disabled:pointer-events-none text-white font-bold rounded transition flex items-center gap-1 text-[11px] shadow'>
                Video tiếp <i class='fa-solid fa-arrow-down'></i>
              </button>
            </div>
          </div>

        </div> <!-- End Khung Player TikTok -->

      </div> <!-- End 3B-2 TikTok Shorts Section -->

      <!-- 3B. YOUTUBE VIDEO SECTION (CHỈ LẤY VIDEO TỈNH TÂY NINH) -->
      <div v-else-if='activeTab === "video"' class='space-y-5'>"""

assert old_video_section in content, 'Cannot find old_video_section'
content = content.replace(old_video_section, new_shorts_section, 1)

# 5. Thêm Modals (Upload Short Video + Comments Sheet) vào khu vực modal cuối trang
old_modals_end = """    <!-- 13. MODAL ADMIN CRAWLER PANEL (CHỈ QUẢN TRỊ VIÊN MỚI TRUY CẬP ĐƯỢC) -->"""

new_modals = """    <!-- MODAL ĐĂNG SHORT VIDEO TIKTOK (CHỈ DÀNH CHO USER ĐÃ NẠP TIỀN - TỐI ĐA 10MB) -->
    <div v-if='showShortVideoUploadModal' v-cloak='true' class='fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-5 bg-black/80 backdrop-blur-sm overflow-y-auto'>
      <div class='bg-white border border-[#E0DDD8] max-w-lg w-full overflow-hidden shadow-2xl relative my-auto text-xs'>
        
        <!-- Header Modal -->
        <div class='px-4 py-3 bg-[#161513] text-white flex items-center justify-between border-b-2 border-[#FE2C55]'>
          <div class='flex items-center gap-2'>
            <div class='w-6 h-6 rounded-full bg-gradient-to-tr from-[#FE2C55] to-[#25F4EE] flex items-center justify-center text-black font-black text-xs'>
              <i class='fa-brands fa-tiktok text-white'></i>
            </div>
            <h3 class='font-black text-xs sm:text-sm uppercase tracking-wide'>
              Đăng Short Video TikTok Tây Ninh (Dành Cho VIP)
            </h3>
          </div>
          <button type='button' v-on:click='showShortVideoUploadModal = false' class='w-7 h-7 flex items-center justify-center text-slate-400 hover:text-white transition'>
            <i class='fa-solid fa-xmark text-sm'></i>
          </button>
        </div>

        <!-- Banner cảnh báo dung lượng <= 10MB và đặc quyền VIP -->
        <div class='p-3 bg-amber-50 border-b border-amber-200 flex items-center justify-between gap-2 text-[11px]'>
          <div class='flex items-center gap-2 text-amber-900'>
            <i class='fa-solid fa-crown text-amber-600 text-sm'></i>
            <span>Đặc quyền tài khoản VIP: Đăng tải video ngắn tiếp cận hàng nghìn khách du lịch Tây Ninh.</span>
          </div>
          <span class='px-2 py-0.5 bg-rose-600 text-white font-black text-[10px] uppercase rounded shrink-0'>
            Tối đa 10MB
          </span>
        </div>

        <!-- Form Body -->
        <form v-on:submit.prevent='submitShortVideo' class='p-4 space-y-4'>
          
          <!-- Khu vực chọn file video từ thiết bị -->
          <div>
            <label class='block font-bold text-slate-700 mb-1.5 flex items-center justify-between'>
              <span>Chọn file video từ máy tính / điện thoại:</span>
              <span class='text-rose-600 font-bold text-[10px]'>* Giới hạn ≤ 10MB</span>
            </label>
            <div class='border-2 border-dashed border-[#E0DDD8] hover:border-[#FE2C55] p-4 text-center bg-[#FAF9F8] transition relative cursor-pointer'>
              <input type='file' accept='video/mp4,video/webm,video/quicktime' v-on:change='handleShortVideoFileSelect' 
                     class='absolute inset-0 opacity-0 cursor-pointer w-full h-full' />
              <div v-if='!shortUploadForm.videoUrl' class='space-y-1.5 pointer-events-none'>
                <i class='fa-solid fa-cloud-arrow-up text-2xl text-slate-400'></i>
                <p class='font-bold text-xs text-slate-700'>Nhấn để chọn video MP4 / WebM</p>
                <p class='text-[10px] text-slate-500'>Định dạng 9:16 hoặc video dọc để hiển thị đẹp nhất (Dung lượng ≤ 10MB)</p>
              </div>
              <div v-else='true' class='space-y-2 pointer-events-none'>
                <div class='h-36 max-w-[200px] mx-auto bg-black rounded overflow-hidden shadow'>
                  <video v-bind:src='shortUploadForm.videoUrl' class='w-full h-full object-cover' controls='false'></video>
                </div>
                <p class='text-emerald-700 font-bold text-[11px]'>
                  <i class='fa-solid fa-circle-check'></i> Đã nạp video ({{ shortUploadForm.fileSizeMB }} MB / 10MB tối đa)
                </p>
              </div>
            </div>
          </div>

          <!-- Hoặc nhập link video trực tiếp (MP4 URL / CDN) -->
          <div>
            <label class='block font-bold text-slate-700 mb-1'>Hoặc dán trực tiếp URL video (MP4 / WebM):</label>
            <input type='url' v-model='shortUploadForm.videoUrl' placeholder='https://domain.com/video.mp4...' 
                   class='w-full px-3 py-2 bg-white border border-[#E0DDD8] text-xs outline-none focus:border-[#FE2C55]' />
          </div>

          <!-- Tiêu đề / Caption + Hashtag -->
          <div>
            <label class='block font-bold text-slate-700 mb-1'>Tiêu đề / Caption video ngắn:</label>
            <textarea v-model='shortUploadForm.caption' rows='2' placeholder='Nhập cảm nghĩ, giới thiệu món ăn, điểm check-in #tayninh #shorts...' 
                      class='w-full px-3 py-2 bg-white border border-[#E0DDD8] text-xs outline-none focus:border-[#FE2C55]' required='true'></textarea>
            <!-- Gợi ý hashtag nhanh -->
            <div class='flex items-center gap-1.5 mt-1 text-[10px] text-slate-500 overflow-x-auto pb-0.5'>
              <span class='font-semibold'>Gợi ý:</span>
              <button type='button' v-on:click='shortUploadForm.caption += " #tayninh"' class='px-1.5 py-0.5 bg-slate-100 hover:bg-slate-200'>#tayninh</button>
              <button type='button' v-on:click='shortUploadForm.caption += " #nuibaden"' class='px-1.5 py-0.5 bg-slate-100 hover:bg-slate-200'>#nuibaden</button>
              <button type='button' v-on:click='shortUploadForm.caption += " #amthuc"' class='px-1.5 py-0.5 bg-slate-100 hover:bg-slate-200'>#amthuc</button>
              <button type='button' v-on:click='shortUploadForm.caption += " #shorts"' class='px-1.5 py-0.5 bg-slate-100 hover:bg-slate-200'>#shorts</button>
            </div>
          </div>

          <div class='grid grid-cols-1 sm:grid-cols-2 gap-3'>
            <!-- Tên âm thanh / Nhạc nền -->
            <div>
              <label class='block font-bold text-slate-700 mb-1'>Tên âm thanh / Nhạc nền:</label>
              <input type='text' v-model='shortUploadForm.sound' placeholder='Âm thanh gốc - Tây Ninh...' 
                     class='w-full px-3 py-1.5 bg-white border border-[#E0DDD8] text-xs' />
            </div>
            <!-- Vị trí check-in -->
            <div>
              <label class='block font-bold text-slate-700 mb-1'>Địa điểm check-in:</label>
              <input type='text' v-model='shortUploadForm.location' placeholder='Núi Bà Đen, Tây Ninh...' 
                     class='w-full px-3 py-1.5 bg-white border border-[#E0DDD8] text-xs' />
            </div>
          </div>

          <!-- Nút Đăng Video -->
          <div class='pt-2 border-t border-[#E0DDD8] flex items-center justify-end gap-2'>
            <button type='button' v-on:click='showShortVideoUploadModal = false' class='px-4 py-2 bg-slate-200 hover:bg-slate-300 text-slate-700 font-bold text-xs'>
              Hủy
            </button>
            <button type='submit' class='px-5 py-2 bg-gradient-to-r from-[#FE2C55] to-[#E02446] hover:brightness-110 text-white font-black text-xs uppercase tracking-wider shadow transition'>
              <i class='fa-solid fa-paper-plane mr-1'></i> Đăng Lên Shorts TikTok
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- MODAL BÌNH LUẬN SHORT VIDEO TIKTOK -->
    <div v-if='showShortCommentsModal &amp;&amp; currentShortVideo' v-cloak='true' class='fixed inset-0 z-50 flex items-end sm:items-center justify-center p-0 sm:p-5 bg-black/60 backdrop-blur-xs'>
      <div class='bg-white border border-[#E0DDD8] max-w-md w-full h-[65vh] sm:h-[500px] flex flex-col shadow-2xl relative text-xs'>
        <!-- Header -->
        <div class='px-4 py-3 border-b border-[#E0DDD8] flex items-center justify-between'>
          <h4 class='font-bold text-xs text-[#161513] uppercase flex items-center gap-1.5'>
            <i class='fa-solid fa-comments text-[#FE2C55]'></i>
            <span>Bình Luận ({{ (currentShortVideo.comments || []).length }})</span>
          </h4>
          <button type='button' v-on:click='showShortCommentsModal = false' class='w-7 h-7 flex items-center justify-center text-slate-500 hover:text-black'>
            <i class='fa-solid fa-xmark text-sm'></i>
          </button>
        </div>
        <!-- Comment List -->
        <div class='flex-1 overflow-y-auto p-3 space-y-3 bg-[#FAF9F8]'>
          <div v-if='!currentShortVideo.comments || currentShortVideo.comments.length === 0' class='text-center py-10 text-slate-400'>
            Chưa có bình luận nào. Hãy là người đầu tiên bình luận!
          </div>
          <div v-for='(c, idx) in currentShortVideo.comments' v-bind:key='idx' class='flex items-start gap-2.5'>
            <img v-bind:src='c.authorAvatar || NO_AVATAR_PLACEHOLDER' class='w-7 h-7 rounded-full object-cover border border-[#E0DDD8] shrink-0' />
            <div class='flex-1 bg-white p-2.5 border border-[#E0DDD8] rounded space-y-1'>
              <div class='flex items-center justify-between'>
                <span class='font-bold text-slate-800 text-[11px]'>{{ c.authorName }}</span>
                <span class='text-[9px] text-slate-400'>{{ formatTime(c.createdAt) }}</span>
              </div>
              <p class='text-xs text-slate-700'>{{ c.text }}</p>
            </div>
          </div>
        </div>
        <!-- Comment Input -->
        <div class='p-2.5 bg-white border-t border-[#E0DDD8] flex items-center gap-2'>
          <input type='text' v-model='shortNewCommentText' v-on:keydown.enter='submitShortComment' 
                 placeholder='Thêm bình luận cho video này...' 
                 class='flex-1 px-3 py-2 bg-[#F1EFED] border border-[#E0DDD8] text-xs outline-none focus:border-[#FE2C55]' />
          <button type='button' v-on:click='submitShortComment' class='px-4 py-2 bg-[#FE2C55] hover:bg-[#E02446] text-white font-bold text-xs'>
            Gửi
          </button>
        </div>
      </div>
    </div>

    <!-- 13. MODAL ADMIN CRAWLER PANEL (CHỈ QUẢN TRỊ VIÊN MỚI TRUY CẬP ĐƯỢC) -->"""

assert old_modals_end in content, 'Cannot find old_modals_end'
content = content.replace(old_modals_end, new_modals, 1)

# 6. Thêm State & Logic của Shorts TikTok vào Setup()
old_setup_marker = """        // QUẢN LÝ BẠN BÈ STATE
        const showFriendsModal = ref(false);
        const friendsList = ref([]);"""

new_setup_logic = """        // QUẢN LÝ BẠN BÈ STATE
        const showFriendsModal = ref(false);
        const friendsList = ref([]);

        // ==========================================
        // TÍNH NĂNG TIKTOK SHORTS VIDEO (REELS 9:16)
        // ==========================================
        const activeShortIndex = ref(0);
        const isShortPlaying = ref(true);
        const isShortMuted = ref(false);
        const shortVideoProgress = ref(0);
        const showShortVideoUploadModal = ref(false);
        const showShortCommentsModal = ref(false);
        const shortNewCommentText = ref('');

        const shortUploadForm = ref({
          caption: '',
          sound: 'Âm thanh gốc - Tây Ninh',
          location: 'TP. Tây Ninh',
          videoUrl: '',
          file: null,
          fileSizeMB: 0
        });

        // KHO SHORT VIDEO TÂY NINH MẪU CHUẨN TIKTOK (9:16)
        const defaultShortVideos = [
          {
            id: 'short_1',
            url: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4',
            poster: 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=600&q=80',
            authorName: 'Núi Bà Đen Travel',
            authorAvatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=120&q=80',
            authorEmail: 'nuibaden@tnhub.vn',
            isVip: true,
            caption: 'Săn mây bồng bềnh trên nóc nhà Nam Bộ đỉnh Núi Bà Đen sáng sớm siêu chill ☁️🏔️ #nuibaden #tayninh #shorts #dulich',
            sound: 'Âm thanh gốc - Nhạc chill Tây Ninh',
            location: 'Đỉnh Núi Bà Đen (986m)',
            likesCount: 1420,
            likedByMe: false,
            comments: [
              { authorName: 'Quang Pham', authorAvatar: 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=80&q=80', text: 'Cảnh đẹp mê hồn! Cuối tuần này mình nhất định đi!', createdAt: '2026-03-20T10:00:00Z' },
              { authorName: 'Lan Huong', authorAvatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=80&q=80', text: 'Cáp treo lên đỉnh bao nhiêu tiền vậy bạn?', createdAt: '2026-03-20T11:00:00Z' }
            ],
            sharesCount: 312,
            createdAt: '2026-03-20T08:00:00Z'
          },
          {
            id: 'short_2',
            url: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4',
            poster: 'https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=600&q=80',
            authorName: 'Bò Tơ Năm Sánh',
            authorAvatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=120&q=80',
            authorEmail: 'boto@tnhub.vn',
            isVip: true,
            caption: 'Đặc sản bò tơ nướng than hồng thơm nức mũi chấm mắm nêm đậm đà 🥩🔥 #amthuc #boto #tayninh #foodie',
            sound: 'Âm thanh gốc - Ẩm thực Nam Bộ',
            location: 'TX. Hòa Thành, Tây Ninh',
            likesCount: 890,
            likedByMe: true,
            comments: [
              { authorName: 'Thanh Tung', authorAvatar: 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=80&q=80', text: 'Ngon quá, nhìn thèm chảy nước miếng!', createdAt: '2026-03-20T12:00:00Z' }
            ],
            sharesCount: 154,
            createdAt: '2026-03-20T09:00:00Z'
          },
          {
            id: 'short_3',
            url: 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4',
            poster: 'https://images.unsplash.com/photo-1510312305653-8ed496efae75?auto=format&fit=crop&w=600&q=80',
            authorName: 'Hồ Dầu Tiếng Glamping',
            authorAvatar: 'https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?auto=format&fit=crop&w=120&q=80',
            authorEmail: 'camping@tnhub.vn',
            isVip: true,
            caption: 'Chiều hoàng hôn buông bên Hồ Dầu Tiếng, đốt lửa trại ca hát cùng hội bạn thân 🌅⛺ #camping #hodautieng #tayninh',
            sound: 'Âm thanh gốc - Acoustic Chill',
            location: 'Hồ Dầu Tiếng, Huyện Dương Minh Châu',
            likesCount: 2150,
            likedByMe: false,
            comments: [],
            sharesCount: 480,
            createdAt: '2026-03-20T07:30:00Z'
          }
        ];

        // Lấy danh sách video từ cache localStorage hoặc mặc định
        let initialShorts = defaultShortVideos;
        try {
          const cachedShorts = safeGetStorage('tnhub_shorts_videos', null);
          if (cachedShorts) {
            const parsed = JSON.parse(cachedShorts);
            if (Array.isArray(parsed) && parsed.length > 0) {
              initialShorts = parsed;
            }
          }
        } catch(e) {}

        const shortVideosList = ref(initialShorts);

        const currentShortVideo = computed(() => {
          if (!shortVideosList.value || shortVideosList.value.length === 0) {
            return defaultShortVideos[0];
          }
          const idx = Math.max(0, Math.min(activeShortIndex.value, shortVideosList.value.length - 1));
          return shortVideosList.value[idx];
        });

        const openShortsPage = () => {
          activeTab.value = 'shorts';
          isShortPlaying.value = true;
          const mainEl = document.querySelector('main');
          if (mainEl) mainEl.scrollTop = 0;
          window.scrollTo(0, 0);
          setTimeout(() => {
            const vid = document.getElementById('tiktokShortPlayer');
            if (vid) {
              vid.currentTime = 0;
              vid.play().catch(() => { isShortMuted.value = true; vid.play(); });
            }
          }, 200);
        };

        const nextShortVideo = () => {
          if (activeShortIndex.value < shortVideosList.value.length - 1) {
            activeShortIndex.value++;
            playCurrentShortVideo();
          }
        };

        const prevShortVideo = () => {
          if (activeShortIndex.value > 0) {
            activeShortIndex.value--;
            playCurrentShortVideo();
          }
        };

        const playCurrentShortVideo = () => {
          isShortPlaying.value = true;
          shortVideoProgress.value = 0;
          setTimeout(() => {
            const vid = document.getElementById('tiktokShortPlayer');
            if (vid) {
              vid.currentTime = 0;
              vid.play().catch(() => {});
            }
          }, 150);
        };

        const togglePlayShortVideo = () => {
          const vid = document.getElementById('tiktokShortPlayer');
          if (!vid) return;
          if (vid.paused) {
            vid.play();
            isShortPlaying.value = true;
          } else {
            vid.pause();
            isShortPlaying.value = false;
          }
        };

        const toggleShortMute = () => {
          isShortMuted.value = !isShortMuted.value;
          const vid = document.getElementById('tiktokShortPlayer');
          if (vid) vid.muted = isShortMuted.value;
        };

        const toggleLikeShort = (video) => {
          if (!video) return;
          if (video.likedByMe) {
            video.likesCount = Math.max(0, (video.likesCount || 1) - 1);
            video.likedByMe = false;
          } else {
            video.likesCount = (video.likesCount || 0) + 1;
            video.likedByMe = true;
            playNotificationSound();
          }
          safeSetStorage('tnhub_shorts_videos', JSON.stringify(shortVideosList.value));
        };

        const openShortComments = (video) => {
          if (!video) return;
          showShortCommentsModal.value = true;
        };

        const submitShortComment = () => {
          const text = shortNewCommentText.value.trim();
          if (!text || !currentShortVideo.value) return;
          const user = currentUser.value || guestUser.value;
          if (!currentShortVideo.value.comments) currentShortVideo.value.comments = [];
          currentShortVideo.value.comments.push({
            id: 'c_' + Date.now(),
            authorName: user.displayName || 'Thành viên Tây Ninh',
            authorAvatar: user.photoURL || NO_AVATAR_PLACEHOLDER,
            text: text,
            createdAt: new Date().toISOString()
          });
          shortNewCommentText.value = '';
          safeSetStorage('tnhub_shorts_videos', JSON.stringify(shortVideosList.value));
          showToast('Đã đăng bình luận!', 'success');
        };

        const shareShortVideo = (video) => {
          if (!video) return;
          const text = '[Tây Ninh Shorts] ' + video.caption + ' - Xem ngay trên TNHub: https://www.tayninhinfo.com';
          try {
            navigator.clipboard.writeText(text);
            showToast('Đã sao chép link video ngắn để chia sẻ!', 'success');
          } catch(e) {
            showToast('Link video: ' + video.url, 'info');
          }
        };

        const followShortAuthor = (video) => {
          if (!video) return;
          showToast('Đã theo dõi tác giả @' + video.authorName + '!', 'success');
        };

        // ==========================================
        // QUY TẮC UPLOAD SHORT VIDEO: CHỈ USER ĐÃ NẠP TIỀN & GIỚI HẠN <= 10MB
        // ==========================================
        const openShortVideoUploadModal = () => {
          // KIỂM TRA ĐIỀU KIỆN ĐÃ NẠP TIỀN
          if (!isFundedUser.value && !isAdmin.value) {
            showPopup(
              'Đặc Quyền Thành Viên Nạp Tiền (VIP)',
              'Tính năng Đăng Short Video TikTok lên TNHub chỉ dành riêng cho các thành viên VIP đã nạp tiền!\\n\\nVui lòng nạp tiền vào tài khoản để mở khóa quyền đăng tải các video ngắn triệu view giới thiệu địa điểm, ẩm thực và dịch vụ Tây Ninh.',
              'warning',
              'Nạp tiền mở khóa ngay',
              openDepositModal,
              true,
              'Để sau'
            );
            return;
          }

          shortUploadForm.value = {
            caption: '',
            sound: 'Âm thanh gốc - ' + ((currentUser.value && currentUser.value.displayName) || 'Tây Ninh'),
            location: 'TP. Tây Ninh',
            videoUrl: '',
            file: null,
            fileSizeMB: 0
          };
          showShortVideoUploadModal.value = true;
        };

        const handleShortVideoFileSelect = (event) => {
          const file = event.target.files && event.target.files[0];
          if (!file) return;

          // RÀNG BUỘC CHẶT CHẼ DUNG LƯỢNG KHÔNG QUÁ 10MB (10 * 1024 * 1024 bytes)
          const maxSizeBytes = 10 * 1024 * 1024;
          if (file.size > maxSizeBytes) {
            const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
            showToast('⚠️ Video vượt quá dung lượng cho phép (' + sizeMB + 'MB > 10MB tối đa)! Vui lòng chọn video ngắn hơn hoặc nén lại trước khi đăng.', 'error', 'Quá Dung Lượng 10MB');
            event.target.value = '';
            shortUploadForm.value.videoUrl = '';
            shortUploadForm.value.file = null;
            shortUploadForm.value.fileSizeMB = 0;
            return;
          }

          const sizeMB = (file.size / (1024 * 1024)).toFixed(1);
          shortUploadForm.value.file = file;
          shortUploadForm.value.fileSizeMB = sizeMB;

          // Tạo URL xem trước ngay lập tức
          const blobUrl = URL.createObjectURL(file);
          shortUploadForm.value.videoUrl = blobUrl;
          showToast('Đã chọn video: ' + file.name + ' (' + sizeMB + ' MB / 10MB tối đa - Hợp lệ ✅)', 'success');
        };

        const submitShortVideo = () => {
          if (!shortUploadForm.value.videoUrl) {
            showToast('Vui lòng chọn file video (≤ 10MB) hoặc dán link video MP4!', 'error');
            return;
          }
          if (!shortUploadForm.value.caption.trim()) {
            showToast('Vui lòng nhập tiêu đề / caption cho video!', 'error');
            return;
          }

          const user = currentUser.value || guestUser.value;
          const newShort = {
            id: 'short_' + Date.now(),
            url: shortUploadForm.value.videoUrl,
            poster: 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=600&q=80',
            authorName: user.displayName || 'Thành viên Tây Ninh VIP',
            authorAvatar: user.photoURL || NO_AVATAR_PLACEHOLDER,
            authorEmail: user.email || '',
            isVip: true,
            caption: shortUploadForm.value.caption.trim(),
            sound: shortUploadForm.value.sound.trim() || 'Âm thanh gốc - Tây Ninh',
            location: shortUploadForm.value.location.trim() || 'Tây Ninh',
            likesCount: 1,
            likedByMe: true,
            comments: [],
            sharesCount: 0,
            createdAt: new Date().toISOString()
          };

          // Thêm lên đầu danh sách
          shortVideosList.value.unshift(newShort);
          activeShortIndex.value = 0;
          showShortVideoUploadModal.value = false;

          safeSetStorage('tnhub_shorts_videos', JSON.stringify(shortVideosList.value.slice(0, 30)));
          showToast('🎉 Đăng Short Video TikTok thành công! Video của bạn đang phát trên bảng tin.', 'success', 'Thành Công');
          
          openShortsPage();
        };"""

assert old_setup_marker in content, 'Cannot find old_setup_marker'
content = content.replace(old_setup_marker, new_setup_logic, 1)

# 7. Xuất các biến và hàm mới vào return { ... } của Vue App
old_return_marker = """          openPrivateChat,
          sendPrivateMessage,
          closePrivateChat,"""

new_return_additions = """          openPrivateChat,
          sendPrivateMessage,
          closePrivateChat,
          activeShortIndex,
          isShortPlaying,
          isShortMuted,
          shortVideoProgress,
          showShortVideoUploadModal,
          showShortCommentsModal,
          shortNewCommentText,
          shortUploadForm,
          shortVideosList,
          currentShortVideo,
          openShortsPage,
          nextShortVideo,
          prevShortVideo,
          togglePlayShortVideo,
          toggleShortMute,
          toggleLikeShort,
          openShortComments,
          submitShortComment,
          shareShortVideo,
          followShortAuthor,
          openShortVideoUploadModal,
          handleShortVideoFileSelect,
          submitShortVideo,"""

assert old_return_marker in content, 'Cannot find old_return_marker'
content = content.replace(old_return_marker, new_return_additions, 1)

with open('/data/projects/blogger/theme.xml', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated TikTok Shorts feature successfully!')
