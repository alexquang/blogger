import re
import base64

# Đọc file metaverse_decompiled.html
with open('/data/projects/blogger/metaverse_decompiled.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Đổi theme mặc định sang 'light' trong DEFAULT_GALLERY_STATE
content = content.replace('theme: "dark", // \'dark\' or \'light\'', 'theme: "light", // \'dark\' or \'light\'')
content = content.replace("theme: 'dark'", "theme: 'light'")

# 2. Thay đổi phần khởi tạo Scene, Background, Fog, Lighting và Floor thành Luxury Modern Gallery sáng rực rỡ
old_scene_setup = """    const scene = new THREE.Scene();
    scene.background = new THREE.Color(galleryState.theme === 'light' ? 0xf4f4f7 : 0x090a0f);
    scene.fog = new THREE.Fog(galleryState.theme === 'light' ? 0xeaeaf0 : 0x090a0f, 28, 75);

    const camera = new THREE.PerspectiveCamera(65, window.innerWidth / window.innerHeight, 0.1, 150);
    camera.position.set(0, 1.7, 13); // Eye level walk start
    camera.lookAt(0, 1.8, 0);

    const renderer = new THREE.WebGLRenderer({
      canvas: canvas,
      antialias: true,
      powerPreference: 'default',
      preserveDrawingBuffer: true
    });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.1;"""

new_scene_setup = """    const scene = new THREE.Scene();
    // Bầu trời Oncyber ban ngày trong xanh, sáng sủa, không còn màu đen u tối
    const skyColor = new THREE.Color(0xdcecf8);
    scene.background = skyColor;
    scene.fog = new THREE.FogExp2(0xe6f0fa, 0.012);

    const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 200);
    camera.position.set(0, 2.5, 14);
    camera.lookAt(0, 1.4, 0);

    const renderer = new THREE.WebGLRenderer({
      canvas: canvas,
      antialias: true,
      powerPreference: 'high-performance',
      preserveDrawingBuffer: false,
      alpha: true
    });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.25;

    // Chống mất WebGL context
    canvas.addEventListener('webglcontextlost', (e) => {
      e.preventDefault();
      console.warn('WebGL Context Lost captured. Preventing crash.');
    }, false);"""

assert old_scene_setup in content, 'Cannot find old_scene_setup'
content = content.replace(old_scene_setup, new_scene_setup, 1)

# 3. Nâng cấp Floor, Walls, Ceiling & Lighting sang Light Modern Luxury Oncyber
old_arch_setup = """    /* Procedural Floor Texture (Polished Museum Concrete) */
    function generateFloorTexture() {
      const fCanvas = document.createElement('canvas');
      fCanvas.width = 256;
      fCanvas.height = 256;
      const fCtx = fCanvas.getContext('2d', { willReadFrequently: true });
      fCtx.fillStyle = '#1c1e26';
      fCtx.fillRect(0, 0, 256, 256);

      // Subtle marble veining & grid
      fCtx.strokeStyle = 'rgba(255, 255, 255, 0.04)';
      fCtx.lineWidth = 1;
      fCtx.strokeRect(0, 0, 256, 256);

      for (let i = 0; i < 600; i++) {
        fCtx.fillStyle = `rgba(255, 255, 255, ${Math.random() * 0.03})`;
        fCtx.fillRect(Math.random() * 256, Math.random() * 256, 2, 2);
      }

      const tex = new THREE.CanvasTexture(fCanvas);
      tex.wrapS = THREE.RepeatWrapping;
      tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(12, 16);
      return tex;
    }

    const floorTexture = generateFloorTexture();

    // Floor Mesh
    const floorGeo = new THREE.PlaneGeometry(30, 42);
    const floorMat = new THREE.MeshStandardMaterial({
      map: floorTexture,
      roughness: 0.28,
      metalness: 0.35,
      color: galleryState.theme === 'light' ? 0xd8d7d4 : 0x2a2e3d
    });
    const floor = new THREE.Mesh(floorGeo, floorMat);
    floor.rotation.x = -Math.PI / 2;
    floor.position.y = 0;
    floor.receiveShadow = true;
    scene.add(floor);

    // Ceiling Mesh
    const ceilingGeo = new THREE.PlaneGeometry(30, 42);
    const ceilingMat = new THREE.MeshStandardMaterial({
      color: galleryState.theme === 'light' ? 0xffffff : 0x1b1d28,
      roughness: 0.8
    });
    const ceiling = new THREE.Mesh(ceilingGeo, ceilingMat);
    ceiling.rotation.x = Math.PI / 2;
    ceiling.position.y = 6.8;
    scene.add(ceiling);

    // Skylight luminous panels in ceiling
    const skylightGeo = new THREE.PlaneGeometry(6, 26);
    const skylightMat = new THREE.MeshBasicMaterial({
      color: galleryState.theme === 'light' ? 0xfffaed : 0xd6e8ff
    });
    const skylight = new THREE.Mesh(skylightGeo, skylightMat);
    skylight.rotation.x = Math.PI / 2;
    skylight.position.set(0, 6.78, 0);
    scene.add(skylight);

    // Wall Materials & Meshes
    const wallMat = new THREE.MeshStandardMaterial({
      color: galleryState.theme === 'light' ? 0xf0efe9 : 0x262938,
      roughness: 0.85,
      metalness: 0.05
    });"""

new_arch_setup = """    /* Procedural Floor Texture (Sàn Đá Cẩm Thạch Trắng Sang Trọng - White Carrara Marble) */
    function generateFloorTexture() {
      const fCanvas = document.createElement('canvas');
      fCanvas.width = 512;
      fCanvas.height = 512;
      const fCtx = fCanvas.getContext('2d', { willReadFrequently: true });
      fCtx.fillStyle = '#f0f2f5';
      fCtx.fillRect(0, 0, 512, 512);

      // Vân đá marble vàng kim và xám thanh lịch
      fCtx.strokeStyle = 'rgba(200, 205, 215, 0.45)';
      fCtx.lineWidth = 1.5;
      fCtx.strokeRect(0, 0, 512, 512);

      for (let i = 0; i < 40; i++) {
        fCtx.beginPath();
        fCtx.moveTo(Math.random() * 512, Math.random() * 512);
        fCtx.bezierCurveTo(Math.random() * 512, Math.random() * 512, Math.random() * 512, Math.random() * 512, Math.random() * 512, Math.random() * 512);
        fCtx.strokeStyle = `rgba(180, 185, 195, ${0.08 + Math.random() * 0.12})`;
        fCtx.lineWidth = 1 + Math.random() * 2.5;
        fCtx.stroke();
      }

      const tex = new THREE.CanvasTexture(fCanvas);
      tex.wrapS = THREE.RepeatWrapping;
      tex.wrapT = THREE.RepeatWrapping;
      tex.repeat.set(10, 14);
      return tex;
    }

    const floorTexture = generateFloorTexture();

    // Sàn đá cẩm thạch trắng phản chiếu ánh sáng
    const floorGeo = new THREE.PlaneGeometry(34, 46);
    const floorMat = new THREE.MeshStandardMaterial({
      map: floorTexture,
      roughness: 0.18,
      metalness: 0.25,
      color: 0xffffff
    });
    const floor = new THREE.Mesh(floorGeo, floorMat);
    floor.rotation.x = -Math.PI / 2;
    floor.position.y = 0;
    floor.receiveShadow = true;
    scene.add(floor);

    // Trần giếng trời đón ánh sáng tự nhiên
    const ceilingGeo = new THREE.PlaneGeometry(34, 46);
    const ceilingMat = new THREE.MeshStandardMaterial({
      color: 0xfafbfc,
      roughness: 0.7
    });
    const ceiling = new THREE.Mesh(ceilingGeo, ceilingMat);
    ceiling.rotation.x = Math.PI / 2;
    ceiling.position.y = 7.2;
    scene.add(ceiling);

    // Giếng trời kính rực rỡ (Skylight)
    const skylightGeo = new THREE.PlaneGeometry(8, 30);
    const skylightMat = new THREE.MeshBasicMaterial({
      color: 0xe6f4ff
    });
    const skylight = new THREE.Mesh(skylightGeo, skylightMat);
    skylight.rotation.x = Math.PI / 2;
    skylight.position.set(0, 7.18, 0);
    scene.add(skylight);

    // Tường bảo tàng màu trắng kem ngà hiện đại Minimalism
    const wallMat = new THREE.MeshStandardMaterial({
      color: 0xfdfdfd,
      roughness: 0.75,
      metalness: 0.02
    });"""

assert old_arch_setup in content, 'Cannot find old_arch_setup'
content = content.replace(old_arch_setup, new_arch_setup, 1)

# 4. Thay đổi hệ thống ánh sáng (Lighting) sáng rực rỡ, tự nhiên
old_lighting = """    /* Room Lighting */
    const ambientLight = new THREE.AmbientLight(
      galleryState.theme === 'light' ? 0xffffff : 0xa4b1cd,
      galleryState.theme === 'light' ? 1.4 : 1.35
    );
    scene.add(ambientLight);

    const sunLight = new THREE.DirectionalLight(0xfff7e6, galleryState.theme === 'light' ? 1.6 : 1.35);
    sunLight.position.set(6, 12, 6);
    sunLight.castShadow = true;
    sunLight.shadow.mapSize.width = 1024;
    sunLight.shadow.mapSize.height = 1024;
    sunLight.shadow.bias = -0.0001;
    sunLight.shadow.camera.near = 0.5;"""

new_lighting = """    /* Room Lighting - Hệ thống chiếu sáng ban ngày ngập tràn ánh sáng */
    const hemiLight = new THREE.HemisphereLight(0xffffff, 0xcbe3f8, 1.8);
    hemiLight.position.set(0, 20, 0);
    scene.add(hemiLight);

    const ambientLight = new THREE.AmbientLight(0xffffff, 1.3);
    scene.add(ambientLight);

    const sunLight = new THREE.DirectionalLight(0xfffaec, 2.2);
    sunLight.position.set(8, 16, 8);
    sunLight.castShadow = true;
    sunLight.shadow.mapSize.width = 1024;
    sunLight.shadow.mapSize.height = 1024;
    sunLight.shadow.bias = -0.0001;
    sunLight.shadow.camera.near = 0.5;"""

assert old_lighting in content, 'Cannot find old_lighting'
content = content.replace(old_lighting, new_lighting, 1)

# 5. Xây dựng ACTOR 3D NHÂN VẬT DI CHUYỂN (3D Third-Person Character Avatar)
actor_code = """
    /* ==========================================================================
       ACTOR 3D: NHÂN VẬT METAVERSE DI CHUYỂN SỐNG ĐỘNG (CHARACTER CONTROLLER)
       ========================================================================== */
    let isThirdPersonView = true;
    let cameraOrbitAngleY = 0;
    let cameraOrbitAngleX = 0.22;
    let isMouseDragging = false;
    let lastMousePos = { x: 0, y: 0 };

    // Hàm tạo 3D Text Nametag Sprite
    function createNametagSprite(nameText, isVip = false) {
      const nCanvas = document.createElement('canvas');
      nCanvas.width = 320;
      nCanvas.height = 80;
      const nCtx = nCanvas.getContext('2d');
      
      // Khung bo góc
      nCtx.fillStyle = 'rgba(15, 18, 26, 0.85)';
      nCtx.strokeStyle = isVip ? '#f59e0b' : '#38bdf8';
      nCtx.lineWidth = 4;
      nCtx.beginPath();
      nCtx.roundRect(10, 10, 300, 60, 16);
      nCtx.fill();
      nCtx.stroke();

      // Dấu chấm xanh online
      nCtx.fillStyle = '#10b981';
      nCtx.beginPath();
      nCtx.arc(36, 40, 8, 0, Math.PI * 2);
      nCtx.fill();

      // Chữ tên nhân vật
      nCtx.fillStyle = '#ffffff';
      nCtx.font = 'bold 24px "Plus Jakarta Sans", sans-serif';
      nCtx.fillText(nameText, 54, 48);

      const spTex = new THREE.CanvasTexture(nCanvas);
      const spriteMat = new THREE.SpriteMaterial({ map: spTex, transparent: true, depthTest: false });
      const sprite = new THREE.Sprite(spriteMat);
      sprite.scale.set(1.6, 0.4, 1);
      return sprite;
    }

    // Hàm tạo nhân vật 3D chi tiết (Humanoid Avatar)
    function buildCharacterMesh(avatarName, isPlayer = true, colorHex = 0xC74634) {
      const group = new THREE.Group();

      // 1. Thân áo Hoodie phong cách Metaverse
      const torsoMat = new THREE.MeshStandardMaterial({
        color: colorHex,
        roughness: 0.35,
        metalness: 0.2
      });
      const torso = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.65, 0.32), torsoMat);
      torso.position.y = 0.95;
      torso.castShadow = true;
      group.add(torso);

      // 2. Đầu & Kính VR Visor công nghệ cao
      const headMat = new THREE.MeshStandardMaterial({ color: 0xffdbac, roughness: 0.6 });
      const head = new THREE.Mesh(new THREE.SphereGeometry(0.18, 16, 16), headMat);
      head.position.y = 1.48;
      head.castShadow = true;
      group.add(head);

      // Kính VR Visor phát sáng neon
      const visorMat = new THREE.MeshStandardMaterial({
        color: isPlayer ? 0x25f4ee : 0xec4899,
        emissive: isPlayer ? 0x25f4ee : 0xec4899,
        emissiveIntensity: 0.9,
        roughness: 0.1
      });
      const visor = new THREE.Mesh(new THREE.BoxGeometry(0.26, 0.09, 0.14), visorMat);
      visor.position.set(0, 1.48, 0.14);
      group.add(visor);

      // Tai nghe Gaming / Headset
      const headsetMat = new THREE.MeshStandardMaterial({ color: 0x111318, metalness: 0.8, roughness: 0.2 });
      const headsetArch = new THREE.Mesh(new THREE.TorusGeometry(0.2, 0.03, 8, 16, Math.PI), headsetMat);
      headsetArch.rotation.x = -Math.PI / 2;
      headsetArch.position.set(0, 1.54, 0);
      group.add(headsetArch);

      // 3. Hai cánh tay (Vai & Cẳng tay)
      const armMat = new THREE.MeshStandardMaterial({ color: colorHex, roughness: 0.4 });
      
      const leftArmGroup = new THREE.Group();
      leftArmGroup.position.set(-0.35, 1.2, 0);
      const leftArm = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.065, 0.5, 12), armMat);
      leftArm.position.y = -0.22;
      leftArm.castShadow = true;
      leftArmGroup.add(leftArm);
      group.add(leftArmGroup);

      const rightArmGroup = new THREE.Group();
      rightArmGroup.position.set(0.35, 1.2, 0);
      const rightArm = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.065, 0.5, 12), armMat);
      rightArm.position.y = -0.22;
      rightArm.castShadow = true;
      rightArmGroup.add(rightArm);
      group.add(rightArmGroup);

      // 4. Hai chân & Đôi giày Sneaker
      const pantsMat = new THREE.MeshStandardMaterial({ color: 0x1a1e29, roughness: 0.6 });
      const shoeMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.3 });

      const leftLegGroup = new THREE.Group();
      leftLegGroup.position.set(-0.16, 0.62, 0);
      const leftLeg = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.08, 0.55, 12), pantsMat);
      leftLeg.position.y = -0.25;
      leftLeg.castShadow = true;
      leftLegGroup.add(leftLeg);
      const leftShoe = new THREE.Mesh(new THREE.BoxGeometry(0.13, 0.09, 0.22), shoeMat);
      leftShoe.position.set(0, -0.52, 0.04);
      leftShoe.castShadow = true;
      leftLegGroup.add(leftShoe);
      group.add(leftLegGroup);

      const rightLegGroup = new THREE.Group();
      rightLegGroup.position.set(0.16, 0.62, 0);
      const rightLeg = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.08, 0.55, 12), pantsMat);
      rightLeg.position.y = -0.25;
      rightLeg.castShadow = true;
      rightLegGroup.add(rightLeg);
      const rightShoe = new THREE.Mesh(new THREE.BoxGeometry(0.13, 0.09, 0.22), shoeMat);
      rightShoe.position.set(0, -0.52, 0.04);
      rightShoe.castShadow = true;
      rightLegGroup.add(rightShoe);
      group.add(rightLegGroup);

      // 5. Bóng tròn mềm dưới chân (Blob shadow)
      const shadowMat = new THREE.MeshBasicMaterial({ color: 0x000000, transparent: true, opacity: 0.3 });
      const blobShadow = new THREE.Mesh(new THREE.CircleGeometry(0.42, 16), shadowMat);
      blobShadow.rotation.x = -Math.PI / 2;
      blobShadow.position.y = 0.02;
      group.add(blobShadow);

      // 6. Bảng tên 3D Nametag
      const nametag = createNametagSprite(avatarName, isPlayer);
      nametag.position.y = 1.95;
      group.add(nametag);

      // Gắn references phục vụ animation
      group.userData = {
        leftLegGroup,
        rightLegGroup,
        leftArmGroup,
        rightArmGroup,
        walkCycle: 0,
        isMoving: false,
        torso
      };

      return group;
    }

    // Khởi tạo Actor chính của người dùng
    const playerActor = buildCharacterMesh('Quang Pham (Bạn)', true, 0xC74634);
    playerActor.position.set(0, 0, 11);
    scene.add(playerActor);

    // Khởi tạo 2 NPC khách tham quan cùng trong phòng triển lãm
    const npc1 = buildCharacterMesh('Lan Huong (Khách)', false, 0x2563eb);
    npc1.position.set(-6, 0, -4);
    npc1.rotation.y = Math.PI / 2;
    scene.add(npc1);

    const npc2 = buildCharacterMesh('Minh Tri (VIP)', false, 0x10b981);
    npc2.position.set(6, 0, 2);
    npc2.rotation.y = -Math.PI / 3;
    scene.add(npc2);

    // Xử lý kéo chuột xoay góc nhìn camera quanh Actor
    container.addEventListener('mousedown', (e) => {
      if (e.target.closest('#top-hud') || e.target.closest('#ui-nav-bar') || e.target.closest('#chat-drawer') || e.target.closest('#studio-drawer')) return;
      isMouseDragging = true;
      lastMousePos = { x: e.clientX, y: e.clientY };
    });

    window.addEventListener('mouseup', () => { isMouseDragging = false; });
    window.addEventListener('mousemove', (e) => {
      if (!isMouseDragging || !isThirdPersonView) return;
      const dx = e.clientX - lastMousePos.x;
      const dy = e.clientY - lastMousePos.y;
      lastMousePos = { x: e.clientX, y: e.clientY };

      cameraOrbitAngleY -= dx * 0.005;
      cameraOrbitAngleX = Math.max(-0.1, Math.min(0.9, cameraOrbitAngleX + dy * 0.004));
    });

    // Touch orbit xoay camera trên mobile
    const touchLookZone = document.getElementById('touch-look-zone');
    let lastTouchPos = null;
    if (touchLookZone) {
      touchLookZone.addEventListener('touchstart', (e) => {
        if (e.touches.length > 0) lastTouchPos = { x: e.touches[0].clientX, y: e.touches[0].clientY };
      }, { passive: true });
      touchLookZone.addEventListener('touchmove', (e) => {
        if (!lastTouchPos || e.touches.length === 0) return;
        const dx = e.touches[0].clientX - lastTouchPos.x;
        const dy = e.touches[0].clientY - lastTouchPos.y;
        lastTouchPos = { x: e.touches[0].clientX, y: e.touches[0].clientY };
        cameraOrbitAngleY -= dx * 0.006;
        cameraOrbitAngleX = Math.max(-0.1, Math.min(0.9, cameraOrbitAngleX + dy * 0.005));
      }, { passive: true });
      touchLookZone.addEventListener('touchend', () => { lastTouchPos = null; });
    }
"""

# Chèn actor_code vào trước phần texture slot
content = content.replace("    /* Procedural Floor Texture", actor_code + "\n    /* Procedural Floor Texture")

# 6. Cập nhật Animation Loop trong animate() để Actor di chuyển mượt mà và Camera bám theo Actor
old_fps_controls = """      // FPS Walk Movement Physics & Boundary Collision
      if (controls.isLocked || joystickActive) {
        // Friction / Damping
        moveVelocity.x -= moveVelocity.x * 10.0 * delta;
        moveVelocity.z -= moveVelocity.z * 10.0 * delta;

        moveDirection.z = Number(Boolean(keysPressed['KeyW'] || keysPressed['ArrowUp'])) - Number(Boolean(keysPressed['KeyS'] || keysPressed['ArrowDown']));
        moveDirection.x = Number(Boolean(keysPressed['KeyD'] || keysPressed['ArrowRight'])) - Number(Boolean(keysPressed['KeyA'] || keysPressed['ArrowLeft']));

        // Touch Joystick injection
        if (joystickActive) {
          moveDirection.z = -joystickDelta.y;
          moveDirection.x = joystickDelta.x;
        }

        moveDirection.normalize();

        const walkSpeed = 38.0;
        if (keysPressed['KeyW'] || keysPressed['KeyS'] || keysPressed['ArrowUp'] || keysPressed['ArrowDown'] || joystickActive) {
          moveVelocity.z -= moveDirection.z * walkSpeed * delta;
        }
        if (keysPressed['KeyA'] || keysPressed['KeyD'] || keysPressed['ArrowLeft'] || keysPressed['ArrowRight'] || joystickActive) {
          moveVelocity.x -= moveDirection.x * walkSpeed * delta;
        }

        controls.moveRight(-moveVelocity.x * delta);
        controls.moveForward(-moveVelocity.z * delta);

        // Lock eye level height
        camera.position.y = 1.7;

        // Gallery Perimeter Boundary Collision (Stay inside museum walls)
        const boundX = 13.8 - playerRadius;
        const boundZ = 19.8 - playerRadius;
        camera.position.x = Math.max(-boundX, Math.min(boundX, camera.position.x));
        camera.position.z = Math.max(-boundZ, Math.min(boundZ, camera.position.z));

        // Pedestal collision (Keep player outside central circle)
        const distFromCenter = Math.hypot(camera.position.x, camera.position.z);
        const minPedestalDist = 2.7 + playerRadius;
        if (distFromCenter < minPedestalDist) {
          const pushAngle = Math.atan2(camera.position.z, camera.position.x);
          camera.position.x = Math.cos(pushAngle) * minPedestalDist;
          camera.position.z = Math.sin(pushAngle) * minPedestalDist;
        }
      }"""

new_fps_controls = """      // DI CHUYỂN ACTOR 3D & CAMERA GÓC NHÌN THỨ 3 (THIRD-PERSON CHARACTER MOVEMENT)
      const isInputActive = Boolean(
        keysPressed['KeyW'] || keysPressed['KeyS'] || keysPressed['KeyA'] || keysPressed['KeyD'] ||
        keysPressed['ArrowUp'] || keysPressed['ArrowDown'] || keysPressed['ArrowLeft'] || keysPressed['ArrowRight'] ||
        joystickActive
      );

      // Tính vector di chuyển theo góc nhìn camera hiện tại
      let moveZ = Number(Boolean(keysPressed['KeyW'] || keysPressed['ArrowUp'])) - Number(Boolean(keysPressed['KeyS'] || keysPressed['ArrowDown']));
      let moveX = Number(Boolean(keysPressed['KeyD'] || keysPressed['ArrowRight'])) - Number(Boolean(keysPressed['KeyA'] || keysPressed['ArrowLeft']));

      if (joystickActive) {
        moveZ = -joystickDelta.y;
        moveX = joystickDelta.x;
      }

      if (isInputActive) {
        const inputVec = new THREE.Vector3(moveX, 0, -moveZ).normalize();
        // Áp dụng góc xoay camera
        inputVec.applyAxisAngle(new THREE.Vector3(0, 1, 0), cameraOrbitAngleY);

        const moveSpeed = 6.2 * delta;
        playerActor.position.x += inputVec.x * moveSpeed;
        playerActor.position.z += inputVec.z * moveSpeed;

        // Xoay mặt Actor theo hướng di chuyển mượt mà
        const targetRotY = Math.atan2(inputVec.x, inputVec.z);
        playerActor.rotation.y = THREE.MathUtils.lerp(playerActor.rotation.y, targetRotY, 0.2);

        // Animation bước chân & vung tay của Actor
        playerActor.userData.walkCycle += delta * 12;
        const cycle = playerActor.userData.walkCycle;
        playerActor.userData.leftLegGroup.rotation.x = Math.sin(cycle) * 0.7;
        playerActor.userData.rightLegGroup.rotation.x = -Math.sin(cycle) * 0.7;
        playerActor.userData.leftArmGroup.rotation.x = -Math.sin(cycle) * 0.6;
        playerActor.userData.rightArmGroup.rotation.x = Math.sin(cycle) * 0.6;
        playerActor.position.y = Math.abs(Math.sin(cycle * 2)) * 0.04;
      } else {
        // Đứng yên (Idle): đưa tay chân về thẳng và nhịp thở nhẹ
        playerActor.userData.leftLegGroup.rotation.x *= 0.85;
        playerActor.userData.rightLegGroup.rotation.x *= 0.85;
        playerActor.userData.leftArmGroup.rotation.x *= 0.85;
        playerActor.userData.rightArmGroup.rotation.x *= 0.85;
        playerActor.position.y = Math.sin(clock.getElapsedTime() * 2) * 0.015;
      }

      // Giới hạn Actor ở trong phòng trưng bày (Wall Collision)
      const boundX = 13.5;
      const boundZ = 19.5;
      playerActor.position.x = Math.max(-boundX, Math.min(boundX, playerActor.position.x));
      playerActor.position.z = Math.max(-boundZ, Math.min(boundZ, playerActor.position.z));

      // Tránh đi xuyên qua bục trung tâm
      const distCenter = Math.hypot(playerActor.position.x, playerActor.position.z);
      if (distCenter < 2.9) {
        const pushA = Math.atan2(playerActor.position.z, playerActor.position.x);
        playerActor.position.x = Math.cos(pushA) * 2.9;
        playerActor.position.z = Math.sin(pushA) * 2.9;
      }

      // Camera góc nhìn thứ 3 (Third-Person Follow Camera bám theo Actor)
      if (isThirdPersonView && !isTweeningCamera) {
        const camDistance = 3.6;
        const camHeight = 1.9 + cameraOrbitAngleX * 1.5;
        const targetCamX = playerActor.position.x + Math.sin(cameraOrbitAngleY) * camDistance;
        const targetCamZ = playerActor.position.z + Math.cos(cameraOrbitAngleY) * camDistance;
        const targetCamY = playerActor.position.y + camHeight;

        camera.position.lerp(new THREE.Vector3(targetCamX, targetCamY, targetCamZ), 0.12);
        camera.lookAt(playerActor.position.x, playerActor.position.y + 1.25, playerActor.position.z);
      }

      // Animation nhẹ nhàng cho các NPC khách tham quan
      const t = clock.getElapsedTime();
      npc1.position.y = Math.sin(t * 1.5) * 0.015;
      npc1.rotation.y = Math.PI / 2 + Math.sin(t * 0.8) * 0.2;
      npc2.position.y = Math.sin(t * 1.8 + 1) * 0.015;
      npc2.rotation.y = -Math.PI / 3 + Math.cos(t * 0.7) * 0.25;"""

assert old_fps_controls in content, 'Cannot find old_fps_controls'
content = content.replace(old_fps_controls, new_fps_controls, 1)

# Ghi file metaverse_decompiled.html đã cập nhật
with open('/data/projects/blogger/metaverse_decompiled.html', 'w', encoding='utf-8') as f:
    f.write(content)

# Mã hóa sang Base64
new_b64 = base64.b64encode(content.encode('utf-8')).decode('utf-8')

# Cập nhật vào theme.xml
with open('/data/projects/blogger/theme.xml', 'r', encoding='utf-8') as f:
    theme_xml = f.read()

# Thay thế METAVERSE_APP_B64
theme_xml = re.sub(r'const METAVERSE_APP_B64 = \"[^\"]+\";', f'const METAVERSE_APP_B64 = "{new_b64}";', theme_xml)

with open('/data/projects/blogger/theme.xml', 'w', encoding='utf-8') as f:
    f.write(theme_xml)

print('Updated Metaverse 3D with Bright Oncyber Gallery & Moving Character Actor successfully!')
