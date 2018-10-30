import game_framework
import math
import random
from pico2d import *


import game_world

# Boy Run Speed
# fill expressions correctly
PIXEL_PER_METER = (10.0 / 0.3) # 10pixel 30cm
RUN_SPEED_KMPH = 20.0 #km / hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_CIRCLE = 0.5
CIRCLE_PER_TIME = 1.0 / TIME_PER_CIRCLE
FRAMES_PER_DEGREE = 360

# fill expressions correctly
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


class Ghost:
    image = None
    def __init__(self, x, y, dir):
        self.x, self.y = x, y
        if Ghost.image == None:
            self.image = load_image('animation_sheet.png')
        self.dir = dir
        self.x_velocity = 0.0
        self.y_velocity = 0.0
        self.frame = 0
        self.rx, self.ry = x,y +100
        self.degree = dir * 3.141592 / 2
        self.opacify = 0.01
        self.wakeup = False


    def update(self):
        if self.wakeup is False :
            self.opacify +=  game_framework.frame_time / 4.0
            self.degree = self.degree + game_framework.frame_time * -self.dir * 3.141592 / 2 / 3.9

            if self.opacify >= 1:
                self.opacify = 1
                self.wakeup = True
        else:
            temp = random.randint(0,1)
            if temp == 0 or self.opacify == 1:
                self.opacify -= 0.05;
            elif temp == 1 or self.opacify == 0:
                self.opacify += 0.05;

            self.degree += 360.0 * game_framework.frame_time / 0.5
            self.x_velocity = 100 * math.cos(self.degree * 3.14 / 180)
            self.y_velocity = 100 * math.sin(self.degree * 3.14 / 180)
            self.x = self.rx + self.x_velocity
            self.y = self.ry + self.y_velocity


    def draw(self):
        self.image.opacify(self.opacify)
        if(self.wakeup is False):
            if self.dir == 1:
                self.image.clip_composite_draw(int(self.frame) * 100, 300, 100, 100, self.degree, '', self.x, self.y + 100,
                                          100, 100)
            else:
                self.image.clip_composite_draw(int(self.frame) * 100, 200, 100, 100, self.degree, '', self.x,
                                           self.y +100, 100, 100)
        else:
            pass
            if self.dir == 1:
                self.image.clip_draw(int(self.frame) * 100, 300, 100, 100, self.x, self.y)
            else:
                self.image.clip_draw(int(self.frame) * 100, 200, 100, 100, self.x, self.y)
