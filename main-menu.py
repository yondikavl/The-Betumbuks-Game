import pygame
import button

# create display window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('The Betumbuks')

#load music and sounds
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)

# load background image
background_img = pygame.image.load('assets/images/background/bg-main.png').convert()

# load button images
start_img = pygame.image.load('assets/images/button/btn_play.png').convert_alpha()
options_img = pygame.image.load('assets/images/button/btn_options.png').convert_alpha()
exit_img = pygame.image.load('assets/images/button/btn_quit.png').convert_alpha()

# create button instances
start_button = button.Button(400, 300, start_img, 0.8)
options_button = button.Button(400, 380, options_img, 0.8)
exit_button = button.Button(400, 460, exit_img, 0.8)

# game loop
run = True
while run:

    # draw background image
    screen.blit(background_img, (0, 0))

    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            run = False

        # handle button events
        start_action = start_button.handle_event(event)
        options_action = options_button.handle_event(event)
        exit_action = exit_button.handle_event(event)

        # check for button actions
        if start_action:
            try:
                # Execute start_game.py within the same Python process
                exec(open('start_game.py').read())
            except FileNotFoundError:
                print('start_game.py not found')
        if options_action:
            print('OPTIONS')
        if exit_action:
            run = False

    # draw buttons on screen
    start_button.draw(screen)
    options_button.draw(screen)
    exit_button.draw(screen)

    pygame.display.update()

pygame.quit()
