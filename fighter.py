import pygame

class Fighter():
  def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
    self.player = player # nomor pemain, 1 atau 2
    self.size = data[0] # ukuran gambar karakter
    self.image_scale = data[1] # skala gambar karakter
    self.offset = data[2] # jarak antara karakter dengan objek lain
    self.flip = flip # True jika karakter menghadap ke kiri, False jika menghadap ke kanan
    self.animation_list = self.load_images(sprite_sheet, animation_steps) # daftar animasi karakter
    self.action = 0 # tindakan saat ini, 0:idle #1:run #2:jump #3:attack1 #4: attack2 #5:hit #6:death
    self.frame_index = 0 # indeks frame saat ini dalam daftar animasi
    self.image = self.animation_list[self.action][self.frame_index] # gambar saat ini
    self.update_time = pygame.time.get_ticks() # waktu terakhir gambar diperbarui
    self.rect = pygame.Rect((x, y, 80, 180)) # kotak pemadat untuk deteksi tabrakan
    self.vel_y = 0 # kecepatan vertikal karakter
    self.running = False # True jika karakter sedang berlari, False jika tidak
    self.jump = False # True jika karakter sedang melompat, False jika tidak
    self.attacking = False # True jika karakter sedang menyerang, False jika tidak
    self.attack_type = 0 # jenis serangan saat ini, 0:tidak menyerang #1:serangan 1 #2:serangan 2
    self.attack_cooldown = 0 # waktu pendingin untuk serangan
    self.attack_sound = sound # efek suara serangan
    self.hit = False # True jika karakter terkena serangan, False jika tidak
    self.health = 100 # kesehatan karakter
    self.alive = True # True jika karakter masih hidup, False jika tidak


  def load_images(self, sprite_sheet, animation_steps):
    # Memuat gambar dari spritesheet
    animation_list = []  # Inisialisasi list kosong untuk menampung gambar animasi
    for y, animation in enumerate(animation_steps):
        temp_img_list = []  # Inisialisasi list kosong untuk menampung gambar animasi sementara
        for x in range(animation):
            # Memotong gambar dari spritesheet dengan menggunakan subsurface() method
            temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
            # Mengubah ukuran gambar sesuai dengan ukuran skala gambar
            temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
        # Menambahkan gambar animasi ke dalam animation_list
        animation_list.append(temp_img_list)
    return animation_list



  def move(self, screen_width, screen_height, surface, target, round_over):
    SPEED = 10
    GRAVITY = 2
    dx = 0
    dy = 0
    self.running = False
    self.attack_type = 0

    #get keypresses
    key = pygame.key.get_pressed()

    #can only perform other actions if not currently attacking
    if self.attacking == False and self.alive == True and round_over == False:
      #check player 1 controls
      if self.player == 1:
        #movement
        if key[pygame.K_a]:
          dx = -SPEED
          self.running = True
        if key[pygame.K_d]:
          dx = SPEED
          self.running = True
        #jump
        if key[pygame.K_w] and self.jump == False:
          self.vel_y = -30
          self.jump = True
        #attack
        if key[pygame.K_r] or key[pygame.K_t]:
          self.attack(target)
          #determine which attack type was used
          if key[pygame.K_r]:
            self.attack_type = 1
          if key[pygame.K_t]:
            self.attack_type = 2


      #check player 2 controls
      if self.player == 2:
        #movement
        if key[pygame.K_LEFT]:
          dx = -SPEED
          self.running = True
        if key[pygame.K_RIGHT]:
          dx = SPEED
          self.running = True
        #jump
        if key[pygame.K_UP] and self.jump == False:
          self.vel_y = -30
          self.jump = True
        #attack
        if key[pygame.K_p] or key[pygame.K_o]:
          self.attack(target)
          #determine which attack type was used
          if key[pygame.K_p]:
            self.attack_type = 1
          if key[pygame.K_o]:
            self.attack_type = 2


    #apply gravity
    self.vel_y += GRAVITY
    dy += self.vel_y

    #ensure player stays on screen
    if self.rect.left + dx < 0:
      dx = -self.rect.left
    if self.rect.right + dx > screen_width:
      dx = screen_width - self.rect.right
    if self.rect.bottom + dy > screen_height - 110:
      self.vel_y = 0
      self.jump = False
      dy = screen_height - 110 - self.rect.bottom

    #ensure players face each other
    if target.rect.centerx > self.rect.centerx:
      self.flip = False
    else:
      self.flip = True

    #apply attack cooldown
    if self.attack_cooldown > 0:
      self.attack_cooldown -= 1

    #update player position
    self.rect.x += dx
    self.rect.y += dy


  #handle animation updates
  def update(self):
    #check what action the player is performing
    if self.health <= 0:
      self.health = 0
      self.alive = False
      self.update_action(6)#6:death
    elif self.hit == True:
      self.update_action(5)#5:hit
    elif self.attacking == True:
      if self.attack_type == 1:
        self.update_action(3)#3:attack1
      elif self.attack_type == 2:
        self.update_action(4)#4:attack2
    elif self.jump == True:
      self.update_action(2)#2:jump
    elif self.running == True:
      self.update_action(1)#1:run
    else:
      self.update_action(0)#0:idle

    animation_cooldown = 50
    #update image
    self.image = self.animation_list[self.action][self.frame_index]
    #check if enough time has passed since the last update
    if pygame.time.get_ticks() - self.update_time > animation_cooldown:
      self.frame_index += 1
      self.update_time = pygame.time.get_ticks()
    #check if the animation has finished
    if self.frame_index >= len(self.animation_list[self.action]):
      #if the player is dead then end the animation
      if self.alive == False:
        self.frame_index = len(self.animation_list[self.action]) - 1
      else:
        self.frame_index = 0
        #check if an attack was executed
        if self.action == 3 or self.action == 4:
          self.attacking = False
          self.attack_cooldown = 20
        #check if damage was taken
        if self.action == 5:
          self.hit = False
          #if the player was in the middle of an attack, then the attack is stopped
          self.attacking = False
          self.attack_cooldown = 20


  def attack(self, target):
    if self.attack_cooldown == 0:
      #execute attack
      self.attacking = True
      self.attack_sound.play()
      attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
      if attacking_rect.colliderect(target.rect):
        target.health -= 10
        target.hit = True


  def update_action(self, new_action):
    #check if the new action is different to the previous one
    if new_action != self.action:
      self.action = new_action
      #update the animation settings
      self.frame_index = 0
      self.update_time = pygame.time.get_ticks()

  def draw(self, surface):
    img = pygame.transform.flip(self.image, self.flip, False)
    surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))