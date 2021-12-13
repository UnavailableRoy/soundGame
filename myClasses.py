"""
Group: BugMaker
Game Features: Voice-activated Dragon, Rewards and punishments props., Challenging and fun
"""

import pygame
import random


from random import uniform
from myVariables import *

# attribute index of image rectangle
POS_X = 0  # index of position x
POS_Y = 1  # index of position y
RECT_WIDTH = 2   # index of image rectangle width
RECT_HEIGHT = 3  # index of image rectangle height

# define paths of game-related files
PATH_BACKGROUND_IMAGE = 'images/volcano.png'  # path of game background image
PATH_GREEN_DRAGON1_IMAGE = 'images/green_dragon1.png'  # path of dragon wing up image
PATH_GREEN_DRAGON2_IMAGE = 'images/green_dragon2.png'  # path of dragon wing down image
PATH_RED_DRAGON1_IMAGE = 'images/red_dragon1.png'  # path of red dragon wing up image
PATH_RED_DRAGON2_IMAGE = 'images/red_dragon2.png'  # path of red dragon wing down image
PATH_FLAME_DOWN_IMAGE = 'images/flame_down.png'  # path of a lower flame image
PATH_MAGMA_IMAGE = 'images/magma.png'  # path of the magma river image
PATH_RED_POTION1_IMAGE = 'images/red_potion1.png'  # path of red potion light image
PATH_RED_POTION2_IMAGE = 'images/red_potion2.png'  # path of red potion image
PATH_GREEN_POTION1_IMAGE = 'images/green_potion1.png'  # path of green potion light image
PATH_GREEN_POTION2_IMAGE = 'images/green_potion2.png'  # path of green potion image
PATH_FLOWER_IMAGE = 'images/flower.png'  # path of flower image
PATH_JUMP_SOUNDS = 'sounds/jump.mp3'  # path of jump sounds
PATH_SCORE_SOUNDS = 'sounds/score.mp3'  # path of get score sounds
PATH_DEAD_SOUNDS = 'sounds/dead.mp3'  # path of dragon dead sounds
PATH_POTION_SOUNDS = 'sounds/potion.wav'  # path of acquire potion sounds


class Dragon(pygame.sprite.Sprite):

    # A class for the dragon, inherit the Sprite Class
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # load images of different dragon status
        self.image_list = [pygame.image.load(PATH_GREEN_DRAGON1_IMAGE).convert_alpha(),
                           pygame.image.load(PATH_GREEN_DRAGON2_IMAGE).convert_alpha()]
        self.image_num = len(self.image_list)
        self.image_index = 0  # index of current image to display
        self.cur_image = self.image_list[self.image_index]  # current image to display on the screen
        self.rect = self.cur_image.get_rect()  # get image rectangle of current image
        self.rect[POS_X] = SCREEN_WIDTH / 8  # init dragon position x
        self.rect[POS_Y] = SCREEN_HEIGHT / 2  # init dragon position y
        self.times_to_up = 0  # times dragon to move up per jump

    def is_off_screen(self):
        """check if it is off-screen

        :param: none
        :return: True or False
        """
        return self.rect[POS_Y] + self.rect[RECT_HEIGHT] >= SCREEN_HEIGHT - MAGMA_HEIGHT

    def start_jump(self):
        """init times dragon to move up per jump

        :param: none
        :return: none
        """
        self.times_to_up = MOVE_UP_TIMES

    def down(self):
        """move the dragon on

        :param: none
        :return: none
        """
        self.rect[POS_Y] += DROP_PIXELS

    def up(self):
        """move the dragon up

        :param: none
        :return: none
        """
        self.rect[POS_Y] -= JUMP_PIXELS
        self.times_to_up -= 1

    def update(self):
        """update dragon flying status and position

        :param: none
        :return: none
        """
        # update current image to display on the screen
        # switch different images of dragon status to create flapping effect
        self.image_index = (self.image_index + 1) % self.image_num
        self.cur_image = self.image_list[self.image_index]
        # The following part is connected to up() and down()
        # if FPS = 60, it means game loops 60 times per second. Once clicking, self.times_to_up = MOVE_UP_TIMES and the
        # dragon will move up "MOVE_UP_TIMES" times for "JUMP_PIXELS" distance with "self.times_to_up -= 1" per time.
        # When self.times_to_up <= 0, then it moves down "FPS - MOVE_UP_TIMES" times per second for "DROP_PIXELS"
        # distance per time.
        if self.times_to_up > 0:
            self.up()

    def draw(self, screen):
        """draw a normal flying dragon on the screen

        :param: screen: the screen where to draw a dragon
        :return: none
        """
        screen.blit(self.cur_image, self.rect)

    def draw_dead(self, screen):
        """draw a dead dragon dropping from the sky on the screen

        :param: screen: the screen where to draw a dragon
        :return: none
        """
        # update position y and rotate the dragon image to create dropping effect
        self.rect[POS_Y] += DROP_PIXELS
        dragon = pygame.transform.rotate(self.cur_image, SCREEN_HEIGHT / 2 - self.rect.y)
        # draw the dragon on the screen
        screen.blit(dragon, self.rect)

    def check_collision_with_group(self, group):
        """check if there is a collision with group objects

        :param: group: sprite group object
        :return: True or False
        """
        return pygame.sprite.spritecollideany(self, group)

    def check_collision_with_single(self, single):
        """check if there is a collision with a single object

        :param: single: a single sprite object
        :return: True or False
        """
        return pygame.sprite.collide_rect(self, single)

    def check_pass(self, barrier):
        """check if the dragon go through the barrier successfully

        :param: barrier: can be a pair of flames
        :return: True or False
        """
        return self.rect[POS_X] > barrier.rect[POS_X] and not barrier.is_passed

    def change_appearance(self, path_list):
        """change dragon appearance

        :param: path_list: path list of new images
        :return: none
        """
        # load images of a set of new dragon status
        self.image_list = [""] * len(path_list)
        for i in range(0, len(path_list)):
            self.image_list[i] = pygame.image.load(path_list[i]).convert_alpha()
        self.image_num = len(self.image_list)

    def change_size(self, diff_len):
        """change dragon size

        :param: diff_len: the length of the increase or decrease in width and height
        :return: none
        """
        self.cur_image = pygame.transform.scale(self.image_list[self.image_index],
                                                (self.rect[RECT_WIDTH] + diff_len, self.rect[RECT_HEIGHT] + diff_len))


