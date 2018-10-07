from pico2d import *
from enum import Enum
open_canvas()

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600

tile_size = 40
tile_information_kind = [([(0) for i in range(20)]) for j in range(15)]

tile_kind = load_image('tile_kind.png')
character = load_image('run_animation.png')

running = True
move = False

frame = 0
character_xpos = 800//2
character_ypos = 600//2
character_speed = 0
state = Enum('state', 'left, right, up, down, hold, death, waiting')
character_state = state.left

def character_move(move_type):
    if (move_type == SDLK_LEFT):
        move_left(-0.5)
        set_character_state(state.left)
    elif (move_type == SDLK_RIGHT):
        move_right(0.5)
        set_character_state(state.right)
    elif (move_type == SDLK_UP):
       jump()
    elif (move_type == SDLK_DOWN):
        instant_down()
    pass

def move_left(movement):
    global character_speed
    character_speed += movement
    #바라보는 방향 추가
    pass


def move_right(movement):
    global character_speed
    character_speed += movement
    # 바라보는 방향 추가
    pass

def character_move_calculation(xpos, ypos, type):
    global character_speed
    if (type == state.left):
        xpos += character_speed
        ypos += 0
    elif (type == state.right):
        xpos += character_speed
        ypos += 0
    return xpos,ypos
    pass
def jump():
    pass

def instant_down():
    pass


def set_character_state(type):
    global character_state
    if (type == state.left):
        character_state = state.left
    elif (type == state.right):
        character_state = state.right
    elif (type == state.up):
        character_state = state.up
    elif (type == state.down):
        character_state = state.down
    elif (type == state.hold):
        character_state = state.hold
    elif (type == state.death):
        character_state = state.death
    elif (type == state.waiting):
        character_state = state.waiting


def load_stage():           # 'save_stage'에 저장되어 있는 타일 파일 로드하여 정보 저장
    global tile_information_kind
    file = open("save_stage.txt",'r')
    for j in range(0, 15, 1):
        line = file.readline()
        for i in range(0, 20, 1):
            tile_information_kind[j][i] = int(line[i:i+1])
    file.close()

def handle_events():
    global running, move, character_speed
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.key == SDLK_ESCAPE:
            running = False
#------------------------------------------- 마우스 처리----------------------------------------------------#

# ------------------------------------------- 마우스 처리----------------------------------------------------#

# --------------------------------------- 키보드 입력 처리----------------------------------------------------#
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_1:      #왼쪽 1번째줄 타일 셋
                load_stage()
            if (event.key == SDLK_LEFT or event.key == SDLK_RIGHT or event.key == SDLK_UP or event.key == SDLK_DOWN):
                character_move(event.key)
                move = True
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                move_right(-0.5)
                move = False
            elif event.key == SDLK_LEFT:
                move_left(0.5)
                move = False
# --------------------------------------- 키보드 입력 처리----------------------------------------------------#

def window_to_pico_coordinate_system(num):      # pico 환경과, 윈도우 환경 마우스 좌표 값 조정 함수
    return WINDOW_HEIGHT - 1 - num

def draw_scene():
    global frame, character_xpos, character_ypos, character_state, character_speed
    clear_canvas()

    for j in range(0, 15, 1):
        for i in range(0, 20, 1):
            tile_kind.clip_draw(5 + (42 * ((tile_information_kind[j][i]) % 2)),4 + ((42*4)-(42 * ((tile_information_kind[j][i]+2)// 2))),
                                tile_size, tile_size, 20 + i*tile_size, 20 + j * tile_size)

    character.clip_draw(frame * 100, 0, 100, 100, character_xpos, character_ypos)
    if move == True:
        frame = (frame + 1) % 8
    else:
        frame = 0

    character_xpos, character_ypos = character_move_calculation(character_xpos, character_ypos, character_state)
    update_canvas()
    handle_events()



while running:
    draw_scene()

close_canvas()