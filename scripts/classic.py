import pygame, sys, os, random, math

import scripts.text as text
import scripts.functions as f

from pygame.locals import *

def window_setup(run_speed):
    #----------------Setup pygame/window----------------#
    mainClock = pygame.time.Clock()
    pygame.init()
    pygame.display.quit()
    pygame.display.init()
    pygame.display.set_caption('Classic Snake')

    WINDOW_SIZE = (600, 600)
    screen = pygame.display.set_mode(WINDOW_SIZE, pygame.SCALED + pygame.RESIZABLE)
    display = pygame.Surface((300, 300))
    #----------------Setup pygame/window----------------#
    window_obj = f.WindowOBJ(mainClock, WINDOW_SIZE, screen, display)
    pygame.mouse.set_visible(False)

    classic(window_obj, run_speed)

def classic(window_obj, run_speed=10, play_again=True):
    if not play_again:
        return
    mainClock, WINDOW_SIZE, screen, display = window_obj.return_items()

    edge_time = 0
    snake_list = [[2, 10], [1, 10], [0, 10]]
    snake_direction = 'right'
    apples = []
    walls = -20
    active_walls = []
    waves = [] # start coords, timer, red, green, blue, length
    wave_tiles = []
    wave_timer = 1800/run_speed 
    for i in range(0, 20):
        for v in range(0, 20):
            wave_tiles.append([i, v, [0, 0, 0]])

    temp_color = [0, 0, 0]
    for i, col in enumerate(temp_color):
        test = True
        while test:
            temp_color[i] = random.randint(20, 255)
            if i == 0:
                temp_value = temp_color[i]
                test = False
            elif i == 1:
                if abs(temp_value-temp_color[i]) >= 30:
                    temp_value2 = temp_color[i]
                    test = False
            elif i == 2:
                if abs(temp_value-temp_color[i]) >= 30 and abs(temp_value2-temp_color[i]) >= 30:
                    test = False
    temp_color3 = [0, 0, 0]
    for i, col in enumerate(temp_color3):
        test = True
        while test:
            temp_color3[i] = random.randint(20, 255)
            if i == 0:
                temp_value = temp_color3[i]
                test = False
            elif i == 1:
                if abs(temp_value-temp_color3[i]) >= 30:
                    temp_value2 = temp_color3[i]
                    test = False
            elif i == 2:
                if abs(temp_value-temp_color3[i]) >= 30 and abs(temp_value2-temp_color3[i]) >= 30:
                    test = False
    temp_color2 = f.interpolateColor(temp_color, temp_color3, .5)
    check = True
    for i, col in enumerate(temp_color2):
        if i == 0:
            temp_value = temp_color2[0]
        elif i == 1:
            if abs(temp_color2[1]-temp_color2[0] >= 30):
                temp_value2 = temp_color2[1]
            else:
                check = False
        elif i == 2:
            if not (abs(temp_color2[2]-temp_color2[0] >= 30) or abs(temp_color2[2]-temp_color2[1] >= 30)):
                check = False
    if not check:
        temp_value = random.randint(0, 1)
        if temp_value == 1:
            temp_color2 = temp_color.copy()
        else:
            temp_color2 = temp_color3.copy()
    
    snake = f.Snake(snake_list, run_speed, temp_color, temp_color2, [True, temp_color3])
    apples.append(f.new_apple(snake_list))
    running = True
    while running:
        display.fill((0, 0, 0))

        if snake.move_timer == 0:
            active_walls = []
            if int(walls) > 0:
                for wall in range(int(walls)):
                    for i in range(20):
                        for v in range(2):
                            active_walls.append([i, v*(19-(2*wall+1)+1)+int(wall+1)-1])
                            active_walls.append([i, v*(19-(2*wall+1)+1)+int(wall+1)-1])
                    for i in range(2):
                        for v in range(20):
                            active_walls.append([i*(19-(2*wall+1)+1)+int(wall+1)-1, v])
                            active_walls.append([i*(19-(2*wall+1)+1)+int(wall+1)-1, v])

            if wave_timer > 0:
                wave_timer -= 1
            else:
                wave_timer = 1800/run_speed
                wave_start = [random.randint(1, 18), random.randint(1, 18)]
                waves.append([wave_start, 0, [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)], 2.5])

            edge_time, walls = f.check_edge(snake.segments, edge_time, walls)
            change = False

        if walls > 0:
            for i in range(20):
                for v in range(2):
                    f.draw(display, [i, v*(19-(2*walls)+2)+walls-1], (100, 100, 100), 15)
                    f.draw(display, [i, v*(19-(2*walls)+2)+walls-1], (0, 0, 0), 5)
            for i in range(2):
                for v in range(20):
                    f.draw(display, [i*(19-(2*walls)+2)+walls-1, v], (100, 100, 100), 15)
                    f.draw(display, [i*(19-(2*walls)+2)+walls-1, v], (0, 0, 0), 5)

        for wall in active_walls:
            f.draw(display, wall, (100, 100, 100), 15)
            f.draw(display, wall, (0, 0, 0), 5)

        for tile in wave_tiles:
            for i in range(0, 3):
                if tile[2][i] > 0:
                    if snake.move_timer == 0:
                        tile[2][i] -= tile[2][i]/15
                if tile[2][i] < 0:
                    tile[2][i] = 0
                if tile[2][i] > 255:
                    tile[2][i] = 255
            f.draw(display, tile, (tile[2][0], tile[2][1], tile[2][2]), 9)

        if len(waves) > 0:
            for i, wave in sorted(enumerate(waves), reverse=True):
                wave_tiles = f.draw_wave(wave[0], wave[1], wave_tiles, wave)
                if snake.move_timer == 0:
                    wave[1] += .5
                    if wave[1] > wave[3]:
                        waves.pop(i)

        apple, running, waves = snake.update(display, snake_direction, waves, run_speed, apples, active_walls)

        for apple in apples:
            waves = apple.update(run_speed, waves, display, snake.segments[0])

        play_again = True
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                pass
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    play_again = False
                if event.key == K_w:
                    if snake_direction != 'down' and not change:
                        snake_direction = 'up'
                        change = True
                if event.key == K_a:
                    if snake_direction != 'right' and not change:
                        snake_direction = 'left'
                        change = True
                if event.key == K_s:
                    if snake_direction != 'up' and not change:
                        snake_direction = 'down'
                        change = True
                if event.key == K_d:
                    if snake_direction != 'left' and not change:
                        snake_direction = 'right'
                        change = True

        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
        pygame.display.update()
        mainClock.tick(60)
    if play_again:
        death_menu(snake.length+1, run_speed, window_obj)
        return
    else:
        return

