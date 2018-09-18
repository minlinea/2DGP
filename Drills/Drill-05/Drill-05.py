from pico2d import *

open_canvas()

grass = load_image('grass.png')
character = load_image('character.png')


def straight_move():
    character_x, character_y = 203, 535
    destination_x, destination_y = 132, 243
    character_x, character_y = movement_calculation(character_x, character_y, destination_x, destination_y)
    pass

def movement_calculation(x1, y1, x2, y2):
    momentum_control = 16
    x1 += (x2-x1) / momentum_control
    y1 += ((y2-y1) / (x2-x1)) * ((x2-x1) / momentum_control)
    return x1, y1

def move_to_point():
    straight_move()
    pass

while True:
    move_to_point()


close_canvas()
