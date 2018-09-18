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

image_size = 100
image_point = 100

grass_pibotx, grass_piboty = 400, 30

facing_direction = 0
now_index = 0
next_index = now_index+1
frame = 0

def straight_move():
    global frame
    global now_index
    global next_index
    character_x, character_y = point_dictionary[now_index]
    destination_x, destination_y =  point_dictionary[next_index]
    while (moving_direction(character_x, point_dictionary[now_index][0], point_dictionary[next_index][0])):
        clear_canvas()
        character.clip_draw(frame * image_point, facing_direction * image_point, image_size, image_size, character_x, character_y)
        grass.draw(grass_pibotx, grass_piboty)
        update_canvas()
        frame = (frame + 1) % 8
        character_x, character_y = movement_calculation(character_x, character_y, destination_x, destination_y)
        delay(0.05)
        get_events()
    now_index = (now_index + 1) % 10
    next_index = (now_index + 1) % 10
    character_x, character_y = point_dictionary[now_index]

def moving_direction(character_X, now_indexX, next_indexX):
    global facing_direction
    if(next_indexX - now_indexX > 0):
        if  (character_X + 1 < next_indexX):
            facing_direction = 1
            return True
        else:
            return False
    else:
        if  (character_X > next_indexX + 1):
            facing_direction = 0
            return True
        else:
            return False
    pass

def movement_calculation(x1, y1, x2, y2):
    momentum_control = 10
    x1 += (x2-x1) / momentum_control
    y1 += ((y2-y1) / (x2-x1)) * ((x2-x1) / momentum_control)
    return x1, y1

def move_to_point():
    straight_move()
    pass

while True:
    move_to_point()


close_canvas()
