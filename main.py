import pygame
from pygame import mixer
from fighter import Fighter
from background import Background
from data import *
from health_bar import LaSquadra_Health, GreenLegion_Health

mixer.init()
pygame.init()


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_NAME)


# set framerate
clock = pygame.time.Clock()
FPS = 60
last_count_update = pygame.time.get_ticks()

game_name = pygame.image.load("assets/images/The Betumbuks.png").convert_alpha()

# load music and sounds
pygame.mixer.music.load("assets/audio/bg.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1, 0.0, 5000)

# load spritesheets
boxer_sheet = pygame.image.load("assets/images/boxer/boxer.png").convert_alpha()

# load icons
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()
icon = pygame.image.load("assets/images/icons/icon.png").convert_alpha()
pygame.display.set_icon(icon)

# define font
menu_font_big = pygame.font.Font("assets/fonts/turok.ttf", 75)
menu_font_small = pygame.font.Font("assets/fonts/turok.ttf", 50)
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)


# function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def draw_menu():
    if PAUSE_MENU:
        name_len = GAME_NAME.__len__()
        background_sprites.draw(screen)
        background_sprites.update()
        name_pos_x = SCREEN_WIDTH - ((name_len * 30) * 2)
        draw_text("PAUSE MENU !!!", menu_font_big, RED, name_pos_x, 60)
        draw_text("Press Enter to Resume", menu_font_small, GREEN, 250, 330)
    elif END_MENU:
        screen.fill((0, 0, 0))
        name_len = GAME_NAME.__len__()
        name_pos_x = SCREEN_WIDTH - ((name_len * 30) * 2)
        BOXER_DATA[1] = 3
        if player.health == 0:
            enemy.menu_character(screen)
        elif enemy.health == 0:
            player.menu_character(screen)
        draw_text(
            "La Squadra Victory" if player.health == 0 else "Green Legion Victory", menu_font_big, RED,
            200 if player.health == 0 else 180,
            60,
        )
        draw_text("Press Enter to Quit", menu_font_small, WHITE, 250, 400)
    else:
        name_len = GAME_NAME.__len__()
        name_pos_x = SCREEN_WIDTH - ((name_len * 30) * 2)
        screen.fill((0, 0, 0))
        BOXER_DATA[1] = 3
        draw_text(GAME_NAME, menu_font_big, WHITE, name_pos_x, 60)
        draw_text("Press Enter to start", menu_font_small, RED, 250, 440)
        player.menu_character(screen)
    clock.tick(45)


# create two instances of fighters
player = Fighter(1, 200, 310, False, BOXER_DATA, boxer_sheet, BOXER_ANIMATION_STEPS)
enemy = Fighter(2, 760, 310, True, BOXER_DATA, boxer_sheet, BOXER_ANIMATION_STEPS)

# create two instances of button
green_health_bar = GreenLegion_Health(player.health, 20, 20)
lasquad_health_bar = LaSquadra_Health(enemy.health, 580, 20)

background_sprites = pygame.sprite.Group()
background = Background()
background_sprites.add(background)


# game loop
run = True
while run:
    clock.tick(FPS)

    if MENU == True:
        # draw background
        draw_menu()
        key = pygame.key.get_pressed()
        if key[pygame.K_RETURN]:
            MENU = False
            round_over = False
        if END_MENU:
            if key[pygame.K_RETURN]:
                run = False
    else:
        background_sprites.draw(screen)
        background_sprites.update()

        # show player stats
        green_health_bar.update(player.health)
        green_health_bar.draw(screen)
        lasquad_health_bar.update(enemy.health)
        lasquad_health_bar.draw(screen)
        draw_text("Green Legion", score_font, WHITE, 20, 30)
        draw_text("La Squadra", score_font, WHITE, 840, 30)

        # update countdown
        if intro_count <= 0:
            # move fighters
            player.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, enemy, round_over)
            enemy.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, player, round_over)
        else:
            # display count timer
            draw_text(
                str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3
            )
            # update count timer
            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()

        # update fighters
        player.update(enemy)
        enemy.update(player)

        # draw fighters
        enemy.draw(screen)
        player.draw(screen)

        if player.health == 0 or enemy.health == 0:
            round_over = True
            END_MENU = True

        if round_over == True:
            MENU = True
            END_MENU = True
            PAUSE_MENU = False

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    key = pygame.key.get_pressed()
    if key[pygame.K_ESCAPE]:
        MENU = True
        PAUSE_MENU = True

    # update display
    pygame.display.flip()

# exit pygame
pygame.quit()
