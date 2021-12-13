"""
Group: BugMaker
Game Features: Voice-activated Dragon, Rewards and punishments props., Challenging and fun
"""

import pygame
import os
import sys

from myVariables import *


def Initialize():

    pygame.init()
    pygame.mixer.init()

    # open the window in the centre of the screen
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % ((screenResolution.current_w - SCREEN_WIDTH) / 2,
                                                    (screenResolution.current_h - SCREEN_HEIGHT) / 2)
    # set screen
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT], pygame.DOUBLEBUF, 32)
    # set icon and caption
    pygame.display.set_icon(pygame.image.load('images/dragonicon.ico'))
    pygame.display.set_caption("Voice-activated Dragon Adventure")

    return screen


def draw_text(screen, text, y, size, colour="grey"):
    """
    Draw a black text bigger and a grey text smaller over it to create a 3D effect.
    """

    # set font
    font_black = pygame.font.Font("data/JE.TTF", size + 1)
    font_grey = pygame.font.Font("data/JE.TTF", size)

    # set colour and antialias
    text_black = font_black.render(str(text), 1, pygame.Color("black"))
    text_grey = font_grey.render(str(text), 1, pygame.Color(colour))

    # set x position
    x_black = (SCREEN_WIDTH - text_black.get_width()) / 2
    x_grey = (SCREEN_WIDTH - text_grey.get_width()) / 2

    # show the text in the screen
    screen.blit(text_black, (x_black + 5, y - 2))
    screen.blit(text_grey, (x_grey, y))


def end_the_game(screen, game_score):

    global high_score

    # draw a rectangle to show the result.
    pygame.draw.rect(screen, pygame.Color("black"), (43, SCREEN_HEIGHT / 2 - 77, 314, 154))
    pygame.draw.rect(screen, pygame.Color("lightgrey"), (45, SCREEN_HEIGHT / 2 - 75, 310, 150))

    draw_text(screen, "Your Score: " + str(game_score), 220, 35, "royalblue")

    # if there is a new record, replace it.
    if game_score > high_score:
        high_score = game_score
        draw_text(screen, "New Record!", 160, 35, "gold")

    draw_text(screen, "High score: " + str(high_score), 270, 35, "royalblue")
    draw_text(screen, "Click or Press {Space} to restart", 335, 20)
    draw_text(screen, "Press {Esc} to exit", 365, 20)

    pygame.display.flip()

    # Gets the keyboard events to see whether the user wants to continue to play
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == K_SPACE:
                    return False
                elif e.key == K_ESCAPE:
                    return True
            elif e.type == pygame.MOUSEBUTTONDOWN:
                return False
