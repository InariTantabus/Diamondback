import pygame, sys, os, random, math

import scripts.text as text
import scripts.functions as f
import scripts.classic as classic
import scripts.spring as spring
from pygame.locals import *

def window_setup():
    #----------------Setup pygame/window----------------#
    mainClock = pygame.time.Clock()
    pygame.init()
    pygame.display.quit()
    pygame.display.init()
    pygame.display.set_caption('Snake Game')

    WINDOW_SIZE = (600, 600)
    screen = pygame.display.set_mode(WINDOW_SIZE, pygame.SCALED + pygame.RESIZABLE)
    display = pygame.Surface((300, 300))

    pygame.mouse.set_visible(True)
    #----------------Setup pygame/window----------------#
    return mainClock, WINDOW_SIZE, screen, display

def run_classic(run_speed):
    classic.window_setup(run_speed)
    mainClock, WINDOW_SIZE, screen, display = window_setup()
    return mainClock, WINDOW_SIZE, screen, display

def run_game():
    spring.window_setup()
    mainClock, WINDOW_SIZE, screen, display = window_setup()
    return mainClock, WINDOW_SIZE, screen, display

def main_menu():
    mainClock, WINDOW_SIZE, screen, display = window_setup()

    font = text.Font('data/fonts/large_font.png', (200, 200, 200))
    s_font = text.Font('data/fonts/small_font.png', (200, 200, 200))
    green_font = text.Font('data/fonts/large_font.png', (0, 200, 0))

    snake_list = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9], [0, 10], [0, 11], [0, 12], [0, 13], [0, 14], [0, 15], [0, 16], [0, 17], [0, 18], [0, 19], [1, 19], [2, 19], [3, 19], [4, 19], [5, 19], [6, 19], [7, 19], [8, 19], [9, 19], [10, 19], [11, 19], [12, 19], [13, 19], [14, 19], [15, 19], [16, 19], [17, 19], [18, 19], [19, 19]]
    snake_direction = 'right'
    run_speed = 10
    snake_timer = int(60/run_speed)-1
    snake_turn_timer = 18

    click = False

    waves = [] # start coords, timer, red, green, blue, length
    wave_tiles = []
    for i in range(0, 20):
        for v in range(0, 20):
            wave_tiles.append([i, v, [0, 0, 0]])
    wave_timer = 30

    anti_wave_rects = [
        [pygame.Rect((display.get_width()-font.width('Snake'))/2-12, 39, font.width('Snake')+25, 35), True],
        [pygame.Rect((display.get_width()-font.width('Snake'))/2-11, 40, font.width('Snake')+23, 33), False],
        [pygame.Rect(75, 189, 147, 45), True],
        [pygame.Rect(76, 190, 145, 43), False]]

    classic_outline_rect = pygame.Rect(110, 100, 80, 30)
    classic_rect = pygame.Rect(111, 101, 78, 28)
    endless_outline_rect = pygame.Rect(110, 140, 80, 30)
    endless_rect = pygame.Rect(111, 141, 78, 28)

    snake = f.Snake(snake_list, 10, [0, 255, 0], [0, 255, 255])
    waves.append([snake.segments[0].copy(), 2, (0, 255, 255), 6])

    while True:
        display.fill((0, 0, 0))
        mx, my = pygame.mouse.get_pos()
        mx /= 2
        my /= 2

        if wave_timer > 0:
            wave_timer -= 1
        else:
            wave_timer = 90
            wave_start = [random.randint(1, 18), random.randint(1, 18)]
            waves.append([wave_start, 0, [0, 255, 255], 10])

        for tile in wave_tiles:
            for i in range(0, 3):
                if tile[2][i] > 0:
                    tile[2][i] -= tile[2][i]/20
                if tile[2][i] < 0:
                    tile[2][i] = 0
                if tile[2][i] > 255:
                    tile[2][i] = 255
            f.draw(display, tile, (tile[2][0], tile[2][1], tile[2][2]), 9)

        if len(waves) > 0:
            for i, wave in sorted(enumerate(waves), reverse=True):
                wave_tiles = f.draw_wave(wave[0], wave[1], wave_tiles, wave)
                wave[1] += .5/6
                if wave[1] > wave[3]:
                    waves.pop(i)

        for anti in anti_wave_rects:
            if anti[1]:
                pygame.draw.rect(display, (0, 200, 0), anti[0])
            else:
                pygame.draw.rect(display, (10, 10, 10), anti[0])

        green_font.render('Snake', display, ((display.get_width()-font.width('Snake'))/2, 50))
        s_font.render('Scroll to adjust speed - {} -'.format(run_speed), display, ((display.get_width()-s_font.width('Scroll to adjust speed - {} -'.format(run_speed)))/2, 200))
        s_font.render("Press 'esc' to return to this menu", display, ((display.get_width()-s_font.width("Press 'esc' to return to this menu"))/2, 215))

        pygame.draw.rect(display, (0, 200, 0), classic_outline_rect)
        pygame.draw.rect(display, (0, 200, 0), endless_outline_rect)
        
        if classic_rect.collidepoint(mx, my):
            pygame.draw.rect(display, (30, 30, 30), classic_rect)
            if click:
                mainClock, WINDOW_SIZE, screen, display = run_classic(run_speed)
        else:
            pygame.draw.rect(display, (10, 10, 10), classic_rect)
        if endless_rect.collidepoint(mx, my):
            pygame.draw.rect(display, (30, 30, 30), endless_rect)
            if click:
                mainClock, WINDOW_SIZE, screen, display = run_game()
        else:
            pygame.draw.rect(display, (10, 10, 10), endless_rect)

        font.render('Classic', display, ((display.get_width()-font.width('Classic'))/2, 109))
        font.render('Freeplay', display, ((display.get_width()-font.width('Freeplay'))/2, 149))

        temp = snake.update(display, snake_direction, waves, run_speed)
        
        if snake_timer > 0:
            snake_timer -= 1
        else:
            snake_timer = int(60/run_speed)-1
            if snake_turn_timer > 0:
                snake_turn_timer -= 1
            else:
                waves.append([snake.segments[0].copy(), 2, (0, 255, 255), 6])
                snake_turn_timer = 18
                if snake_direction == 'right':
                    snake_direction = 'down'
                elif snake_direction == 'down':
                    snake_direction = 'left'
                elif snake_direction == 'left':
                    snake_direction = 'up'
                elif snake_direction == 'up':
                    snake_direction = 'right'

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                if event.button == 4:
                    run_speed += 1
                    if run_speed > 30:
                        run_speed = 30
                if event.button == 5:
                    run_speed -= 1
                    if run_speed < 5:
                        run_speed = 5

        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
        pygame.display.update()
        mainClock.tick(60)

main_menu()
