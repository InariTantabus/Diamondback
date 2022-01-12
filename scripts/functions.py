import pygame, random, math

class Snake:
    def __init__(self, segments, speed, color, w_color, fade_color=[False, [0, 0, 0]], direction={'right': True, 'left': False, 'up': False, 'down': False}):
        self.speed = speed
        self.move_timer = 0
        self.direction = direction
        self.color = color
        self.w_color = w_color
        self.segments = segments
        self.length = len(segments)-1
        self.fade_color = fade_color
    
    def draw(self, display):
        for i, segment in enumerate(self.segments):
            if self.fade_color[0]:
                if i <= 25:
                    temp_color = interpolateColor(self.color, self.fade_color[1], i/25)
                else:
                    temp_color = interpolateColor(self.color, self.fade_color[1], -i)
                draw(display, segment, (
                    (temp_color[0]-((temp_color[0]/25)*i) + abs(temp_color[0]-((temp_color[0]/25)*i)))/2,
                    (temp_color[1]-((temp_color[1]/25)*i) + abs(temp_color[1]-((temp_color[1]/25)*i)))/2,
                    (temp_color[2]-((temp_color[2]/25)*i) + abs(temp_color[2]-((temp_color[2]/25)*i)))/2))
            else:
                draw(display, segment, (
                    (self.color[0]-((self.color[0]/25)*i) + abs(self.color[0]-((self.color[0]/25)*i)))/2, 
                    (self.color[1]-((self.color[1]/25)*i) + abs(self.color[1]-((self.color[1]/25)*i)))/2, 
                    (self.color[2]-((self.color[2]/25)*i) + abs(self.color[2]-((self.color[2]/25)*i)))/2))
            if i == self.length:
                draw(display, segment, (self.color[0], self.color[1], self.color[2]))

    def move(self, apples, running, active_walls):
        if self.move_timer > 0:
            self.move_timer -= 1
        else:
            self.move_timer = int(60/self.speed)-1

            while len(self.segments)-1 < self.length:
                self.segments.append(self.segments[-1])

            for i in range(len(self.segments)-1, -1, -1):
                if i != 0:
                    self.segments[i] = self.segments[i-1].copy()

            if len(active_walls) > 0:
                for w in active_walls:
                    if self.segments[0] == w:
                        running = False

            for key in self.direction:
                if self.direction[key]:
                    if self.direction['up']:
                        if self.segments[0][1] > 0:
                            self.segments[0][1] -= 1
                        else:
                            running = False
                    if self.direction['left']:
                        if self.segments[0][0] > 0:
                            self.segments[0][0] -= 1
                        else:
                            running = False
                    if self.direction['down']:
                        if self.segments[0][1] < 19:
                            self.segments[0][1] += 1
                        else:
                            running = False
                    if self.direction['right']:
                        if self.segments[0][0] < 19:
                            self.segments[0][0] += 1
                        else:
                            running = False
    
            for i in range(0, len(self.segments)-1):
                if i != 0:
                    if self.segments[0] == self.segments[i]:
                        running = False

            if apples:
                for i, apple in sorted(enumerate(apples), reverse=True):
                    if self.segments[0] == apple.tile:
                        if apple.version == 'red':
                            self.length += 2
                        elif apple.version == 'gold':
                            self.length += 7
                        apples.pop(i)
                        apples.append(new_apple(self.segments))   

        return apples, running

    def update(self, display, direction, waves, speed=10, apples=[], active_walls=[], running=True):
        self.speed = speed
        temp_direction = self.direction.copy()
        for key in self.direction:
            if key == direction:
                self.direction[key] = True
            else:
                self.direction[key] = False
        if temp_direction != self.direction:
            temp_div = (2-self.length/80)
            if temp_div < 1:
                temp_div = 1
            waves.append([self.segments[0].copy(), 5, (self.w_color[0]/temp_div, self.w_color[1]/temp_div, self.w_color[2]/temp_div), 6])
        
        apples, running = self.move(apples, running, active_walls)
        self.draw(display)

        waves.append([self.segments[-1], 0, [self.w_color[0]/5, self.w_color[1]/5, self.w_color[2]/5], 1.5])

        if apples:
            return apples, running, waves
        else:
            return running, waves

