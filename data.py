# create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600


# define colours
RED = (255, 0, 0)
GREEN = (0, 230, 0)
DARK_GREEN = (0, 150, 0)
WHITE = (255, 255, 255)

# define game variables
GAME_NAME = "TheBetumbuks"
MENU = True
PAUSE_MENU = False
END_MENU = False
intro_count = 3
score = [0, 0]  # player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

# define fighter variables
BOXER_SIZE = 250
BOXER_SCALE = 1
BOXER_OFFSET = [112, 50]
BOXER_DATA = [BOXER_SIZE, BOXER_SCALE, BOXER_OFFSET]

# define fighter variables
BOXER_SIZE = 250
BOXER_SCALE = 1
BOXER_OFFSET = [112, 50]
BOXER_BG = [BOXER_SIZE, BOXER_SCALE, BOXER_OFFSET]

# define number of steps in each animation
BOXER_ANIMATION_STEPS = [6, 10, 4, 14, 14, 7, 6, 5, 3, 3]
