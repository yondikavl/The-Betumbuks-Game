import pygame
from pygame import mixer
from fighter import GreenLegion, LaSquadra
from data import *
from health_bar import LaSquadra_Health, GreenLegion_Health

mixer.init()
pygame.init()

# set ukuran layar dengan lebar dan tinggi dari data.py
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_NAME)

# set framerate
clock = pygame.time.Clock()
FPS = 60

# last_count_update akan digunakan nanti pada saat countdown
last_count_update = pygame.time.get_ticks()

# load gambar background dan music
bg_img = pygame.image.load("assets/images/background/bg-menu.png").convert_alpha()
bg_main = pygame.image.load("assets/images/background/bg-main.png").convert_alpha()
glwin_img = pygame.image.load("assets/images/background/bg-glwin.png").convert_alpha()
lswin_img = pygame.image.load("assets/images/background/bg-lswin.png").convert_alpha()
pygame.mixer.music.load("assets/audio/bg.mp3")
green_legion_fx = pygame.mixer.Sound("assets/audio/punch.wav")
lasquadra_fx = pygame.mixer.Sound("assets/audio/uh.wav")

# Volume
pygame.mixer.music.set_volume(0)
pygame.mixer.music.play(-1, 0.0, 5000)
green_legion_fx.set_volume(1)
lasquadra_fx.set_volume(1)

# load spritesheets
greenlegion_sheet = pygame.image.load("assets/images/boxer/ijo.png").convert_alpha()
lasquadra_sheet = pygame.image.load("assets/images/boxer/biru.png").convert_alpha()

# load icons
icon = pygame.image.load("assets/images/icons/icon.png").convert_alpha()
pygame.display.set_icon(icon)

# mendefinisikan font
menu_font_big = pygame.font.Font("assets/fonts/Super Mario Bros.ttf", 40)
menu_font_small = pygame.font.Font("assets/fonts/Super Mario Bros.ttf", 20)
count_font = pygame.font.Font("assets/fonts/Super Mario Bros.ttf", 40)
score_font = pygame.font.Font("assets/fonts/Super Mario Bros.ttf", 15)

# function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# function untuk menggambar menu
def draw_menu():
    if PAUSE_MENU:
        # memperbaharui dan menggambar background sprite
        screen.blit(bg_main, (0, 0))
        draw_text("PAUSE MENU !!!", menu_font_big, RED, 250, 60)
        draw_text("Press Enter to Resume", menu_font_small, WHITE, 300, 500)

    elif END_MENU:
        if fighter1.health == 0:
            # menggambar background kemenangan La Squadra dan karakter fighter2
            screen.blit(lswin_img, (0, 0))
            fighter2.menu_character(screen)
        elif fighter2.health == 0:
            # menggambar background kemenangan Green Legion dan karakter fighter1
            screen.blit(glwin_img, (0, 0))
            fighter1.menu_character(screen)
    else:
        # menggambar background menu utama dan karakter fighter1
        screen.blit(bg_img, (0, 0))
        fighter1.menu_character(screen)
        draw_text("Press Enter to Start", menu_font_small, WHITE, 300, 500)

    # menampilkan perubahan terbaru ke layar
    pygame.display.flip()

# membuat 2 instansiasi fighter
fighter1 = GreenLegion(200, 260, False, BOXER_DATA, greenlegion_sheet, BOXER_ANIMATION_STEPS, green_legion_fx)
fighter2 = LaSquadra(760, 260, True, BOXER_DATA, lasquadra_sheet, BOXER_ANIMATION_STEPS, lasquadra_fx)

# membuat 2 instansiasi health bar
green_health_bar = GreenLegion_Health(fighter1.health, 20, 20)
lasquad_health_bar = LaSquadra_Health(fighter2.health, 580, 20)

# game loop
run = True
while run:
    clock.tick(FPS)
    # Menu utama
    if MENU:
        # Menggambar latar belakang menu
        draw_menu()
        
        # Mengambil input tombol keyboard
        key = pygame.key.get_pressed()
        
        # Jika tombol "Enter" ditekan, keluar dari menu
        if key[pygame.K_RETURN]:
            MENU = False
            round_over = False
        
        # Jika dalam menu akhir dan tombol "Enter" ditekan, keluar dari permainan
        if END_MENU:
            if key[pygame.K_RETURN]:
                run = False

    # Saat permainan sedang berjalan
    else:
        # Menggambar latar belakang
        screen.blit(bg_main, (0, 0))

        # Menampilkan status fighter 1 dan fighter 2
        green_health_bar.update(fighter1.health)
        green_health_bar.draw(screen)
        lasquad_health_bar.update(fighter2.health)
        lasquad_health_bar.draw(screen)
        draw_text("Green Legion", score_font, BLACK, 20, 50)
        draw_text("La Squadra", score_font, BLACK, 830, 50)

        # Memperbarui countdown
        if intro_count <= 0:
            # Memindahkan fighter
            fighter1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter2, round_over)
            fighter2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter1, round_over)
        else:
            # Menampilkan timer countdown
            draw_text(
                str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3
            )
            # Memperbarui timer countdown
            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()

        # Memperbarui fighter
        fighter1.update(fighter2)
        fighter2.update(fighter1)

        # Menggambar fighter
        fighter2.draw(screen)
        fighter1.draw(screen)

        # Jika salah satu fighter telah kalah, tampilkan menu akhir
        if fighter1.health == 0 or fighter2.health == 0:
            round_over = True
            END_MENU = True

        # Jika menu akhir ditampilkan, tampilkan menu utama
        if round_over:
            MENU = True
            END_MENU = True
            PAUSE_MENU = False

    # Handler untuk event keyboard
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    key = pygame.key.get_pressed()

    # Jika tombol "Escape" ditekan, tampilkan menu utama
    if key[pygame.K_ESCAPE]:
        MENU = True
        PAUSE_MENU = True

    # Memperbarui layar
    pygame.display.flip()


# exit pygame
pygame.quit()