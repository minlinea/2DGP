from pico2d import *

open_canvas()

grass = load_image('grass.png')
character = load_image('animation_sheet.png')

grass_pibotx, grass_piboty = 400, 30

def straight_move():
    frame = 0
    character_x, character_y = 203, 535
    destination_x, destination_y = 132, 243
    while (character_x > 132 + 1):
        clear_canvas()
        character.clip_draw(frame * 100, 0 * 100, 100, 100, character_x, character_y)
        grass.draw(grass_pibotx, grass_piboty)
        update_canvas()
        frame = (frame + 1) % 8
        character_x, character_y = movement_calculation(character_x, character_y, destination_x, destination_y)
        delay(0.05)
        get_events()


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
