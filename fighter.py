import pygame

class Fighter:
    def __init__(self, x, y, flip, data, sprite_sheet, animation_steps, sound):
        self.__size = data[0]
        self.__scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0  # 0:idle #1:run #2:jump #3:attack1 #4: attack2 #5:hit #6:death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.vel_y = 0   
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_power = 0
        self.attack_cooldown = 0
        self.hit = False
        self.health = 200
        self.alive = True
        self.should_move = False
        self.should_attack = False
        self.attack_sound = sound
    
    def get_size(self):
        return self.__size
    
    def set_size(self, size):
        self.__size == size
    
    def get_scale(self):
        return self.__scale
    
    def set_scale(self, scale):
        self.__scale = scale
    
    def load_images(self, sprite_sheet, animation_steps):
        # fungsi untuk memuat gambar-gambar animasi dari sprite sheet
        animation_list = [] # variabel untuk menyimpan daftar gambar animasi
        for y, animation in enumerate(animation_steps): # untuk setiap animasi, yaitu setiap baris dalam sprite sheet, lakukan:
            temp_img_list = [] # variabel untuk menyimpan daftar gambar dalam animasi
            for x in range(animation): # untuk setiap gambar dalam animasi, yaitu setiap kolom dalam sprite sheet, lakukan:
                temp_img = sprite_sheet.subsurface(
                    x * self.get_size(), y * self.get_size(), self.get_size(), self.get_size()
                ) # potong gambar dari sprite sheet sesuai ukuran yang diinginkan
                temp_img_list.append(
                    pygame.transform.scale(
                        temp_img,
                        (self.get_size() * self.get_scale(), self.get_size() * self.get_scale()),
                    )
                ) # ubah ukuran gambar dan tambahkan ke daftar gambar dalam animasi
            animation_list.append(temp_img_list) # tambahkan daftar gambar dalam animasi ke daftar gambar animasi
        return animation_list # kembalikan daftar gambar animasi

    def move(self):
        pass

    def update(self):
        pass

    # menampilkan karakter di menu
    def menu_character(self, surface):
        animation_cooldown = 50
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
            self.action += 1
            if self.action > len(self.animation_list[self.action]):
                self.action = 0
        surface.blit(pygame.transform.scale_by(self.image, 1.25), (350, 200))

    # melakukan serangan
    def attack(self, target):
        if self.attack_cooldown == 0:
            # Melakukan serangan jika cooldown serangan = 0
            self.attacking = True
            self.attack_sound.play()
            # Membuat objek Rect untuk area serangan
            attacking_rect = pygame.Rect(
                self.rect.centerx - (2 * self.rect.width * self.flip),
                self.rect.y,
                1 * self.rect.width,
                self.rect.height,
            )
            # Mengecek apakah area serangan bertabrakan dengan target
            if attacking_rect.colliderect(target.rect):
                target.hit = True
            else:
                target.hit = False

    # mengecek action yang dilakukan
    def update_action(self, new_action):
        if new_action != self.action: # jika tindakan baru berbeda dengan tindakan sebelumnya
            self.action = new_action # update tindakan dengan tindakan baru
            self.frame_index = 0 # atur ulang indeks frame untuk animasi
            self.update_time = pygame.time.get_ticks() # atur ulang waktu pembaruan animasi

    # memposisikan karakter
    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(
            img,
            (
                self.rect.x - (self.offset[0] * self.get_scale()),
                self.rect.y - (self.offset[1] * self.get_scale()),
            ),
        )
        
class GreenLegion(Fighter):
    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 6
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        # menerima input keyboard
        key = pygame.key.get_pressed()

        # hanya dapat melakukan aksi lain jika tidak sedang menyerang, hidup, dan ronde belum berakhir
        if self.attacking == False and self.alive == True and round_over == False:
            # gerakan
            if key[pygame.K_a]: # jika tombol "a" ditekan
                dx = -SPEED # gerak ke kiri
                self.running = True # atur "running" ke True
            if key[pygame.K_d]: # jika tombol "d" ditekan
                dx = SPEED # gerak ke kanan
                self.running = True  # atur "running" ke True
            # lompat
            if key[pygame.K_s] and self.jump == False: # jika tombol "space" ditekan dan karakter belum sedang melompat
                self.vel_y = -25 # atur kecepatan vertikal karakter
                self.jump = True  # atur "jump" ke True
            if (key[pygame.K_e] or key[pygame.K_q]):
                self.attack(target)  # panggil metode "attack" dengan parameter "target"
                if key[pygame.K_e]:
                    self.attack_type = 1
                if key[pygame.K_q]:
                    self.attack_type = 2
                

        # menerapkan gravitasi
        self.vel_y += GRAVITY # Menambahkan kecepatan vertikal karena efek gravitasi
        dy += self.vel_y # Menambahkan perubahan posisi vertikal berdasarkan kecepatan vertikal saat ini

        # memastikan pemain tetap berada pada layar
        if self.rect.left + dx < 0: # Jika posisi pemain setelah pergerakan ke kiri kurang dari nol, atur posisinya ke tepi layar sebelah kiri
            dx = -self.rect.left
        if self.rect.right + dx > screen_width: # Jika posisi pemain setelah pergerakan ke kanan lebih dari lebar layar, atur posisinya ke tepi layar sebelah kanan
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 160: # Jika posisi pemain setelah pergerakan ke bawah lebih dari tinggi layar dikurangi 160 pixel (sebagai batas bawah), atur posisinya ke batas bawah
            self.vel_y = 0 # set kecepatan vertikal kembali menjadi nol
            self.jump = False # mengatur nilai jump ke False
            dy = screen_height - 160 - self.rect.bottom # Menetapkan perubahan posisi vertikal agar pemain berada pada batas bawah layar.

        # memastikan pemain menghadap satu sama lain
        if target.rect.centerx > self.rect.centerx: # Jika posisi target lebih ke kanan dari posisi pemain, atur pemain menghadap ke kanan
            self.flip = False
        else: # Jika posisi target lebih ke kiri dari posisi pemain, atur pemain menghadap ke kiri
            self.flip = True

        # menerapkan cooldown serangan
        if self.attack_cooldown > 0: # Jika nilai attack_cooldown lebih besar dari nol, kurangi nilainya satu per satu
            self.attack_cooldown -= 1

        # update posisi pemain
        self.rect.x += dx # Menambahkan perubahan posisi horizontal ke posisi X saat ini
        self.rect.y += dy # Menambahkan perubahan posisi vertikal ke posisi Y saat ini
        
    def update(self, target):
        # check what action the player is performing
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(8)
        elif self.attacking == True:
            if self.attack_type == 1:  # Combo Punch1
                self.update_action(1)
            elif self.attack_type == 2:  # Punch
                self.update_action(2)
        elif self.jump == True:
            self.update_action(0)
        elif self.running == True:
            self.update_action(7)
        else:
            self.update_action(0)

        animation_cooldown = 50
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        # check if the animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            # if the player is dead then end the animation
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                # check if an attack was executed
                if (self.action == 1 or self.action == 2):
                    self.attacking = False
                    self.attack_cooldown = 20
                if target.hit == True:
                    if self.action == 1:
                        target.health -= 20
                    if self.action == 2:
                        target.health -= 15