class Apple:
    def __init__(self, tile, version='red'):
        self.update_timer = 0
        self.tile = tile
        self.version = version
        self.w_timer = 0
        self.w_timer_max = 20
        if self.version == 'red':
            self.color = [255, 0, 0]
            self.w_color = [100, 0, 0]
            self.w_size = 3
        if self.version == 'gold':
            self.color = [255, 255, 0]
            self.w_color = [100, 100, 0]
            self.w_size = 4

    def draw(self, display, snakehead, scroll):
        manh_dist = int(abs(self.tile[0]-snakehead[0]) + abs(self.tile[1]-snakehead[1]))
        if manh_dist <= 5:
            draw(display, self.tile, (
                ((self.color[0]-(self.color[0]/(5.1-manh_dist))) + abs(self.color[0]-(self.color[0]/(5.1-manh_dist))))/2, 
                ((self.color[1]-(self.color[1]/(5.1-manh_dist))) + abs(self.color[1]-(self.color[1]/(5.1-manh_dist))))/2, 
                ((self.color[2]-(self.color[2]/(5.1-manh_dist))) + abs(self.color[2]-(self.color[2]/(5.1-manh_dist))))/2), 13, scroll)

    def update(self, run_speed, waves, display, snakehead, scroll=[0, 0]):
        if self.update_timer > 0:
            self.update_timer -= 1
        else:
            self.update_timer = run_speed
            if self.w_timer > 0:
                self.w_timer -= 1
            else:
                self.w_timer = self.w_timer_max
                waves.append([self.tile, 0, self.w_color, self.w_size])
        
        self.draw(display, snakehead, scroll)

        return waves        

class WindowOBJ:
    def __init__(self, mainClock, WINDOW_SIZE, screen, display):
        self.mainClock = mainClock
        self.WINDOW_SIZE = WINDOW_SIZE
        self.screen = screen
        self.display = display
    
    def return_items(self):
        return self.mainClock, self.WINDOW_SIZE, self.screen, self.display


class FreeSnake:
    def __init__(self, segments, speed, color, w_color, fade_color=[False, [0, 0, 0]], direction={'right': True, 'left': False, 'up': False, 'down': False}):
        self.speed = speed
        self.move_timer = 0
        self.direction = direction
        self.color = color
        self.w_color = w_color
        self.fade_color = fade_color
        self.segments = segments
        self.length = len(segments)-1
    
    def draw(self, display, scroll):
        for i, segment in enumerate(self.segments):
            if abs(self.segments[i][0]-self.segments[0][0]) <= 36:
                if abs(self.segments[i][1]-self.segments[0][1]) <= 22:
                    if self.fade_color[0]:
                        if i <= max(25, (self.length)/4):
                            temp_color = interpolateColor(self.color, self.fade_color[1], i/25)
                        else:
                            temp_color = interpolateColor(self.color, self.fade_color[1], -i)
                        temp_value = max(25, (self.length)/4)
                        draw(display, segment, (
                            (temp_color[0]-((temp_color[0]/temp_value)*i) + abs(temp_color[0]-((temp_color[0]/temp_value)*i)))/2,
                            (temp_color[1]-((temp_color[1]/temp_value)*i) + abs(temp_color[1]-((temp_color[1]/temp_value)*i)))/2,
                            (temp_color[2]-((temp_color[2]/temp_value)*i) + abs(temp_color[2]-((temp_color[2]/temp_value)*i)))/2), 13, scroll)
                    else:
                        draw(display, segment, (
                            (self.color[0]-((self.color[0]/temp_value)*i) + abs(self.color[0]-((self.color[0]/temp_value)*i)))/2, 
                            (self.color[1]-((self.color[1]/temp_value)*i) + abs(self.color[1]-((self.color[1]/temp_value)*i)))/2, 
                            (self.color[2]-((self.color[2]/temp_value)*i) + abs(self.color[2]-((self.color[2]/temp_value)*i)))/2), 13, scroll)
                    if i == self.length:
                        draw(display, segment, (self.color[0], self.color[1], self.color[2]), 13, scroll)

    def move(self, apples, walls, running):
        if self.move_timer > 0:
            self.move_timer -= 1
        else:
            self.move_timer = int(60/self.speed)-1

            while len(self.segments)-1 < self.length:
                self.segments.append(self.segments[-1])

            for i in range(len(self.segments)-1, -1, -1):
                if i != 0:
                    self.segments[i] = self.segments[i-1].copy()

            for key in self.direction:
                if self.direction[key]:
                    if self.direction['up']:
                        self.segments[0][1] -= 1
                    if self.direction['left']:
                        self.segments[0][0] -= 1
                    if self.direction['down']:
                        self.segments[0][1] += 1
                    if self.direction['right']:
                        self.segments[0][0] += 1

            if self.segments[0] in self.segments[1:] or self.segments[0] in walls:
                running = False

            if apples:
                for i, apple in sorted(enumerate(apples), reverse=True):
                    if self.segments[0] == apple.tile:
                        if apple.version == 'red':
                            self.length += 2
                        elif apple.version == 'gold':
                            self.length += 7
                        apples.pop(i)
                        apples.append(new_apple(self.segments, [self.segments[0][0]-10, self.segments[0][1]-10]))   

        return apples, running

    def update(self, display, direction, waves, scroll, speed=10, apples=[], walls=[], running=True):
        self.speed = speed
        temp_direction = self.direction.copy()
        for key in self.direction:
            if key == direction:
                self.direction[key] = True
            else:
                self.direction[key] = False
        if temp_direction != self.direction:
            temp_div = (2-self.length/80)
            if temp_div < 1:
                temp_div = 1
            waves.append([self.segments[0].copy(), 4, (self.w_color[0]/temp_div, self.w_color[1]/temp_div, self.w_color[2]/temp_div), 7])
        
        apples, running = self.move(apples, walls, running)
        self.draw(display, scroll)

        waves.append([self.segments[-1], 0, [self.w_color[0]/10, self.w_color[1]/10, self.w_color[2]/10], 1.5])

        if apples:
            return apples, running, waves
        else:
            return running, waves
   


