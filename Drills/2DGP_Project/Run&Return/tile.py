import game_framework
import threading

from pico2d import *
from enum import Enum

state = Enum('state', 'ground, air, hold, death, waiting')


class Tile:
    image = None
    def __init__(self, vertical, horizon):
        self.y, self.x = vertical, horizon
        self.type = 0
        self.size = 40

        if(self.image == None):
            self.image = load_image('resource\\tile\\tile_kind.png')


    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(5 + (42 * (self.type % 2)), 4 + ((42 * 4) - (42 * ((self.type + 2) // 2))),
                            self.size, self.size, 20 + self.x * self.size, 20 + self.y * self.size)

