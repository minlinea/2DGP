from pico2d import *

open_canvas()

grass = load_image('grass.png')
character = load_image('character.png')

def straight_move():
    x, y = 203, 535
    x, y = movement_calculation(x,y)
    pass

def movement_calculation(x,y):
    return x, y
    pass

def move_to_point():
    straight_move()
    pass

while True:
    move_to_point()


close_canvas()