def new_apple(snake, pos=[0, 0], size=20):
    if pos[1] < -74:
        pos[1] = -74
    if pos[1] > 73:
        pos[1] = 53
    if pos[0] < -99:
        pos[0] = -99
    if pos[0] > 98:
        pos[0] = 78

    test = True
    while test:
        keys = []
        apple_x = pos[0] + random.randint(0, size-1)
        apple_y = pos[1] + random.randint(0, size-1)

        check = False
        if apple_x in [0, 19] and apple_y in [0, 19]:
            if random.randint(0, 1) == 0:
                check = False
        for segment in snake:
            if (apple_x == segment[0] and apple_y == segment[1]):
                check = True
        if not check:
            test = False
    gold_chance = random.randint(0, 5)
    if gold_chance == 1:
        return Apple([apple_x, apple_y], 'gold')
    else:
        return Apple([apple_x, apple_y], 'red')

def draw(display, tile, color, size=13, scroll=[0, 0]):
    temp_rect = pygame.Rect(tile[0]*15+(15-size)/2-scroll[0], tile[1]*15+(15-size)/2-scroll[1], size, size)
    pygame.draw.rect(display, color, temp_rect)

def free_draw_wave(pos, stage, wave_list, wave):
    target_tiles = []
    for i in range(round(wave[3]*2+1)):
        for v in range(round(wave[3]*2+1)):
            temp_pos = [0, 0]
            temp_pos[0] = pos[0]+i-int(round(wave[3]*2+1)/2)
            temp_pos[1] = pos[1]+v-int(round(wave[3]*2+1)/2)
            manh_dist = abs(pos[0]-temp_pos[0]) + abs(temp_pos[1]-pos[1])
            if manh_dist < stage:
                target_tiles.append([int(pos[0]+i-int(round(wave[3]*2+1)/2)), int(pos[1]+v-int(round(wave[3]*2+1)/2))])
    
    for i, tile in enumerate(target_tiles):
        if str(tile[0]) + ':' + str(tile[1]) not in wave_list:
            wave_list[str(tile[0]) + ':' + str(tile[1])] = [tile[0], tile[1], [1, 1, 1]]
        target_tiles[i] = str(tile[0]) + ':' + str(tile[1])
    
    for key in target_tiles:
        manh_dist = abs(pos[0]-wave_list[key][0]) + abs(wave_list[key][1]-pos[1])
        if manh_dist <= stage:
            
            if wave[2][0] > 0:
                if not (wave_list[key][2][0] + (5*((manh_dist+1)-manh_dist) / (wave[2][0]/(wave[2][0]/1.5))) * (wave[3]/(wave[3]/1.5)) / (manh_dist+1) > wave[2][0] / (manh_dist+1)):
                    if not (wave_list[key][2][0] + (5*((manh_dist+1)-manh_dist) / (wave[2][0]/(wave[2][0]/1.5))) * (wave[3]/(wave[3]/1.5)) / (manh_dist+1) < wave_list[key][2][0]):
                        wave_list[key][2][0] += (5*((manh_dist+1)-manh_dist) / (wave[2][0]/(wave[2][0]/1.5))) * (wave[3]/(wave[3]/1.5)) / (manh_dist+1)

            if wave[2][1] > 0:
                if not (wave_list[key][2][1] + (5*((manh_dist+1)-manh_dist) / (wave[2][1]/(wave[2][1]/1.5))) * (wave[3]/(wave[3]/1.5)) / (manh_dist+1) > wave[2][1] / (manh_dist+1)):
                    if not (wave_list[key][2][1] + (5*((manh_dist+1)-manh_dist) / (wave[2][1]/(wave[2][1]/1.5))) * (wave[3]/(wave[3]/1.5)) / (manh_dist+1) < wave_list[key][2][1]):
                        wave_list[key][2][1] += (5*((manh_dist+1)-manh_dist) / (wave[2][1]/(wave[2][1]/1.5))) * (wave[3]/(wave[3]/1.5)) / (manh_dist+1)

            if wave[2][2] > 0:
                if not (wave_list[key][2][2] + (5*((manh_dist+1)-manh_dist) / (wave[2][2]/(wave[2][2]/1.5))) * (wave[3]/(wave[3]/1.5)) / (manh_dist+1) > wave[2][2] / (manh_dist+1)):
                    if not (wave_list[key][2][2] + (5*((manh_dist+1)-manh_dist) / (wave[2][2]/(wave[2][2]/1.5))) * (wave[3]/(wave[3]/1.5)) / (manh_dist+1) < wave_list[key][2][2]):
                        wave_list[key][2][2] += (5*((manh_dist+1)-manh_dist) / (wave[2][2]/(wave[2][2]/1.5))) * (wave[3]/(wave[3]/1.5)) / (manh_dist+1)

    return wave_list

