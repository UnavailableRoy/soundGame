"""
Group: BugMaker
Game Features: Voice-activated Dragon, Rewards and punishments props., Challenging and fun
"""

import pygame
import sys


import audio
from myClasses import *
from myFunctions import *


def main():
    # init flag
    # the initialization potion item did not appear
    potion_play = False
    # sounds control
    sounds_off = False

    # initialize pygame
    screen = Initialize()
    # create dragon, magma and game instance
    mygame = FlappyDragonGame(Dragon(), Magma())
    # Set up a timer to add new flame pairs
    set_flamepair_timer(FLAME_INTERVAL)

    # load images of sounds status
    sound_off_image = pygame.image.load("images/sounds_off.png").convert_alpha()
    sound_on_image = pygame.image.load("images/sounds_on.png").convert_alpha()
    # get image rectangle of sound icon
    sounds_rect = sound_on_image.get_rect()
    # locate the centre of the sound icon at (200, 480)
    sounds_rect.center = 200, 480

    while mygame.wait_click:
        # draw everything and waitClick for the user to click to start the game
        # when we click somewhere, the dragon will jump and the game will start
        mygame.draw_bg(screen)
        draw_text(screen, "Hint:", 75, 40)
        draw_text(screen, '"Shout" to move up', 120, 20)
        draw_text(screen, '"Whisper" to move down', 150, 20)
        draw_text(screen, "Help:", 250, 40)
        draw_text(screen, "Click or press {Space} to start", 300, 20)
        draw_text(screen, "Press {M} to control the sound", 330, 20)
        # drawing a magma river and a flappy dragon
        mygame.magma.draw(screen)
        mygame.dragon.draw(screen)

        # draw the sounds icon
        if not sounds_off:
            screen.blit(sound_on_image, sounds_rect)
        else:
            screen.blit(sound_off_image, sounds_rect)

        # update the screen
        pygame.display.update()

        # check if the user pressed left click or space to start (or not) the game
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN or (e.type == pygame.KEYDOWN and e.key == K_SPACE):
                # init dragon jump times
                mygame.dragon.start_jump()
                mygame.wait_click_set(False)
            if e.type == pygame.KEYDOWN:
                # check whether user wants to turn off the sounds
                if e.key == K_m:
                    sounds_off = not sounds_off

    # Start audio listener
    audio.get_wave()
    # Loop until...we die!

    while True:
        # Drawing the background
        mygame.draw_bg(screen)

        # Analyze audio data if > 300 dragon goes up
        if audio.output() > 300:
            mygame.dragon.start_jump()
            if not sounds_off:
                mygame.play_sounds("jump")
        # If between 300 and 50, dragon goes down
        elif 300 > audio.output() > 50:
            mygame.dragon.down()
            if not sounds_off:
                mygame.play_sounds("jump")
        # Else keep flying

        # get the mouse, keyboard or user events and act accordingly
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == EV_ADD_FLAMEPAIR:
                flame_pair = get_flame_pair()
                mygame.flame_group.add(flame_pair[0])
                mygame.flame_group.add(flame_pair[1])
            elif e.type == pygame.KEYDOWN:
                if e.key == K_UP:
                    mygame.dragon.start_jump()
                    if not sounds_off:
                        mygame.play_sounds("jump")
                if e.key == K_DOWN:
                    mygame.dragon.down()
                    if not sounds_off:
                        mygame.play_sounds("jump")
                if e.key == K_m:
                    sounds_off = not sounds_off
                elif e.key == K_ESCAPE:
                    exit()

            # when the score is greater than 2, potion appear, and one potion is generated for each pillar
            if mygame.score > 2 and e.type == EV_ADD_FLAMEPAIR:
                potion = get_potion()
                type = potion.type              # type equal 1 is green potion, type equal 0 is red potion
                mygame.potion_group.add(potion)
                potion_play = False

            # when the score is greater than 10, flower appear, and one flower is generated for each pillar
            if mygame.score > 10 and e.type == EV_ADD_FLAMEPAIR:
                flower = get_flower([flame_pair[0].rect.y, flame_pair[1].rect.y])
                mygame.flower_group.add(flower)

        # set new frame rate
        mygame.set_frame_rate(FPS)

        # if a pair of flames are not visible anymore, then remove them from the list
        if len(mygame.flame_group.sprites()) > 0 and mygame.flame_group.sprites()[0].is_off_screen():
            mygame.flame_group.remove(mygame.flame_group.sprites()[0])

        # if flowers are not visible anymore, then remove them from the list
        if len(mygame.flower_group.sprites()) > 0 and mygame.flower_group.sprites()[0].is_off_screen():
            mygame.flower_group.remove(mygame.flower_group.sprites()[0])

        # update the position of the flame group and redraw them
        mygame.flame_group.update()
        mygame.flame_group.draw(screen)

        # update potion position and remove it if potion is not visible anymore.
        mygame.potion_group.update()             
        for c in mygame.potion_group:
            if not c.visible():
                mygame.potion_group.remove(mygame.potion_group.sprites()[0])
            else:
                c.redraw(screen)

        # redraw the magma
        mygame.magma.update()
        mygame.magma.draw(screen)
        # update the dragon position and redraw it
        mygame.dragon.update()

        if potion_play:
            if type == 1:
                mygame.dragon.change_size(15)
            else:
                mygame.dragon.change_appearance([PATH_RED_DRAGON1_IMAGE, PATH_RED_DRAGON2_IMAGE])
            mygame.dragon.draw(screen)
        else:
            mygame.dragon.change_appearance([PATH_GREEN_DRAGON1_IMAGE, PATH_GREEN_DRAGON2_IMAGE])
            mygame.dragon.draw(screen)

        # update the flower position and redraw it
        mygame.flower_group.update()
        mygame.flower_group.draw(screen)

        # checks for any collisions between the flames, flowers, dragon, and the magma
        # if exists, then dragon die
        if mygame.dragon.check_collision_with_group(mygame.flame_group) \
                or mygame.dragon.check_collision_with_single(mygame.magma) \
                or mygame.dragon.check_collision_with_group(mygame.flower_group):
            if not sounds_off:
                mygame.play_sounds("dead")
            break

        # check if dragon and potion collide, if they collide, remove potion, play sounds and set potion_play equal true
        if mygame.dragon.check_collision_with_group(mygame.potion_group):
            if not sounds_off:
                mygame.play_sounds("potion")
            mygame.potion_group.remove(mygame.potion_group.sprites()[0])
            potion_play = True

        # if the dragon go through a pair of flames without the collision, then we update the game score
        for p in mygame.flame_group:
            if mygame.dragon.check_pass(p) and not p.is_passed:
                p.set_passed()
                mygame.get_score()
                if not sounds_off:
                    mygame.play_sounds("score")

        # draw the game score on the screen
        draw_text(screen, mygame.score, 50, 35)

        # update the sound icon
        if not sounds_off:
            screen.blit(sound_on_image, sounds_rect)
        else:
            screen.blit(sound_off_image, sounds_rect)

        # update the screen
        pygame.display.update()

    # when the dragon is dead (collision or off the screen), it "falls"
    while not mygame.dragon.is_off_screen():
        # redraw the background
        mygame.draw_bg(screen)

        # redraw the flames in the same place as when it died
        mygame.flame_group.update()
        mygame.flame_group.draw(screen)
        # draw the magma to get the rolling effect
        mygame.magma.update()
        mygame.magma.draw(screen)
        # make the dragon fall down and rotates it
        mygame.dragon.update()
        mygame.dragon.draw_dead(screen)

        # accelerate the game frame rate to create a rapid falling effect for the dragon
        mygame.set_frame_rate(FPS * 3)

        # update the sound icon
        if not sounds_off:
            screen.blit(sound_on_image, sounds_rect)
        else:
            screen.blit(sound_off_image, sounds_rect)

        # Updates the entire screen
        pygame.display.update()

    # Let's end the game!
    if not end_the_game(screen, mygame.score):
        main()
    else:
        pygame.display.quit()
        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    main()
