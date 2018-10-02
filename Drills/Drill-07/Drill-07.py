import random
from pico2d import *

KPU_WIDTH, KPU_HEIGHT = 1280, 1024

open_canvas()

kpu_ground = load_image('KPU_GROUND.png')
character = load_image('animation_sheet.png')

size = 20

point_dictionary = [(random.randint(0,800), random.randint(0,600)) for i in range(size)]

run_left = 0
run_right = 1
walk_left = 2
walk_right = 3
facing_direction = (run_left, run_right, walk_left, walk_right)
facing_point = 0

image_size = 100
image_point = 100
grass_pibotx, grass_piboty = 400, 30

now_index = 1
frame = 0
point = 1
momentum_control = 10

def straight_move():
    global point
    character_x, character_y = point_dictionary[point-1]
    destination_x, destination_y =  point_dictionary[point]
    while (moving_direction(character_x, point_dictionary[point-1][0], point_dictionary[point][0])):
        point = (point + 1) % momentum_control
        draw_scene(character_x,character_y)
        character_x, character_y = movement_calculation(character_x, character_y, destination_x, destination_y)
    point = (point + 1) % momentum_control
    character_x, character_y = point_dictionary[now_index]


def draw_scene(character_X, character_Y):
    global frame
    clear_canvas()
    character.clip_draw(frame * image_point, facing_direction[facing_point] * image_point, image_size, image_size, character_X, character_Y)
    kpu_ground.draw(KPU_WIDTH // 2, KPU_HEIGHT // 2)
    update_canvas()
    frame = (frame + 1) % 8
    delay(0.05)
    get_events()


def moving_direction(character_X, now_indexX, next_indexX):
    global facing_point
    if(next_indexX - now_indexX > 0):
        if (character_X + 1 < next_indexX):
            if(next_indexX - character_X > 6):
                facing_point  = run_right
            else :
                facing_point = walk_right
            return True
        else:
            return False
    else:
        if (character_X > next_indexX + 1):
            if(character_X - next_indexX > 4):
                facing_point  = run_left
            else :
                facing_point = walk_left
            return True
        else:
            return False


def movement_calculation(x1, y1, x2, y2):
    global momentum_control
    for i in range(0, 100 + 1, 10):
        t = i / 100
        x = (1 - t) * x1 + t * x2
        y = (1 - t) * y1 + t * y2
    return (x, y)


def move_to_point():
    straight_move()


while True:
    move_to_point()


close_canvas()