class LaSquadra(Fighter):
    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 6
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        # menerima input keyboard
        key = pygame.key.get_pressed()

        # hanya dapat melakukan aksi lain jika tidak sedang menyerang, hidup, dan ronde belum berakhir
        if self.attacking == False and self.alive == True and round_over == False:
            # gerakan
            if key[pygame.K_LEFT]: # jika tombol "PANAH KIRI" ditekan
                dx = -SPEED  # gerak ke kiri
                self.running = True # atur "running" ke True
            if key[pygame.K_RIGHT]: # jika tombol "PANAH KANAN" ditekan
                dx = SPEED # gerak ke kanan
                self.running = True # atur "running" ke True
            # lompat
            if key[pygame.K_UP] and self.jump == False: # jika tombol "UP ARROW" ditekan dan karakter belum sedang melompat
                self.vel_y = -25 # atur kecepatan vertikal karakter
                self.jump = True  # atur "jump" ke True
            if key[pygame.K_p] or key[pygame.K_o]:
                self.attack(target) # panggil metode "attack" dengan parameter "target"
                if key[pygame.K_p]:
                    self.attack_type = 1
                if key[pygame.K_o]:
                    self.attack_type = 2

        # menerapkan gravitasi
        self.vel_y += GRAVITY # Menambahkan kecepatan vertikal karena efek gravitasi
        dy += self.vel_y # Menambahkan perubahan posisi vertikal berdasarkan kecepatan vertikal saat ini

        # memastikan pemain tetap berada pada layar
        if self.rect.left + dx < 0: # Jika posisi pemain setelah pergerakan ke kiri kurang dari nol, atur posisinya ke tepi layar sebelah kiri
            dx = -self.rect.left
        if self.rect.right + dx > screen_width: # Jika posisi pemain setelah pergerakan ke kanan lebih dari lebar layar, atur posisinya ke tepi layar sebelah kanan
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 160: # Jika posisi pemain setelah pergerakan ke bawah lebih dari tinggi layar dikurangi 160 pixel (sebagai batas bawah), atur posisinya ke batas bawah
            self.vel_y = 0 # set kecepatan vertikal kembali menjadi nol
            self.jump = False # mengatur nilai jump ke False
            dy = screen_height - 160 - self.rect.bottom # Menetapkan perubahan posisi vertikal agar pemain berada pada batas bawah layar.

        # memastikan pemain menghadap satu sama lain
        if target.rect.centerx > self.rect.centerx: # Jika posisi target lebih ke kanan dari posisi pemain, atur pemain menghadap ke kanan
            self.flip = False
        else: # Jika posisi target lebih ke kiri dari posisi pemain, atur pemain menghadap ke kiri
            self.flip = True

        # menerapkan cooldown serangan
        if self.attack_cooldown > 0: # Jika nilai attack_cooldown lebih besar dari nol, kurangi nilainya satu per satu
            self.attack_cooldown -= 1

        # update posisi pemain
        self.rect.x += dx # Menambahkan perubahan posisi horizontal ke posisi X saat ini
        self.rect.y += dy # Menambahkan perubahan posisi vertikal ke posisi Y saat ini
        
    # handle animation updates
    def update(self, target):
        # check what action the player is performing
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(8)
        elif self.attacking == True:
            if self.attack_type == 1:  # Combo Punch1
                self.update_action(1)
            elif self.attack_type == 2:  # Punch
                self.update_action(2)
        elif self.jump == True:
            self.update_action(0)
        elif self.running == True:
            self.update_action(7)
        else:
            self.update_action(0)

        animation_cooldown = 50
        # update image
        self.image = self.animation_list[self.action][self.frame_index]
        # check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        # check if the animation has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            # if the player is dead then end the animation
            if self.alive == False:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                # check if an attack was executed
                if (self.action == 1 or self.action == 2):
                    self.attacking = False
                    self.attack_cooldown = 20
                if target.hit == True:
                    if self.action == 1:
                        target.health -= 15
                    if self.action == 2:
                        target.health -= 20