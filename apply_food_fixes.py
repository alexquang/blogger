with open('/data/projects/blogger/theme.xml', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update openFoodDetailPage & closeFoodDetailPage
old_food_nav = """        const openFoodDetailPage = (card) => {
          if (!card) return;
          incrementView(card);
          selectedFoodCard.value = card;
          foodActiveTab.value = 'intro';
          activeTab.value = 'food_detail';
          try {
            window.scrollTo({ top: 0, behavior: 'smooth' });
          } catch(e) {}
        };

        const closeFoodDetailPage = () => {
          activeTab.value = 'feed';
          activeCategory.value = 'amthuc';
          try {
            window.scrollTo({ top: 0, behavior: 'smooth' });
          } catch(e) {}
        };"""

new_food_nav = """        const openFoodDetailPage = (card) => {
          if (!card) return;
          incrementView(card);
          selectedFoodCard.value = card;
          foodActiveTab.value = 'intro';
          activeTab.value = 'food_detail';
          const scrollToTop = () => {
            const mainEl = document.querySelector('main');
            if (mainEl) {
              mainEl.scrollTop = 0;
            }
            window.scrollTo({ top: 0, behavior: 'instant' });
            document.documentElement.scrollTop = 0;
            document.body.scrollTop = 0;
          };
          scrollToTop();
          setTimeout(scrollToTop, 20);
          setTimeout(scrollToTop, 100);
        };

        const closeFoodDetailPage = () => {
          activeTab.value = 'feed';
          activeCategory.value = 'amthuc';
          const scrollToTop = () => {
            const mainEl = document.querySelector('main');
            if (mainEl) {
              mainEl.scrollTop = 0;
            }
            window.scrollTo({ top: 0, behavior: 'instant' });
            document.documentElement.scrollTop = 0;
            document.body.scrollTop = 0;
          };
          scrollToTop();
          setTimeout(scrollToTop, 20);
          setTimeout(scrollToTop, 100);
        };"""

assert old_food_nav in content, 'Cannot find old_food_nav'
content = content.replace(old_food_nav, new_food_nav, 1)

# 2. Update Highlights section (Điểm đặc sắc thu hút du khách)
old_highlights = """              <!-- Điểm nổi bật độc quyền -->
              <div class='bg-[#FAF9F8] p-4 border-l-4 border-[#C74634] space-y-2'>
                <h4 class='text-xs font-bold text-[#161513] uppercase flex items-center gap-1.5'>
                  <i class='fa-solid fa-award text-[#C74634]'></i>
                  <span>Điểm Đặc Sắc Thu Hút Du Khách</span>
                </h4>
                <ul class='text-xs text-slate-600 space-y-1.5 list-disc list-inside font-medium'>
                  <li>Nguồn nguyên liệu tươi sống sạch 100%, nhập trực tiếp từ nông trại và lò mổ đạt chuẩn an toàn VSTP tại Tây Ninh.</li>
                  <li>Hương vị bí truyền Nam Bộ, kết hợp rổ rau rừng Tây Ninh tươi non và bánh tráng phơi sương trứ danh.</li>
                  <li>Không gian thoáng mát, cảnh quan xanh, bãi đỗ xe rộng rãi thuận tiện cho cả khách đoàn và gia đình.</li>
                </ul>
              </div>"""

new_highlights = """              <!-- Điểm nổi bật độc quyền -->
              <div class='bg-[#FAF9F8] p-4 border-l-4 border-[#C74634] space-y-2'>
                <h4 class='text-xs font-bold text-[#161513] uppercase flex items-center gap-1.5'>
                  <i class='fa-solid fa-award text-[#C74634]'></i>
                  <span>{{ currentLang === "en" ? "Exclusive Highlights &amp; Features" : currentLang === "ko" ? "주요 특징 및 매력 포인트" : currentLang === "zh" ? "特色亮点与核心优势" : "Điểm Đặc Sắc Thu Hút Du Khách" }}</span>
                </h4>
                <ul v-if='selectedFoodCard.subCategory === "chay"' class='text-xs text-slate-600 space-y-1.5 list-disc list-inside font-medium'>
                  <li>{{ currentLang === "en" ? "100% pure plant-based fresh ingredients from local organic mushroom &amp; vegetable farms." : "100% nguyên liệu thuần thực vật tươi sạch, thanh tịnh từ các nông trại rau nấm hữu cơ Tây Ninh." }}</li>
                  <li>{{ currentLang === "en" ? "Authentic Southern Vietnamese flavor nuances with legendary Tay Ninh grapefruit spring rolls (Nem bưởi)." : "Hương vị bí truyền Nam Bộ, biến tấu tinh tế kèm đặc sản nem bưởi trứ danh vùng đất Thánh." }}</li>
                  <li>{{ currentLang === "en" ? "Peaceful, pure and elegant atmosphere ideal for vegetarian dining, pilgrimage tours &amp; families." : "Không gian thanh tịnh, trang nhã, điểm hẹn lý tưởng cho Phật tử và du khách hành hương." }}</li>
                </ul>
                <ul v-else-if='selectedFoodCard.subCategory === "khach_san"' class='text-xs text-slate-600 space-y-1.5 list-disc list-inside font-medium'>
                  <li>{{ currentLang === "en" ? "Prime central or mountain-foot location with panoramic views of Ba Den Mountain." : "Vị trí đắc địa ngay trung tâm thành phố hoặc chân núi, view trực diện mây vờn Núi Bà Đen hùng vĩ." }}</li>
                  <li>{{ currentLang === "en" ? "Modern luxurious amenities, premium bedding, swimming pool, gym &amp; rich buffet breakfast." : "Hệ thống phòng nghỉ cao cấp sang trọng, tiện ích hồ bơi, gym, buffet sáng và dịch vụ chuyên nghiệp." }}</li>
                  <li>{{ currentLang === "en" ? "24/7 dedicated concierge, spacious secure parking lot suitable for large tour groups." : "Đội ngũ lễ tân chu đáo 24/7, hầm và bãi đỗ xe an ninh rộng rãi cho xe ô tô và đoàn du lịch." }}</li>
                </ul>
                <ul v-else-if='selectedFoodCard.subCategory === "cafe"' class='text-xs text-slate-600 space-y-1.5 list-disc list-inside font-medium'>
                  <li>{{ currentLang === "en" ? "Scenic 360-degree open-air panorama view of Ba Den Mountain, ideal for photo check-ins." : "Tầm nhìn panorama 360 độ ngắm trọn Núi Bà Đen mây phủ và hoàng hôn tuyệt đẹp, ngập tràn góc check-in." }}</li>
                  <li>{{ currentLang === "en" ? "Craft coffee menu from fresh beans, refreshing seasonal fruit teas &amp; artisan pastries." : "Menu đồ uống đa dạng từ cà phê rang xay nguyên chất, trà hoa quả thanh mát đến bánh ngọt thủ công." }}</li>
                  <li>{{ currentLang === "en" ? "Relaxing garden seating, acoustic music, friendly hospitality and spacious parking." : "Không gian sân vườn thoáng mát, âm nhạc thư thái, bãi đỗ xe ô tô thuận tiện cho bạn bè và gia đình." }}</li>
                </ul>
                <ul v-else='true' class='text-xs text-slate-600 space-y-1.5 list-disc list-inside font-medium'>
                  <li>{{ currentLang === "en" ? "100% fresh, locally sourced meat &amp; produce meeting strict food safety standards." : "Nguồn nguyên liệu tươi sống sạch 100%, nhập trực tiếp trong ngày đạt chuẩn an toàn VSTP tại Tây Ninh." }}</li>
                  <li>{{ currentLang === "en" ? "Traditional Tay Ninh recipes paired with fresh wild herbs &amp; dew-wetted rice paper." : "Hương vị bí truyền Nam Bộ, kết hợp rổ rau rừng Tây Ninh tươi non và bánh tráng phơi sương trứ danh." }}</li>
                  <li>{{ currentLang === "en" ? "Spacious airy dining atmosphere with dedicated parking accommodating families and large tour buses." : "Không gian thoáng mát, cảnh quan xanh, bãi đỗ xe rộng rãi thuận tiện cho cả khách đoàn và gia đình." }}</li>
                </ul>
              </div>"""

assert old_highlights in content, 'Cannot find old_highlights'
content = content.replace(old_highlights, new_highlights, 1)

# 3. Update Suggestion block (Khối gợi ý)
old_rec_block = """        <!-- Khối Gợi Ý: Các Địa Điểm Ẩm Thực & Khách Sạn Nổi Bật Khác Tại Tây Ninh -->
        <div class='bg-white p-5 border border-[#E0DDD8] shadow-sm space-y-4'>
          <div class='flex items-center justify-between border-b border-[#E0DDD8] pb-2.5'>
            <h4 class='text-xs sm:text-sm font-black text-[#161513] uppercase flex items-center gap-2'>
              <i class='fa-solid fa-compass text-[#C74634]'></i>
              <span>Khám Phá Thêm Các Quán Ngon &amp; Điểm Lưu Trú Khác Tại Tây Ninh</span>
            </h4>
            <button type='button' v-on:click='closeFoodDetailPage' class='text-xs font-bold text-[#C74634] hover:underline'>
              Xem tất cả
            </button>
          </div>

          <div class='grid grid-cols-1 sm:grid-cols-3 gap-4'>
            <div v-for='rec in defaultFoodAndHotelList.filter(f => f.id !== selectedFoodCard.id).slice(0, 3)' v-bind:key='rec.id' 
                 v-on:click='openFoodDetailPage(rec)'
                 class='p-2.5 border border-[#E0DDD8] bg-[#FAF9F8] hover:bg-white hover:border-[#C74634] cursor-pointer transition flex flex-col justify-between group shadow-sm'>
              <div class='relative h-32 w-full overflow-hidden mb-2'>
                <img v-bind:src='rec.image || NO_IMAGE_PLACEHOLDER' v-on:error='handleImgError' class='w-full h-full object-cover group-hover:scale-105 transition-transform duration-300' />
                <span class='absolute bottom-1.5 left-1.5 px-2 py-0.5 bg-black/80 text-white font-bold text-[10px]'>
                  {{ rec.price }}
                </span>
              </div>
              <div class='space-y-1'>
                <h5 class='font-bold text-xs text-[#161513] group-hover:text-[#C74634] transition line-clamp-1'>{{ rec.title }}</h5>
                <p class='text-[10px] text-slate-500 truncate flex items-center gap-1'>
                  <i class='fa-solid fa-location-dot text-[#C74634]'></i>
                  <span>{{ rec.subtitle || rec.location }}</span>
                </p>
              </div>
            </div>
          </div>
        </div>"""

new_rec_block = """        <!-- Khối Gợi Ý: Các Địa Điểm Ẩm Thực & Khách Sạn Nổi Bật Khác Tại Tây Ninh -->
        <div class='bg-white p-5 border border-[#E0DDD8] shadow-sm space-y-4'>
          <div class='flex items-center justify-between border-b border-[#E0DDD8] pb-2.5'>
            <h4 class='text-xs sm:text-sm font-black text-[#161513] uppercase flex items-center gap-2'>
              <i class='fa-solid fa-compass text-[#C74634]'></i>
              <span>{{ currentLang === "en" ? "Explore More Famous Food &amp; Accommodations in Tay Ninh" : currentLang === "ko" ? "타이닌의 다른 맛집 및 숙소 탐색" : currentLang === "zh" ? "探索更多西宁美食与住宿" : "Khám Phá Thêm Các Quán Ngon &amp; Điểm Lưu Trú Khác Tại Tây Ninh" }}</span>
            </h4>
            <button type='button' v-on:click='closeFoodDetailPage' class='text-xs font-bold text-[#C74634] hover:underline flex items-center gap-1'>
              <span>{{ currentLang === "en" ? "View all" : currentLang === "ko" ? "모두 보기" : currentLang === "zh" ? "查看全部" : "Xem tất cả" }}</span>
              <i class='fa-solid fa-arrow-right text-[10px]'></i>
            </button>
          </div>

          <div class='grid grid-cols-1 sm:grid-cols-3 gap-4'>
            <div v-for='rec in defaultFoodAndHotelList.filter(f => f.id !== selectedFoodCard.id).slice(0, 3)' v-bind:key='rec.id' 
                 v-on:click='openFoodDetailPage(rec)'
                 class='p-2.5 border border-[#E0DDD8] bg-[#FAF9F8] hover:bg-white hover:border-[#C74634] cursor-pointer transition flex flex-col justify-between group shadow-sm'>
              <div class='relative h-32 w-full overflow-hidden mb-2'>
                <img v-bind:src='rec.image || NO_IMAGE_PLACEHOLDER' v-on:error='handleImgError' class='w-full h-full object-cover group-hover:scale-105 transition-transform duration-300' />
                <span class='absolute bottom-1.5 left-1.5 px-2 py-0.5 bg-black/80 text-white font-bold text-[10px]'>
                  {{ getPostPrice(rec) }}
                </span>
              </div>
              <div class='space-y-1'>
                <h5 class='font-bold text-xs text-[#161513] group-hover:text-[#C74634] transition line-clamp-1'>{{ getPostTitle(rec) }}</h5>
                <p class='text-[10px] text-slate-500 truncate flex items-center gap-1'>
                  <i class='fa-solid fa-location-dot text-[#C74634]'></i>
                  <span>{{ getPostLocation(rec) }}</span>
                </p>
              </div>
            </div>
          </div>
        </div>"""

assert old_rec_block in content, 'Cannot find old_rec_block'
content = content.replace(old_rec_block, new_rec_block, 1)

with open('/data/projects/blogger/theme.xml', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated successfully!')