def death_menu(length, run_speed, window_obj):
    mainClock, WINDOW_SIZE, screen, display = window_obj.return_items()

    running = True
    play_again = False
    font = text.Font('data/fonts/large_font.png', (200, 200, 200))
    red_font = text.Font('data/fonts/large_font.png', (200, 0, 0))
    timer = 20

    snake_list = [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9], [0, 10], [0, 11], [0, 12], [0, 13], [0, 14], [0, 15], [0, 16], [0, 17], [0, 18], [0, 19], [1, 19], [2, 19], [3, 19], [4, 19], [5, 19], [6, 19], [7, 19], [8, 19], [9, 19], [10, 19], [11, 19], [12, 19], [13, 19], [14, 19], [15, 19], [16, 19], [17, 19], [18, 19], [19, 19]]
    snake_direction = 'right'
    snake_timer = int(60/run_speed)-1
    snake_turn_timer = 18

    waves = [] # start coords, timer, red, green, blue, length
    wave_tiles = []
    for i in range(0, 20):
        for v in range(0, 20):
            wave_tiles.append([i, v, [0, 0, 0]])
    wave_timer = 30

    anti_wave_rects = [
        [pygame.Rect(42, 39, 219, 87), True],
        [pygame.Rect(43, 40, 217, 85), False],
        [pygame.Rect(64, 189, 172, 54), True],
        [pygame.Rect(65, 190, 170, 52), False]]

    snake = f.Snake(snake_list, 10, [255, 255, 0], [255, 255, 0], [True, [255, 0, 0]])
    waves.append([snake.segments[0].copy(), 2, (255, 255, 0), 6])

    while running:
        display.fill((0, 0, 0))
        if timer > 0:
            timer -= 1 
        if wave_timer > 0:
            wave_timer -= 1
        else:
            wave_timer = 90
            wave_start = [random.randint(1, 18), random.randint(1, 18)]
            waves.append([wave_start, 0, [255, 255, 0], 10])

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
                pygame.draw.rect(display, (255, 255, 0), anti[0])
            else:
                pygame.draw.rect(display, (10, 10, 10), anti[0])

        red_font.render('You Died', display, (125, 50))
        font.render('Your snake was {} tiles long'.format(length), display, (53, 70))
        font.render('Press any key to try again', display, (64, 100))
        font.render('Scroll to adjust speed', display, (75, 200))
        font.render('- {} -'.format(run_speed), display, (133, 220))
        
        temp, waves = snake.update(display, snake_direction, waves, run_speed)
        
        if snake_timer > 0:
            snake_timer -= 1
        else:
            snake_timer = int(60/run_speed)-1
            if snake_turn_timer > 0:
                snake_turn_timer -= 1
            else:
                snake_turn_timer = 18
                waves.append([snake.segments[0].copy(), 2, (255, 255, 0), 6])
                if snake_direction == 'right':
                    snake_direction = 'down'
                elif snake_direction == 'down':
                    snake_direction = 'left'
                elif snake_direction == 'left':
                    snake_direction = 'up'
                elif snake_direction == 'up':
                    snake_direction = 'right'
           
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                play_again = False
                if event.key == K_ESCAPE:
                    running = False
                else:
                    if timer == 0:
                        running = False
                        play_again = True
                        classic(window_obj, run_speed)
            if event.type == MOUSEBUTTONDOWN:
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
    if not play_again:
        return
    else:
        classic(window_obj, run_speed, False)
        return