def draw_wave(pos, stage, wave_list, wave):
    for tile in wave_list:
        manh_dist = abs(pos[0]-tile[0]) + abs(tile[1]-pos[1])
        if manh_dist <= stage:
            
            if wave[2][0] > 0:
                if not (tile[2][0] + (5*((manh_dist+1)-manh_dist) / (wave[2][0]/(wave[2][0]/1.5))) * (wave[3]/(wave[3]/1.5)) / (manh_dist+1) > wave[2][0] / (manh_dist+1)):
                    if not (tile[2][0] + (5*((manh_dist+1)-manh_dist) / (wave[2][0]/(wave[2][0]/1.5))) * (wave[3]/(wave[3]/1.5)) / (manh_dist+1) < tile[2][0]):
                        tile[2][0] += (5*((manh_dist+1)-manh_dist) / (wave[2][0]/(wave[2][0]/1.5))) * (wave[3]/(wave[3]/1.5)) / (manh_dist+1)

            if wave[2][1] > 0:
                if not (tile[2][1] + (5*((manh_dist+1)-manh_dist) / (wave[2][1]/(wave[2][1]/1.5))) * (wave[3]/(wave[3]/1.5)) / (manh_dist+1) > wave[2][1] / (manh_dist+1)):
                    if not (tile[2][1] + (5*((manh_dist+1)-manh_dist) / (wave[2][1]/(wave[2][1]/1.5))) * (wave[3]/(wave[3]/1.5)) / (manh_dist+1) < tile[2][1]):
                        tile[2][1] += (5*((manh_dist+1)-manh_dist) / (wave[2][1]/(wave[2][1]/1.5))) * (wave[3]/(wave[3]/1.5)) / (manh_dist+1)

            if wave[2][2] > 0:
                if not (tile[2][2] + (5*((manh_dist+1)-manh_dist) / (wave[2][2]/(wave[2][2]/1.5))) * (wave[3]/(wave[3]/1.5)) / (manh_dist+1) > wave[2][2] / (manh_dist+1)):
                    if not (tile[2][2] + (5*((manh_dist+1)-manh_dist) / (wave[2][2]/(wave[2][2]/1.5))) * (wave[3]/(wave[3]/1.5)) / (manh_dist+1) < tile[2][2]):
                        tile[2][2] += (5*((manh_dist+1)-manh_dist) / (wave[2][2]/(wave[2][2]/1.5))) * (wave[3]/(wave[3]/1.5)) / (manh_dist+1)

    return wave_list

def check_edge(snake_list, edge_time, walls):
    if snake_list[0][0] < 4+(walls)/3 or snake_list[0][0] > 15-(walls)/3 or snake_list[0][1] < 4+(walls)/3 or snake_list[0][1] > 15-(walls)/3:
        edge_time += 1
    else:
        edge_time -= 2
    if edge_time < -50:
        edge_time = -50
    
    walls = edge_time/(50)
    return edge_time, walls

def interpolateColor(color1, color2, factor):
    result = color1.copy()
    for i in range(3):
        result[i] = round(result[i]+factor*(color2[i]-color1[i]))
        if result[i] > 255:
            result[i] = 255
        if result[i] < 0:
            result[i] = 0
    return result
