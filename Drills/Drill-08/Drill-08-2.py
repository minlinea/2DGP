import random
from pico2d import *

KPU_WIDTH, KPU_HEIGHT = 1280, 1024

open_canvas()

kpu_ground = load_image('KPU_GROUND.png')
character = load_image('animation_sheet.png')

size = 10
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
t = cycle / momentum_control
delay_time = 2
move_count = 0
pass_point = 0


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
    global point, character_x, character_y, pass_point
    moving_direction(character_x, point_dictionary[point-1][0], point_dictionary[point][0])
    character_x, character_y = movement_calculation(point_dictionary[point - 1][0], point_dictionary[point - 1][1],
                                                        point_dictionary[point][0], point_dictionary[point][1])
    if(cycle == 1 and t == 0):
        character_x, character_y = point_dictionary[point]
        point = (point+1) % size

def curve_move():
    global point, character_x, character_y, delay_time, move_count
    moving_direction(character_x, point_dictionary[(point+move_count) % size][0])
    character_x, character_y = cardinal_spline(point_dictionary[(point - 1) % size], point_dictionary[point % size],
                                                    point_dictionary[(point + 1) % size], point_dictionary[(point + 2) % size])
    delay_time += 2
    if(move_count == 3):
        move_count = 1
        point = (point+2) % size


def cardinal_spline(p1, p2, p3, p4):
    global delay_time, move_count, point, pass_point

    # draw p1-p2
    if(move_count == 0):
        t = ((delay_time + 2) % 100) / 100
        x = (2*t**2-3*t+1)*p1[0]+(-4*t**2+4*t)*p2[0]+(2*t**2-t)*p3[0]
        y = (2*t**2-3*t+1)*p1[1]+(-4*t**2+4*t)*p2[1]+(2*t**2-t)*p3[1]
        if (delay_time == 50):
            delay_time = 0
            move_count = 1
            x = p2[0]
            y = p2[1]
            pass_point = (pass_point + 1) % size
        return x,y

    # draw p2-p3
    if(move_count == 1):
        t = ((delay_time + 2) % 101) / 100
        x = ((-t**3 + 2*t**2 - t)*p1[0] + (3*t**3 - 5*t**2 + 2)*p2[0] + (-3*t**3 + 4*t**2 + t)*p3[0] + (t**3 - t**2)*p4[0])/2
        y = ((-t**3 + 2*t**2 - t)*p1[1] + (3*t**3 - 5*t**2 + 2)*p2[1] + (-3*t**3 + 4*t**2 + t)*p3[1] + (t**3 - t**2)*p4[1])/2
        if (delay_time == 100):
            delay_time = 0
            move_count = 2
            x = p3[0]
            y = p3[1]
            pass_point = (pass_point + 1) % size
        return x,y

    # draw p3-p4

    if (move_count == 2):
        t = ((delay_time + 2) % 101) / 100
        x = ((-t ** 3 + 2 * t ** 2 - t) * p2[0] + (3 * t ** 3 - 5 * t ** 2 + 2) * p3[0] + (
                    -3 * t ** 3 + 4 * t ** 2 + t) * p4[0] + (t ** 3 - t ** 2) * p1[0]) / 2
        y = ((-t ** 3 + 2 * t ** 2 - t) * p2[1] + (3 * t ** 3 - 5 * t ** 2 + 2) * p3[1] + (
                    -3 * t ** 3 + 4 * t ** 2 + t) * p4[1] + (t ** 3 - t ** 2) * p1[1]) / 2
        if (delay_time == 100):
            delay_time = 0
            move_count = 3
            x = p4[0]
            y = p4[1]
            pass_point = (pass_point + 1) % size
        return x,y

def draw_scene():
    global frame
    clear_canvas()
    kpu_ground.draw(KPU_WIDTH // 2, KPU_HEIGHT // 2)
    character.clip_draw(frame * image_point, facing_direction[facing_point] * image_point, image_size, image_size, character_x, character_y)
    character_stamp()
    update_canvas()
    frame = (frame + 1) % 8
    delay(0.05)
    handle_events()

def character_stamp():
    for i in range (0, pass_point+1,1):
        character.clip_draw(0, 0, image_size, image_size, point_dictionary[i][0], point_dictionary[i][1])

def moving_direction(character_X, next_indexX):
    global facing_point
    if(next_indexX - character_X >= 0):
        facing_point = run_right
    else:
        facing_point = run_left


def movement_calculation(x1, y1, x2, y2):
    global momentum_control, cycle, t
    cycle = ((cycle+1) % momentum_control)
    t = cycle / momentum_control
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
    #straight_move()
    curve_move()


while running:
    move_to_point()
    draw_scene()


close_canvas()