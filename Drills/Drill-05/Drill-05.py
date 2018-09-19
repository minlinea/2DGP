from pico2d import *

open_canvas()

grass = load_image('grass.png')
character = load_image('animation_sheet.png')

point0 = (203, 535)
point1 = (132, 243)
point2 = (535, 470)
point3 = (477, 203)
point4 = (715, 136)
point5 = (316, 225)
point6 = (510, 92)
point7 = (692, 518)
point8 = (682, 336)
point9 = (712, 349)
point_dictionary = (point0, point1, point2, point3, point4, point5, point6, point7, point8, point9)

run_left = 0
run_right = 1
walk_left = 2
walk_right = 3
facing_direction = (run_left, run_right, walk_left, walk_right)
facing_point = 0

image_size = 100
image_point = 100

grass_pibotx, grass_piboty = 400, 30


now_index = 0
next_index = now_index+1
frame = 0

def straight_move():
    global frame, now_index, next_index
    character_x, character_y = point_dictionary[now_index]
    destination_x, destination_y =  point_dictionary[next_index]
    while (moving_direction(character_x, point_dictionary[now_index][0], point_dictionary[next_index][0])):
        clear_canvas()
        character.clip_draw(frame * image_point, facing_direction[facing_point] * image_point, image_size, image_size, character_x, character_y)
        grass.draw(grass_pibotx, grass_piboty)
        update_canvas()
        frame = (frame+1)% 8
        character_x, character_y = movement_calculation(character_x, character_y, destination_x, destination_y)
        delay(0.05)
        get_events()
    now_index = (now_index + 1) % 10
    next_index = (now_index + 1) % 10
    character_x, character_y = point_dictionary[now_index]

def draw_scene()
    pass


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
    pass

def movement_calculation(x1, y1, x2, y2):
    global facing_direction
    momentum_control = 10
    return x1 + (x2-x1) / momentum_control, y1 + ((y2-y1) / (x2-x1)) * ((x2-x1) / momentum_control)

def move_to_point():
    straight_move()
    pass

while True:
    move_to_point()


close_canvas()
