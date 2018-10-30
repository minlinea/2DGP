import game_framework
from pico2d import *


import game_world

# Boy Run Speed
# fill expressions correctly
PIXEL_PER_METER = (10.0 / 0.3) # 10pixel 30cm
RUN_SPEED_KMPH = 20.0 #km / hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
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
        self.velocity = 0
        self.frame = 0
        self.degree = dir * 3.141592 / 2
        self.opacify = 0.01
        self.wakeup = False


    def update(self):
        if self.wakeup is False :
            self.opacify += self.opacify * game_framework.frame_time
            if self.opacify > 1:
                self.wakeup = True
        else:
            pass

    def draw(self):
        self.image.opacify(self.opacify)
        if self.dir == 1:
            self.image.clip_composite_draw(int(self.frame) * 100, 300, 100, 100, self.degree, '', self.x - 25, self.y - 25 + 100,
                                          100, 100)
        else:
            self.image.clip_composite_draw(int(self.frame) * 100, 200, 100, 100, self.degree, '', self.x + 25,
                                           self.y - 25 + 100, 100, 100)
