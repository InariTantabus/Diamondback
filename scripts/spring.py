import pygame, sys, os, random, math, time

import scripts.text as text
import scripts.functions as f

from pygame.locals import *

def window_setup():
    #----------------Setup pygame/window----------------#
    mainClock = pygame.time.Clock()
    pygame.init()
    pygame.display.quit()
    pygame.display.init()
    pygame.display.set_caption('Classic Snake')

    WINDOW_SIZE = (1680, 945)
    screen = pygame.display.set_mode(WINDOW_SIZE, pygame.SCALED + pygame.RESIZABLE + pygame.FULLSCREEN)
    display = pygame.Surface((1680/2, 945/2))
    #----------------Setup pygame/window----------------#
    window_obj = f.WindowOBJ(mainClock, WINDOW_SIZE, screen, display)
    pygame.mouse.set_visible(False)

    spring(window_obj)

def spring(window_obj, play_again=True):
    if not play_again:
        return
    mainClock, WINDOW_SIZE, screen, display = window_obj.return_items()

    walls = []
    close_walls = []
    for i in range(200):
        walls.append([i-100, -75])
    for i in range(200):
        walls.append([i-100, +74])
    for i in range(150):
        walls.append([-100, i-75])
    for i in range(150):
        walls.append([+99, i-75])

    s_font = text.Font('data/fonts/small_font.png', (150, 200, 200))
    font = text.Font('data/fonts/large_font.png', (150, 200, 200))

    player_direction = 'right'
    player = f.FreeSnake([[2, 10], [1, 10], [0, 10]], 10, [0, 255, 0], [0, 255, 255], [True, [0, 255, 255]])
    waves = [] # start coords, timer, red, green, blue, length
    arrows = [] # pos, target, color
    wave_tiles = {} # x:y: [x, y, [red, green, blue]]
    true_scroll = [0, 0]
    true_scroll[0] = (player.segments[0][0]*15 - (1680 + 15) / 4)
    true_scroll[1] = (player.segments[0][1]*15 - (945 + 15) / 4)
    run_speed = 10
    to_delete = []

    apples = []
    apples.append(f.new_apple(player.segments))
    running = True
    while running:
        display.fill((0, 0, 0))
        true_scroll[0] += (player.segments[0][0]*15 - true_scroll[0] - (1680 + 15) / 4) / 40
        true_scroll[1] += (player.segments[0][1]*15 - true_scroll[1] - (945 + 15) / 4) / 30

        if not player.move_timer:
            change = False # lets you input a new direction only after the snake moves

        if wave_tiles:
            to_delete = []
            for key in wave_tiles:
                temp_counter = 0
                for i in range(0, 3):
                    if wave_tiles[key][2][i] > 0:
                        if player.move_timer == 0:
                            wave_tiles[key][2][i] -= wave_tiles[key][2][i]/15
                    if wave_tiles[key][2][i] < 1:
                        temp_counter += 1
                    if wave_tiles[key][2][i] > 255:
                        wave_tiles[key][2][i] = 255
                
                if temp_counter >= 3: 
                    to_delete.append(key)

                f.draw(display, wave_tiles[key], (wave_tiles[key][2][0], wave_tiles[key][2][1], wave_tiles[key][2][2]), 9, true_scroll)

        if to_delete:
            for val in to_delete:
                if val in wave_tiles:
                    del wave_tiles[val]

        if waves:
            for i, wave in sorted(enumerate(waves), reverse=True):
                wave_tiles = f.free_draw_wave(wave[0], wave[1], wave_tiles, wave)
                if player.move_timer == 0:
                    wave[1] += .5
                    if wave[1] > wave[3]:
                        waves.pop(i)

        apple, running, waves = player.update(display, player_direction, waves, true_scroll, run_speed, apples, close_walls)

        if apples:
            for apple in apples:
                waves = apple.update(run_speed, waves, display, player.segments[0], true_scroll)
                if len(arrows) > 0:
                    for arrow in arrows:
                        arrow.update((player.segments[0][0]*15-true_scroll[0]+7.5, player.segments[0][1]*15-true_scroll[1]+7.5), (apple.tile[0]*15-true_scroll[0]+7.5, apple.tile[1]*15-true_scroll[1]+7.5), apple.color, display)
                else:
                    arrows.append(Arrow((player.segments[0][0]*15-true_scroll[0]+7.5, player.segments[0][1]*15-true_scroll[1]+7.5), (apple.tile[0]*15-true_scroll[0]+7.5, apple.tile[1]*15-true_scroll[1]+7.5), apple.color, display))

        if (player.segments[0][0] <= -68) or (player.segments[0][0] >= 68) or (player.segments[0][1] <= -55) or (player.segments[0][1] >= 55):
            close_walls = []
            if walls:
                for wall in walls:
                    if abs(wall[0]-player.segments[0][0]) <= 36:
                        if abs(wall[1]-player.segments[0][1]) <= 22:
                            close_walls.append(wall)
                            f.draw(display, wall, (100, 100, 100), 15, true_scroll)

        font.render('LENGTH: {}'.format(player.length+1), display, (30, 15))
            # font.render('X {}'.format(player.segments[0][0]), display, (30, 15)) ## Coords
            # font.render('Y {}'.format(player.segments[0][1]), display, (30, 30))
        fps = round(mainClock.get_fps())
        font.render('FPS: {}'.format(fps), display, (30, 30))

        play_again = True
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                pass
                # apples.append(f.new_apple(player.segments, [player.segments[0][0]-10, player.segments[0][1]-10]))
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    play_again = False
                if event.key == K_w:
                    if player_direction != 'down' and not change:
                        player_direction = 'up'
                        change = True
                if event.key == K_a:
                    if player_direction != 'right' and not change:
                        player_direction = 'left'
                        change = True
                if event.key == K_s:
                    if player_direction != 'up' and not change:
                        player_direction = 'down'
                        change = True
                if event.key == K_d:
                    if player_direction != 'left' and not change:
                        player_direction = 'right'
                        change = True

        screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
        pygame.display.update()
        mainClock.tick(60)
    if not play_again:
        return

