import random
from pico2d import *

KPU_WIDTH, KPU_HEIGHT = 1280, 1024

open_canvas()

kpu_ground = load_image('KPU_GROUND.png')
character = load_image('animation_sheet.png')

size = 20
run_left = 0
run_right = 1
walk_left = 2
walk_right = 3
facing_direction = [run_left, run_right, walk_left, walk_right]
facing_point = 0

image_size = 100
image_point = 100

frame = 0
point = 1
momentum_control = 20
cycle = 1

running = True

point_dictionary = [(random.randint(0 + image_size, 800 - image_size), random.randint(0 + image_size, 600 - image_size)) for i in range(size)]

character_x, character_y = point_dictionary[0]

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

def straight_move():
    global point, character_x, character_y, running
    moving_direction(character_x, point_dictionary[point-1][0], point_dictionary[point][0])
    character_x, character_y = movement_calculation(point_dictionary[point - 1][0], point_dictionary[point - 1][1],
                                                        point_dictionary[point][0], point_dictionary[point][1])
    character_x, character_y = point_dictionary[point]
    point = (point) % momentum_control + 1

def Reach_destination():
    pass

def draw_scene():
    global frame
    handle_events()
    clear_canvas()
    kpu_ground.draw(KPU_WIDTH // 2, KPU_HEIGHT // 2)
    character.clip_draw(frame * image_point, facing_direction[facing_point] * image_point, image_size, image_size, character_x, character_y)
    update_canvas()
    frame = (frame + 1) % 8
    delay(0.05)
    get_events()



def moving_direction(character_X, now_indexX, next_indexX):
    global facing_point
    if(next_indexX - now_indexX > 0):
        facing_point = run_right
    else:
        facing_point = run_left



def movement_calculation(x1, y1, x2, y2):
    global momentum_control, cycle
    cycle = ((cycle+1) % momentum_control)
    t= cycle / momentum_control
    x = (1 - t) * x1 + t * x2
    y = (1 - t) * y1 + t * y2
    if(cycle == momentum_control-1):
        t = 1
        x = (1 - t) * x1 + t * x2
        y = (1 - t) * y1 + t * y2
        cycle = 1
        t = 0
    return (x, y)


def move_to_point():
    straight_move()


while running:
    move_to_point()
    draw_scene()


close_canvas()