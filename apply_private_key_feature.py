with open('/data/projects/blogger/theme.xml', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Thêm State vào phần khai báo Private Chat (dòng ~6083)
old_state = """        // CHAT PRIVATE 1-1 STATE
        const showPrivateChat = ref(false);
        const activeChatPartner = ref(null);
        const privateMessages = ref([]);
        const privateMessageInput = ref('');
        let privateChatUnsubscribe = null;"""

new_state = """        // CHAT PRIVATE 1-1 STATE
        const showPrivateChat = ref(false);
        const activeChatPartner = ref(null);
        const privateMessages = ref([]);
        const privateMessageInput = ref('');
        let privateChatUnsubscribe = null;

        // TÍNH NĂNG MÃ KHÓA BẢO MẬT PHÒNG CHAT PRIVATE (ROOM KEY & PASSCODE)
        const currentRoomKey = ref('');
        const isPrivateRoomUnlocked = ref(false);
        const enteredRoomKey = ref('');
        const roomKeyInputError = ref('');"""

assert old_state in content, 'Cannot find old_state'
content = content.replace(old_state, new_state, 1)

# 2. Thêm logic Room Key & cập nhật openPrivateChat, sendPrivateMessage
old_logic = """        const getChatId = (userA, userB) => {
          const k1 = getUserChatKey(userA).replace(/[^a-zA-Z0-9]/g, '_');
          const k2 = getUserChatKey(userB).replace(/[^a-zA-Z0-9]/g, '_');
          if (!k1 || !k2) return 'general_chat';
          return [k1, k2].sort().join('___chat___');
        };

        let allFirebaseMessages = [];

        const loadPrivateMessagesForChat = (chatId) => {
          const sender = (currentUser.value && currentUser.value.uid) ? currentUser.value : guestUser.value;
          const myEmail = (sender.email || sender.uid || '').toLowerCase().trim();
          
          const filtered = allFirebaseMessages.filter(m => m.chatId === chatId);
          privateMessages.value = filtered.map(m => ({
            ...m,
            isMe: (myEmail && m.senderEmail && m.senderEmail.toLowerCase() === myEmail) || (sender.uid && m.senderId === sender.uid)
          }));
          setTimeout(() => {
            const box = document.getElementById('privateChatBox');
            if (box) box.scrollTop = box.scrollHeight;
          }, 80);
        };

        const openPrivateChat = (target) => {
          if (!target) return;

          const sender = (currentUser.value && currentUser.value.uid) ? currentUser.value : guestUser.value;

          // Hỗ trợ mọi loại target: card bài đăng, friend, user profile, notification
          const partnerEmail = (target.email || target.authorEmail || target.senderEmail || (target.rawTarget ? target.rawTarget.authorEmail : '') || '').toLowerCase().trim();
          const partnerName = target.name || target.displayName || target.authorName || target.author || target.senderName || (partnerEmail ? partnerEmail.split('@')[0] : 'Người đăng');
          const partnerAvatar = target.avatar || target.photoURL || target.authorAvatar || target.senderAvatar || 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=80&q=80';
          const partnerId = partnerEmail || target.userId || target.uid || (target.id ? ('user_' + target.id) : 'partner_' + Date.now());

          const myEmail = (sender.email || sender.uid || '').toLowerCase().trim();
          if (myEmail && partnerEmail && myEmail === partnerEmail) {
            showToast('Đây là bài viết hoặc tài khoản của chính bạn. Không thể tự chat với mình!', 'info');
            return;
          }

          activeChatPartner.value = {
            id: partnerId,
            name: partnerName,
            email: partnerEmail,
            avatar: partnerAvatar
          };

          const chatId = getChatId(sender, activeChatPartner.value);
          loadPrivateMessagesForChat(chatId);

          showPrivateChat.value = true;
          if (showFriendsModal.value) showFriendsModal.value = false;
          if (showNotificationDropdown.value) showNotificationDropdown.value = false;
        };

        const sendPrivateMessage = async () => {
          const text = privateMessageInput.value.trim();
          if (!text || !activeChatPartner.value) return;

          const sender = (currentUser.value && currentUser.value.uid) ? currentUser.value : guestUser.value;
          const myEmail = (sender.email || sender.uid || '').toLowerCase().trim();
          const partnerEmail = (activeChatPartner.value.email || '').toLowerCase().trim();
          const chatId = getChatId(sender, activeChatPartner.value);

          const newMsg = {
            chatId: chatId,
            type: 'private',
            senderId: sender.uid || '',
            senderName: sender.displayName || 'Thành viên Tây Ninh',
            senderEmail: myEmail,
            senderAvatar: sender.photoURL || '',
            receiverId: activeChatPartner.value.id || '',
            receiverEmail: partnerEmail,
            receiverName: activeChatPartner.value.name,
            text: text,
            createdAt: new Date().toISOString()
          };"""

new_logic = """        const getChatId = (userA, userB) => {
          const k1 = getUserChatKey(userA).replace(/[^a-zA-Z0-9]/g, '_');
          const k2 = getUserChatKey(userB).replace(/[^a-zA-Z0-9]/g, '_');
          if (!k1 || !k2) return 'general_chat';
          return [k1, k2].sort().join('___chat___');
        };

        // SINH MÃ KEY MẶC ĐỊNH BẢO MẬT CHO MỖI PHÒNG CHAT (ROOM KEY)
        const getRoomDefaultKey = (chatId) => {
          if (!chatId) return 'TN-6888';
          let hash = 0;
          for (let i = 0; i < chatId.length; i++) {
            hash = ((hash << 5) - hash) + chatId.charCodeAt(i);
            hash |= 0;
          }
          const num = Math.abs(hash) % 90000 + 10000;
          return 'TN-' + num;
        };

        const getRoomKeyForChat = (chatId) => {
          // 1. Kiểm tra nếu trong tin nhắn của phòng có roomKey do người gửi lưu
          const msgWithKey = allFirebaseMessages.slice().reverse().find(m => m.chatId === chatId && m.roomKey);
          if (msgWithKey && msgWithKey.roomKey) {
            return msgWithKey.roomKey;
          }
          // 2. Kiểm tra nếu có custom key lưu tại localStorage
          const localCustomKey = safeGetStorage('tnhub_room_key_' + chatId, null);
          if (localCustomKey) return localCustomKey;
          // 3. Mặc định sinh mã theo chatId
          return getRoomDefaultKey(chatId);
        };

        const copyRoomKey = () => {
          if (!currentRoomKey.value) return;
          const partnerName = (activeChatPartner.value && activeChatPartner.value.name) ? activeChatPartner.value.name : 'bạn';
          const textToShare = '[TNHub Private Chat] Mã khóa phòng trò chuyện riêng tư của tôi với ' + partnerName + ' là: ' + currentRoomKey.value + '. Bạn hãy mở TNHub, vào phòng chat và nhập mã này để mở khóa trò chuyện nhé!';
          try {
            if (navigator && navigator.clipboard && navigator.clipboard.writeText) {
              navigator.clipboard.writeText(textToShare);
            } else {
              const ta = document.createElement('textarea');
              ta.value = textToShare;
              document.body.appendChild(ta);
              ta.select();
              document.execCommand('copy');
              document.body.removeChild(ta);
            }
            showToast('Đã sao chép mã Key: ' + currentRoomKey.value + '. Hãy gửi cho ' + partnerName + '!', 'success', 'Sao Chép Mã Key');
          } catch(e) {
            showToast('Mã Key phòng: ' + currentRoomKey.value, 'info');
          }
        };

        const unlockPrivateRoom = () => {
          const input = (enteredRoomKey.value || '').trim().toUpperCase();
          const target = (currentRoomKey.value || '').trim().toUpperCase();
          if (!input) {
            roomKeyInputError.value = 'Vui lòng nhập mã Key của phòng chat!';
            return;
          }
          const cleanInput = input.replace(/[^A-Z0-9]/g, '');
          const cleanTarget = target.replace(/[^A-Z0-9]/g, '');

          if (cleanInput === cleanTarget) {
            isPrivateRoomUnlocked.value = true;
            roomKeyInputError.value = '';
            const sender = (currentUser.value && currentUser.value.uid) ? currentUser.value : guestUser.value;
            const chatId = getChatId(sender, activeChatPartner.value);
            safeSetStorage('tnhub_unlocked_' + chatId, 'unlocked');
            showToast('Mở khóa phòng chat riêng tư thành công!', 'success', 'Mở Khóa Thành Công');
            setTimeout(() => {
              const box = document.getElementById('privateChatBox');
              if (box) box.scrollTop = box.scrollHeight;
            }, 100);
          } else {
            roomKeyInputError.value = 'Mã Key không chính xác! Vui lòng hỏi lại người gửi để nhận đúng mã.';
            showToast('Mã Key không chính xác. Vui lòng thử lại!', 'error', 'Sai Mã Khóa');
          }
        };

        const relockPrivateRoom = () => {
          if (!activeChatPartner.value) return;
          const sender = (currentUser.value && currentUser.value.uid) ? currentUser.value : guestUser.value;
          const chatId = getChatId(sender, activeChatPartner.value);
          safeSetStorage('tnhub_unlocked_' + chatId, 'locked');
          isPrivateRoomUnlocked.value = false;
          enteredRoomKey.value = '';
          roomKeyInputError.value = '';
          showToast('Đã khóa lại cuộc trò chuyện riêng tư này.', 'info', 'Đã Khóa');
        };

        let allFirebaseMessages = [];

        const loadPrivateMessagesForChat = (chatId) => {
          const sender = (currentUser.value && currentUser.value.uid) ? currentUser.value : guestUser.value;
          const myEmail = (sender.email || sender.uid || '').toLowerCase().trim();
          
          const filtered = allFirebaseMessages.filter(m => m.chatId === chatId);
          privateMessages.value = filtered.map(m => ({
            ...m,
            isMe: (myEmail && m.senderEmail && m.senderEmail.toLowerCase() === myEmail) || (sender.uid && m.senderId === sender.uid)
          }));
          setTimeout(() => {
            const box = document.getElementById('privateChatBox');
            if (box) box.scrollTop = box.scrollHeight;
          }, 80);
        };

        const openPrivateChat = (target) => {
          if (!target) return;

          const sender = (currentUser.value && currentUser.value.uid) ? currentUser.value : guestUser.value;

          // Hỗ trợ mọi loại target: card bài đăng, friend, user profile, notification
          const partnerEmail = (target.email || target.authorEmail || target.senderEmail || (target.rawTarget ? target.rawTarget.authorEmail : '') || '').toLowerCase().trim();
          const partnerName = target.name || target.displayName || target.authorName || target.author || target.senderName || (partnerEmail ? partnerEmail.split('@')[0] : 'Người đăng');
          const partnerAvatar = target.avatar || target.photoURL || target.authorAvatar || target.senderAvatar || 'https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=80&q=80';
          const partnerId = partnerEmail || target.userId || target.uid || (target.id ? ('user_' + target.id) : 'partner_' + Date.now());

          const myEmail = (sender.email || sender.uid || '').toLowerCase().trim();
          if (myEmail && partnerEmail && myEmail === partnerEmail) {
            showToast('Đây là bài viết hoặc tài khoản của chính bạn. Không thể tự chat với mình!', 'info');
            return;
          }

          activeChatPartner.value = {
            id: partnerId,
            name: partnerName,
            email: partnerEmail,
            avatar: partnerAvatar
          };

          const chatId = getChatId(sender, activeChatPartner.value);

          // 1. Lấy mã Key phòng
          currentRoomKey.value = getRoomKeyForChat(chatId);

          // 2. Kiểm tra quyền mở khóa
          const unlockedStatus = safeGetStorage('tnhub_unlocked_' + chatId, '');
          const myKey = getUserChatKey(sender);
          const chatMsgs = allFirebaseMessages.filter(m => m.chatId === chatId);
          const sentByMe = chatMsgs.filter(m => getUserChatKey(m.senderEmail || m.senderId) === myKey);

          if (unlockedStatus === 'unlocked') {
            isPrivateRoomUnlocked.value = true;
          } else if (unlockedStatus === 'locked') {
            isPrivateRoomUnlocked.value = false;
          } else if (chatMsgs.length === 0 || sentByMe.length > 0) {
            // Là người khởi tạo phòng hoặc người đã từng nhắn tin trong phòng này -> Mở khóa sẵn
            isPrivateRoomUnlocked.value = true;
            safeSetStorage('tnhub_unlocked_' + chatId, 'unlocked');
          } else {
            // Là người nhận tin nhắn từ đối phương và chưa từng mở khóa -> Yêu cầu nhập Key
            isPrivateRoomUnlocked.value = false;
          }

          enteredRoomKey.value = '';
          roomKeyInputError.value = '';

          loadPrivateMessagesForChat(chatId);

          showPrivateChat.value = true;
          if (showFriendsModal.value) showFriendsModal.value = false;
          if (showNotificationDropdown.value) showNotificationDropdown.value = false;
        };

        const sendPrivateMessage = async () => {
          if (!isPrivateRoomUnlocked.value) {
            showToast('Phòng chat đang bị khóa. Vui lòng nhập mã Key để mở khóa trước khi gửi tin nhắn!', 'error');
            return;
          }
          const text = privateMessageInput.value.trim();
          if (!text || !activeChatPartner.value) return;

          const sender = (currentUser.value && currentUser.value.uid) ? currentUser.value : guestUser.value;
          const myEmail = (sender.email || sender.uid || '').toLowerCase().trim();
          const partnerEmail = (activeChatPartner.value.email || '').toLowerCase().trim();
          const chatId = getChatId(sender, activeChatPartner.value);

          const newMsg = {
            chatId: chatId,
            type: 'private',
            roomKey: currentRoomKey.value,
            senderId: sender.uid || '',
            senderName: sender.displayName || 'Thành viên Tây Ninh',
            senderEmail: myEmail,
            senderAvatar: sender.photoURL || '',
            receiverId: activeChatPartner.value.id || '',
            receiverEmail: partnerEmail,
            receiverName: activeChatPartner.value.name,
            text: text,
            createdAt: new Date().toISOString()
          };"""

assert old_logic in content, 'Cannot find old_logic'
content = content.replace(old_logic, new_logic, 1)

# 3. Cập nhật HTML Modal showPrivateChat
old_modal = """    <!-- 12. MODAL CHAT PRIVATE 1-1 REALTIME (MESSENGER DIALOG) -->
    <div v-if='showPrivateChat &amp;&amp; activeChatPartner' v-cloak='true' style='display: none;' v-bind:style='showPrivateChat ? "display: flex !important;" : "display: none !important;"' class='fixed inset-0 z-50 flex items-end sm:items-center justify-center sm:justify-end sm:p-6 bg-black/40 backdrop-blur-xs'>
      <div class='bg-white border border-[#E0DDD8] w-full sm:max-w-sm sm:h-[500px] h-[85vh] flex flex-col shadow-2xl relative text-xs'>
        <!-- Chat Header -->
        <div class='px-4 py-3 bg-[#161513] text-white flex items-center justify-between shrink-0'>
          <div class='flex items-center gap-2.5 min-w-0'>
            <div class='relative shrink-0'>
              <img v-bind:src='activeChatPartner.avatar || "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&amp;fit=crop&amp;w=80&amp;q=80"' 
                   class='w-8 h-8 object-cover border border-white/20' />
              <span class='absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 bg-emerald-500 border-2 border-[#161513] rounded-full'></span>
            </div>
            <div class='min-w-0'>
              <h4 class='font-bold text-xs truncate flex items-center gap-1.5'>
                <span>{{ activeChatPartner.name }}</span>
              </h4>
              <p class='text-[10px] text-emerald-400 flex items-center gap-1'>
                <span class='w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse'></span>
                <span>Trực tuyến Tây Ninh</span>
              </p>
            </div>
          </div>
          <div class='flex items-center gap-1'>
            <button v-on:click='closePrivateChat' class='w-7 h-7 flex items-center justify-center text-slate-400 hover:text-white transition'>
              <i class='fa-solid fa-xmark text-sm'></i>
            </button>
          </div>
        </div>

        <!-- Chat Notification Notice -->
        <div class='p-2 bg-amber-50 border-b border-amber-200 text-[10px] text-amber-800 flex items-center gap-1.5 px-3'>
          <i class='fa-solid fa-shield-halved text-amber-600'></i>
          <span>Cuộc trò chuyện riêng tư 1-1 giữa bạn và {{ activeChatPartner.name }}.</span>
        </div>

        <!-- Chat Messages Container -->
        <div id='privateChatBox' class='flex-1 overflow-y-auto p-3 space-y-2.5 bg-[#FAF9F8]'>
          <div v-if='privateMessages.length === 0' class='text-center py-12 text-slate-400 space-y-2'>
            <div class='w-10 h-10 mx-auto rounded-full bg-slate-100 flex items-center justify-center text-slate-400 text-lg'>
              <i class='fa-regular fa-comment-dots'></i>
            </div>
            <p class='text-xs font-semibold text-slate-600'>Chưa có tin nhắn riêng nào.</p>
            <p class='text-[10px] text-slate-400'>Hãy gửi lời chào đầu tiên đến {{ activeChatPartner.name }}!</p>
          </div>

          <div v-for='msg in privateMessages' v-bind:key='msg.id' 
               v-bind:class='msg.isMe ? "justify-end" : "justify-start"' 
               class='flex items-end gap-2'>
            <!-- Avatar đối phương nếu tin nhắn của họ -->
            <img v-if='!msg.isMe' v-bind:src='activeChatPartner.avatar || "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&amp;fit=crop&amp;w=80&amp;q=80"' 
                 class='w-6 h-6 object-cover border border-[#E0DDD8] shrink-0 mb-1' />

            <div v-bind:class='msg.isMe ? "bg-[#C74634] text-white" : "bg-white text-slate-800 border border-[#E0DDD8]"' 
                 class='max-w-[75%] px-3 py-2 shadow-xs leading-relaxed text-xs break-words'>
              <p>{{ msg.text }}</p>
              <span v-bind:class='msg.isMe ? "text-white/70" : "text-slate-400"' class='block text-[9px] mt-1 text-right'>
                {{ formatTime(msg.createdAt) }}
              </span>
            </div>
          </div>
        </div>

        <!-- Chat Input Footer -->
        <div class='p-2.5 bg-white border-t border-[#E0DDD8] flex items-center gap-1.5'>
          <input type='text' v-model='privateMessageInput' 
                 v-on:keydown.enter.prevent='sendPrivateMessage' 
                 placeholder='Nhập tin nhắn riêng...' 
                 class='flex-1 px-3 py-2 bg-[#F1EFED] border border-[#E0DDD8] text-xs outline-none focus:border-[#C74634] focus:bg-white transition' />
          <button type='button' v-on:click='sendPrivateMessage' class='px-3.5 py-2 bg-[#C74634] hover:bg-[#B13C2C] text-white font-bold text-xs transition flex items-center gap-1 shadow-sm'>
            <i class='fa-solid fa-paper-plane'></i>
            <span>Gửi</span>
          </button>
        </div>
      </div>
    </div>"""

new_modal = """    <!-- 12. MODAL CHAT PRIVATE 1-1 REALTIME (MESSENGER DIALOG VỚI MÃ KEY BẢO MẬT) -->
    <div v-if='showPrivateChat &amp;&amp; activeChatPartner' v-cloak='true' style='display: none;' v-bind:style='showPrivateChat ? "display: flex !important;" : "display: none !important;"' class='fixed inset-0 z-50 flex items-end sm:items-center justify-center sm:justify-end sm:p-6 bg-black/40 backdrop-blur-xs'>
      <div class='bg-white border border-[#E0DDD8] w-full sm:max-w-sm sm:h-[520px] h-[85vh] flex flex-col shadow-2xl relative text-xs'>
        <!-- Chat Header -->
        <div class='px-4 py-3 bg-[#161513] text-white flex items-center justify-between shrink-0'>
          <div class='flex items-center gap-2.5 min-w-0'>
            <div class='relative shrink-0'>
              <img v-bind:src='activeChatPartner.avatar || "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&amp;fit=crop&amp;w=80&amp;q=80"' 
                   class='w-8 h-8 object-cover border border-white/20' />
              <span class='absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 bg-emerald-500 border-2 border-[#161513] rounded-full'></span>
            </div>
            <div class='min-w-0'>
              <h4 class='font-bold text-xs truncate flex items-center gap-1.5'>
                <span>{{ activeChatPartner.name }}</span>
              </h4>
              <p class='text-[10px] text-emerald-400 flex items-center gap-1'>
                <span class='w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse'></span>
                <span>Trực tuyến Tây Ninh</span>
              </p>
            </div>
          </div>
          <div class='flex items-center gap-1.5'>
            <!-- Nút Mã Key Phòng (Sao chép gửi cho người nhận) -->
            <button type='button' v-on:click='copyRoomKey' 
                    class='px-2 py-1 bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 border border-amber-500/40 font-mono font-bold text-[10px] flex items-center gap-1 transition' 
                    title='Mã Key phòng chat (nhấn để sao chép gửi cho người nhận)'>
              <i class='fa-solid fa-key text-[9px]'></i>
              <span>{{ currentRoomKey }}</span>
              <i class='fa-regular fa-copy text-[9px] ml-0.5 opacity-80'></i>
            </button>

            <!-- Nút Khóa lại phòng nếu đã mở khóa -->
            <button v-if='isPrivateRoomUnlocked' type='button' v-on:click='relockPrivateRoom' 
                    class='w-7 h-7 flex items-center justify-center text-slate-400 hover:text-amber-400 hover:bg-white/10 transition' 
                    title='Khóa lại phòng chat này'>
              <i class='fa-solid fa-lock text-xs'></i>
            </button>

            <!-- Nút Đóng -->
            <button v-on:click='closePrivateChat' class='w-7 h-7 flex items-center justify-center text-slate-400 hover:text-white hover:bg-white/10 transition'>
              <i class='fa-solid fa-xmark text-sm'></i>
            </button>
          </div>
        </div>

        <!-- Chat Notification Notice: Trạng thái Khóa / Mở Khóa -->
        <div v-if='isPrivateRoomUnlocked' class='p-2 bg-amber-50 border-b border-amber-200 text-[10px] text-amber-900 flex items-center justify-between px-3'>
          <div class='flex items-center gap-1.5 truncate'>
            <i class='fa-solid fa-shield-halved text-amber-600 shrink-0'></i>
            <span class='truncate'>Mã Key phòng: <strong class='font-mono text-amber-800'>{{ currentRoomKey }}</strong></span>
          </div>
          <button type='button' v-on:click='copyRoomKey' class='text-[10px] font-bold text-[#C74634] hover:underline flex items-center gap-1 shrink-0'>
            <i class='fa-regular fa-copy'></i> Gửi Key
          </button>
        </div>
        <div v-else='true' class='p-2 bg-rose-50 border-b border-rose-200 text-[10px] text-rose-800 flex items-center gap-1.5 px-3 font-semibold'>
          <i class='fa-solid fa-lock text-rose-600 shrink-0'></i>
          <span>Phòng đang khóa. Cần nhập đúng mã Key để xem &amp; nhắn tin.</span>
        </div>

        <!-- MÀN HÌNH KHÓA: YÊU CẦU NGƯỜI NHẬN NHẬP KEY NẾU CHƯA MỞ KHÓA -->
        <div v-if='!isPrivateRoomUnlocked' class='flex-1 flex flex-col items-center justify-center p-6 bg-[#FAF9F8] text-center space-y-4'>
          <div class='w-14 h-14 rounded-full bg-rose-100 border border-rose-300 flex items-center justify-center text-[#C74634] text-2xl shadow-sm'>
            <i class='fa-solid fa-lock'></i>
          </div>
          <div class='space-y-1.5 max-w-xs'>
            <h4 class='text-sm font-bold text-[#161513] uppercase tracking-wide'>Phòng Chat Được Bảo Vệ Bằng Key</h4>
            <p class='text-xs text-slate-600 leading-relaxed'>
              Cuộc trò chuyện với <strong>{{ activeChatPartner.name }}</strong> yêu cầu <strong>Mã Khóa Bảo Mật (Room Key)</strong>.
            </p>
            <p class='text-[11px] text-slate-500'>
              Vui lòng liên hệ người gửi để nhận mã Key và nhập vào bên dưới để mở khóa cuộc trò chuyện:
            </p>
          </div>

          <!-- Form Nhập Key -->
          <div class='w-full max-w-xs space-y-2.5'>
            <div class='relative'>
              <input type='text' v-model='enteredRoomKey' v-on:keydown.enter='unlockPrivateRoom' 
                     placeholder='Nhập mã Key (ví dụ: TN-84920)...' 
                     class='w-full px-3.5 py-2.5 bg-white border text-center font-mono font-bold text-sm tracking-widest text-[#161513] outline-none shadow-inner uppercase' 
                     v-bind:class='roomKeyInputError ? "border-rose-500 ring-1 ring-rose-400" : "border-[#E0DDD8] focus:border-[#C74634]"' />
            </div>
            <p v-if='roomKeyInputError' class='text-[11px] text-rose-600 font-bold flex items-center justify-center gap-1'>
              <i class='fa-solid fa-circle-exclamation'></i> {{ roomKeyInputError }}
            </p>

            <button type='button' v-on:click='unlockPrivateRoom' 
                    class='w-full py-2.5 bg-[#C74634] hover:bg-[#B13C2C] text-white font-bold text-xs uppercase tracking-wider shadow-sm transition flex items-center justify-center gap-2'>
              <i class='fa-solid fa-key text-amber-300'></i>
              <span>Mở Khóa Cuộc Trò Chuyện</span>
            </button>
          </div>

          <div class='pt-2 border-t border-[#E0DDD8] w-full max-w-xs text-[10px] text-slate-400 flex items-center justify-center gap-1.5'>
            <i class='fa-solid fa-shield-halved text-emerald-600'></i>
            <span>Bảo mật 1-1 riêng tư TNHub Private</span>
          </div>
        </div>

        <!-- Chat Messages Container (Chỉ hiển thị khi ĐÃ MỞ KHÓA) -->
        <div v-else='true' id='privateChatBox' class='flex-1 overflow-y-auto p-3 space-y-2.5 bg-[#FAF9F8]'>
          <div v-if='privateMessages.length === 0' class='text-center py-12 text-slate-400 space-y-2'>
            <div class='w-10 h-10 mx-auto rounded-full bg-slate-100 flex items-center justify-center text-slate-400 text-lg'>
              <i class='fa-regular fa-comment-dots'></i>
            </div>
            <p class='text-xs font-semibold text-slate-600'>Chưa có tin nhắn riêng nào.</p>
            <p class='text-[10px] text-slate-400'>Hãy gửi lời chào đầu tiên đến {{ activeChatPartner.name }}!</p>
          </div>

          <div v-for='msg in privateMessages' v-bind:key='msg.id' 
               v-bind:class='msg.isMe ? "justify-end" : "justify-start"' 
               class='flex items-end gap-2'>
            <!-- Avatar đối phương nếu tin nhắn của họ -->
            <img v-if='!msg.isMe' v-bind:src='activeChatPartner.avatar || "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&amp;fit=crop&amp;w=80&amp;q=80"' 
                 class='w-6 h-6 object-cover border border-[#E0DDD8] shrink-0 mb-1' />

            <div v-bind:class='msg.isMe ? "bg-[#C74634] text-white" : "bg-white text-slate-800 border border-[#E0DDD8]"' 
                 class='max-w-[75%] px-3 py-2 shadow-xs leading-relaxed text-xs break-words'>
              <p>{{ msg.text }}</p>
              <span v-bind:class='msg.isMe ? "text-white/70" : "text-slate-400"' class='block text-[9px] mt-1 text-right'>
                {{ formatTime(msg.createdAt) }}
              </span>
            </div>
          </div>
        </div>

        <!-- Chat Input Footer -->
        <div v-if='isPrivateRoomUnlocked' class='p-2.5 bg-white border-t border-[#E0DDD8] flex items-center gap-1.5'>
          <input type='text' v-model='privateMessageInput' 
                 v-on:keydown.enter.prevent='sendPrivateMessage' 
                 placeholder='Nhập tin nhắn riêng...' 
                 class='flex-1 px-3 py-2 bg-[#F1EFED] border border-[#E0DDD8] text-xs outline-none focus:border-[#C74634] focus:bg-white transition' />
          <button type='button' v-on:click='sendPrivateMessage' class='px-3.5 py-2 bg-[#C74634] hover:bg-[#B13C2C] text-white font-bold text-xs transition flex items-center gap-1 shadow-sm'>
            <i class='fa-solid fa-paper-plane'></i>
            <span>Gửi</span>
          </button>
        </div>
      </div>
    </div>"""

assert old_modal in content, 'Cannot find old_modal'
content = content.replace(old_modal, new_modal, 1)

# 4. Thêm các biến trả về trong setup() return { ... }
old_return = """          openPrivateChat,
          sendPrivateMessage,
          closePrivateChat,"""

new_return = """          openPrivateChat,
          sendPrivateMessage,
          closePrivateChat,
          currentRoomKey,
          isPrivateRoomUnlocked,
          enteredRoomKey,
          roomKeyInputError,
          copyRoomKey,
          unlockPrivateRoom,
          relockPrivateRoom,"""

assert old_return in content, 'Cannot find old_return'
content = content.replace(old_return, new_return, 1)

with open('/data/projects/blogger/theme.xml', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated Private Chat Key feature successfully!')
