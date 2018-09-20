from pico2d import *

KPU_WIDTH, KPU_HEIGHT = 1280, 1024


def handle_events():
    global running
    global mouse_xpos, mouse_ypos, character_xpos, character_ypos, mouseclick_ypos, mouseclick_xpos
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_MOUSEMOTION:
            mouse_xpos, mouse_ypos = event.x, window_to_pico_coordinate_system(event.y)
        elif event.type == SDL_MOUSEBUTTONDOWN:
            mouseclick_xpos, mouseclick_ypos = event.x,  window_to_pico_coordinate_system(event.y)
            character_xpos, character_ypos = mouseclick_xpos, mouseclick_ypos
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

def straight_move():
    pass

def window_to_pico_coordinate_system(num):
    return KPU_HEIGHT - 1 - num

def moving_direction(character_X, now_indexX, next_indexX):
    pass

def movement_calculation(x1, y1, x2, y2):
    momentum_control = 10
    return x1 + (x2-x1) / momentum_control, y1 + ((y2-y1) / (x2-x1)) * ((x2-x1) / momentum_control)

open_canvas(KPU_WIDTH, KPU_HEIGHT)
kpu_ground = load_image('KPU_GROUND.png')
character = load_image('animation_sheet.png')
hand_arrow = load_image('hand_arrow.png')



running = True
click = True

mouse_xpos, mouse_ypos = KPU_WIDTH // 2, KPU_HEIGHT // 2
character_xpos, character_ypos = KPU_WIDTH // 2, KPU_HEIGHT // 2
mouseclick_xpos, mouseclick_ypos = KPU_WIDTH // 2, KPU_HEIGHT // 2


frame = 0
hide_cursor()

run_left = 0
run_right = 1
walk_left = 2
walk_right = 3
facing_direction = (run_left, run_right, walk_left, walk_right)
facing_point = 0

while running:
    clear_canvas()
    kpu_ground.draw(KPU_WIDTH // 2, KPU_HEIGHT // 2)
    character.clip_draw(frame * 100, 100 * facing_direction[facing_point], 100, 100, character_xpos, character_ypos)
    hand_arrow.draw(mouse_xpos, mouse_ypos)
    straight_move()
    update_canvas()
    frame = (frame + 1) % 8

    delay(0.02)
    handle_events()

close_canvas()