def find_arrow_points(pos, rot, size):
    points = []
    rot = -rot

    dist = 5*size
    points.append((pos[0]+dist*math.cos(rot), pos[1]-dist*math.sin(rot)))
    
    dist = math.hypot(155-150, 155-150)*size ## sqrt(50)
    angle = (rot+math.atan2(155-150, 155-150))%(2*math.pi)
    points.append((pos[0]-dist*math.cos(angle), pos[1]+dist*math.sin(angle)))

    dist = -2.5*size
    points.append((pos[0]+dist*math.cos((rot)%(2*math.pi)), pos[1]-dist*math.sin(rot)))

    dist = math.hypot(155-150, 155-150)*size
    angle = (rot+math.atan2(155-150, 145-150))%(2*math.pi)
    points.append((pos[0]+dist*math.cos(angle), pos[1]-dist*math.sin(angle)))

    return points

class Arrow:
    def __init__(self, pos, target, color, surf):
        self.x = pos[0]
        self.y = pos[1]
        self.update(pos, target, color, surf)
    
    def draw(self, surf):
        points = find_arrow_points((self.off_x, self.off_y), self.rot, self.size)
        pygame.draw.polygon(surf, self.color, points)

    def update(self, pos, target, color, surf):
        self.color = color
        self.x += (pos[0]-self.x)/10
        self.y += (pos[1]-self.y)/10
        self.rot = math.atan2(target[1]-self.y, target[0]-self.x)
        self.off_x = self.x+30*math.cos(self.rot)
        self.off_y = self.y+30*math.sin(self.rot)

        self.size = 1
        if self.size > 2:
            self.size = 2
        elif self.size < 1:
            self.size = 1

        if not math.sqrt(abs(pos[0]-target[0])**2 + abs(pos[1]-target[1])**2) < (30*10):
            self.draw(surf)
