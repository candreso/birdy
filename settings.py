import os

# game options/settings
TITLE = "birdy"
WIDTH = 480
HEIGHT = 600
FPS = 60 # frames per second
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100,50) # window position

FONT_NAME = 'arial'

# rgb color values
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PEACH = (255, 216, 199)
BURNT_ORANGE = (224, 131, 49)
SEA_GREEN = (116, 237, 187)
NAVY = (29, 84, 105)


# player properties
PLAYER_ACC = 0.5 # horizontal acceleration
PLAYER_FRICTION = -0.12 # horizontal friction
JUMP_SPEED = -13
G = 0.5 # gravity / vertical acceleration

PLATFORM_HEIGHT = HEIGHT / 25

# starting platforms
PLATFORM_LIST = \
    [(HEIGHT/1.25, PLATFORM_HEIGHT),
     (HEIGHT/1.65, PLATFORM_HEIGHT),
     (HEIGHT/2.15, PLATFORM_HEIGHT),
     (HEIGHT/3.5, PLATFORM_HEIGHT)]

MOVING_PLATFORM_LIST = [(HEIGHT/9, PLATFORM_HEIGHT)]
