"""
Group: BugMaker
Game Features: Voice-activated Dragon, Rewards and punishments props., Challenging and fun
"""

import pygame
from pygame.locals import *


SCREEN_WIDTH = 400                        # game screen width
SCREEN_HEIGHT = 500                       # game screen height
MOVE_PIXELS = 3                           # move speed of the game screen (eg. background and magma )
FPS = 60                                  # frame rate
EV_ADD_FLAMEPAIR = USEREVENT + 1          # custom event

MAGMA_HEIGHT = 73                         # Height of the magma

FLAME_WIDTH = 52                          # width of flame
FLAME_HEIGHT = 320                        # height of flame
FLAME_SPACE = 4 * 40                      # space between flames
FLAME_INTERVAL = 1600                     # milliseconds to add a new flame

MOVE_UP_TIMES = 15                        # times to move up per jump
JUMP_PIXELS = 4                           # pixel distance each time you move up
DROP_PIXELS = 3                           # pixel distance each time you drop

pygame.init()                             # initialize pygame
screenResolution = pygame.display.Info()  # get screen resolution
pygame.quit()                             # close pygame
high_score = 0                            # store the high score