class Flame(pygame.sprite.Sprite):

    # A class for a flame， inherit the Sprite Class
    def __init__(self, flame_len, inverted):
        """init flame attributes

        :param: flame_len: random flame length
        :param: inverted: True: invert a lower flame to generate a pair of flames
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(PATH_FLAME_DOWN_IMAGE).convert_alpha()  # load image
        self.rect = self.image.get_rect()  # get image rectangle of the image
        self.rect[POS_X] = SCREEN_WIDTH  # flame always move from the most right of game screen to the left

        if inverted:
            # invert a lower flame to create an upper flame
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[POS_Y] = flame_len - self.rect[RECT_HEIGHT]
            self.is_passed = True
        else:
            # create a lower flame
            self.rect[POS_Y] = SCREEN_HEIGHT - flame_len
            # note: only to identify one of flame pairs to mark if the dragon go through them and modify total score
            self.is_passed = False

    def is_off_screen(self):
        """check if it is off-screen

        :param: none
        :return: True or False
        """
        return self.rect[POS_X] + self.rect[RECT_WIDTH] < 0

    def update(self):
        """update flame position

        :param: none
        :return: none
        """
        self.rect[POS_X] -= MOVE_PIXELS

    def set_passed(self):
        """set pass flag to indicate if the dragon go through a pair of flames successfully

        :param: none
        :return: none
        """
        self.is_passed = True


class Magma(pygame.sprite.Sprite):

    # A class for the magma rolling to the left， inherit the Sprite Class
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # init attributes of Sprite Class
        self.image = pygame.image.load(PATH_MAGMA_IMAGE).convert_alpha()  # load image
        self.rect = self.image.get_rect()  # get image rectangle to modify position
        self.rect[POS_X] = 0  # init magma position x
        self.rect[POS_Y] = SCREEN_HEIGHT - MAGMA_HEIGHT  # init magma position y

    def is_off_screen(self):
        """check if it is off-screen

        :param: none
        :return: none
        """
        return self.rect[POS_X] < -SCREEN_WIDTH

    def update(self):
        """update the magma position, when it is reaching its end, then reset it

        :param: none
        :return: none
        """
        # update position x to move to the left
        self.rect[POS_X] -= MOVE_PIXELS
        # when reaching its end, reset it
        if self.is_off_screen():
            self.rect[POS_X] = 0

    def draw(self, screen):
        """draw magma on the screen

        :param: screen: screen where to draw magma
        :return: none
        """
        screen.blit(self.image, self.rect)


class Potion(pygame.sprite.Sprite):

    # A class for a potion, inherit the Sprite Class
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.randint(0, 1)  # random 0 or 1
        if self.type == 0:  # if random number is 0, show red potion
            self.image_list = [pygame.image.load(PATH_RED_POTION1_IMAGE).convert_alpha(),
                               pygame.image.load(PATH_RED_POTION2_IMAGE).convert_alpha()]
        else:  # if random number is 1, show green potion
            self.image_list = [pygame.image.load(PATH_GREEN_POTION1_IMAGE).convert_alpha(),
                               pygame.image.load(PATH_GREEN_POTION2_IMAGE).convert_alpha()]
        self.image_index = 0  # index of current image to display
        self.cur_image = self.image_list[self.image_index]  # current image to display on the screen
        self.rect = self.cur_image.get_rect()
        self.rect[POS_X] = random.randint(50, 250)  # random generate potion position x
        self.rect[POS_Y] = random.randint(50, 250) + FLAME_SPACE - 50  # random generate potion position y
        self.speed = uniform(0.1, 0.5)  # random generate potion speed
        self.mask = pygame.mask.from_surface(self.cur_image)

    def visible(self):
        """ check if it is off-screen

        :param: none
        :return: True or False
        """
        return -self.image_list[0].get_width() < self.rect[POS_X] < SCREEN_WIDTH

    def update(self, frame=1):
        """ update potion position on the screen
        
        :param： frame
        :return: none
        """
        self.rect[POS_X] -= int(self.speed * (1000.0 * frame / FPS))

    def redraw(self, screen):
        """draw a potion on the screen

        :param： screen: the screen where to draw a potion
        :return: none
        """
        screen.blit(self.cur_image, self.rect)


class Flower(pygame.sprite.Sprite):

    # A class for a flower inherit the Sprite Class
    def __init__(self, flame_position, index):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(PATH_FLOWER_IMAGE).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect[POS_X] = SCREEN_WIDTH + FLAME_WIDTH / 2 - self.rect.width / 2
        # if index equal 1, image on the inverted flame, flip flower image
        if index == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[POS_Y] = flame_position
        else:
            self.rect[POS_Y] = flame_position - self.rect.height
        self.mask = pygame.mask.from_surface(self.image)

    def is_off_screen(self):
        """check if it is off-screen

        :param: none
        :return: True or False
        """
        return self.rect[POS_X] + self.rect[RECT_WIDTH] < 0

    def update(self):
        """update flower position

        :param: none
        :return: none
        """
        self.rect[POS_X] -= MOVE_PIXELS


class FlappyDragonGame:

    # A class for Flappy Dragon Game
    def __init__(self, dragon, magma):
        self.dragon = dragon  # init dragon object
        self.flame_group = pygame.sprite.Group()  # init flame objects
        self.potion_group = pygame.sprite.Group()  # init potion object
        self.flower_group = pygame.sprite.Group()  # init flower object
        self.magma = magma  # init magma object
        self.bg = pygame.image.load(PATH_BACKGROUND_IMAGE).convert()  # load game background image
        self.time_clock = pygame.time.Clock()  # game time clock
        self.score = 0  # total game score
        self.wait_click = True  # waiting click to start game
        self.sounds = {"jump": pygame.mixer.Sound(PATH_JUMP_SOUNDS),
                       "score": pygame.mixer.Sound(PATH_SCORE_SOUNDS),
                       "dead": pygame.mixer.Sound(PATH_DEAD_SOUNDS),
                       "potion": pygame.mixer.Sound(PATH_POTION_SOUNDS)}  # load kinds of game sounds

    def set_frame_rate(self, frame_rate):
        """set game frame rate

        :param： frame_rate: game frame rate
        :return: none
        """
        self.time_clock.tick(frame_rate)

    def draw_bg(self, screen):
        """draw game background

        :param： screen: screen where to draw the game background
        :return: none
        """
        screen.blit(self.bg, (0, 0))

    def play_sounds(self, sound_type):
        """choose different sounds to play

        :param: sound_type: sounds including "jump", "score" and "dead"
        :return: none
        """
        if sound_type == "jump" or sound_type == "score" or sound_type == "dead" or sound_type == "potion":
            self.sounds[sound_type].play()

    def wait_click_set(self, flag):
        """set wait click flag

        :param: flag: True or False
        :return: none
        """
        self.wait_click = flag

    def get_score(self):
        """when a dragon get through a pair of flames, it can get one point

        :param: none
        :return: score
        """
        self.score += 1
        # return self.score


def set_flamepair_timer(interval):
    """set a timer for an event: to add a new flame pair periodically

    :param: interval: periodic time (milliseconds)
    :return: none
    """
    pygame.time.set_timer(EV_ADD_FLAMEPAIR, interval)


def get_flame_pair():
    """get a pair of flames

    :param: none
    :return: list of a flame pair
    """
    # get the random length of a flame
    flame_len = random.randint(100, 250)
    # return a pair of flames in the opposite direction
    return Flame(flame_len, False), Flame(SCREEN_HEIGHT - flame_len - FLAME_SPACE, True)


def get_potion():
    """get potion

    :param: none
    :return: list of a potion
    """
    potion = Potion()
    return potion


def get_flower(flame_position):
    """get flower

    :param: flame_position: is a list, include the y coordinate of the flame pair
    :return: list of a flower
    """
    index = random.randint(0, 1)
    if index == 1:
        # inverted flame position
        position = flame_position[1] + FLAME_HEIGHT
    else:
        # flame position
        position = flame_position[0]
    flower = Flower(position, index)

    return flower

