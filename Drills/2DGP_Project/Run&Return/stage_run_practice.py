import game_framework
import stage_run_practice
from pico2d import *

from enum import Enum
open_canvas()

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600


class Boy:
    def __init__(self):
        self.x, self.y = 650//2, 270
        self.frame = 0
        self.image = load_image('run_animation.png')
        self.dir = 1
        self.xspeed = 0
        self.yspeed = 0

    def update(self):
        self.frame = (self.frame + 1) % 8
        self.x += self.dir
        if self.x >= 800:
            self.dir = -1
        elif self.x <= 0:
            self.dir = 1

    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)

tile_size = 40
tile_information = [([(0) for i in range(20)]) for j in range(15)]

tile_kind = load_image('tile_kind.png')
character = load_image('run_animation.png')

running = True
move = False

frame = 0

state = Enum('state', 'ground, air, hold, death, waiting')
character_state = state.hold


def character_move(move_type):
    if (move_type == SDLK_LEFT):
        move_left(-0.5)
    elif (move_type == SDLK_RIGHT):
        move_right(0.5)
    elif (move_type == SDLK_UP):
       jump()
    elif (move_type == SDLK_DOWN):
        instant_down()
    pass


def move_left(movement):
    global character_xspeed
    character_xspeed += movement
    set_character_state(state.ground)
    #바라보는 방향 추가
    pass


def move_right(movement):
    global character_xspeed
    character_xspeed += movement
    set_character_state(state.ground)
    # 바라보는 방향 추가
    pass


def character_move_calculation(xpos, ypos, xspeed, yspeed, type):
    xpos += xspeed
    ypos += yspeed
    return xpos, ypos
    pass


def jump():
    pass

def instant_down():
    pass

def contact_character(xpos, ypos, xspeed, yspeed):
    global tile_information
    character_xbox = int (((20 + xpos)//40))
    character_ybox = int (((20 + ypos)//40) - 1)

    if (xspeed>0):
        predict_character_xbox = int(((40 + xpos + xspeed) // 40))
    elif (xspeed<0):
        predict_character_xbox = int(((0 + xpos + xspeed) // 40))
    else :
        predict_character_xbox = int(((20 + xpos + xspeed) // 40))

    if (yspeed>0):
        predict_charactet_ybox = int(((40 + ypos + yspeed) // 40) - 1)
    elif (yspeed<0):
        predict_charactet_ybox = int(((0 + ypos + yspeed) // 40) - 1)
    else :
        predict_charactet_ybox = int(((20 + ypos + yspeed) // 40) - 1)

    if (abs(character_xbox - predict_character_xbox) + abs(character_ybox - predict_charactet_ybox) < 1):
        pass
    elif(abs(character_xbox - predict_character_xbox) != 0):
        if (tile_information[predict_charactet_ybox][predict_character_xbox] == 2):
            return state.death
        pass
    elif (abs(character_ybox - predict_charactet_ybox) != 0):
        pass
    pass



def set_character_state(type):
    global character_state
    if (type == state.ground):
        character_state = state.ground
    elif (type == state.air):
        character_state = state.air
    elif (type == state.hold):
        character_state = state.hold
    elif (type == state.death):
        character_state = state.death
    elif (type == state.waiting):
        character_state = state.waiting


def load_stage():           # 'save_stage'에 저장되어 있는 타일 파일 로드하여 정보 저장
    global tile_information
    file = open("save_stage.txt",'r')
    for j in range(0, 15, 1):
        line = file.readline()
        for i in range(0, 20, 1):
            tile_information[j][i] = int(line[i:i+1])
    file.close()

def handle_events():
    global running, move
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
    global frame, character_xpos, character_ypos, character_state
    clear_canvas()

    for j in range(0, 15, 1):
        for i in range(0, 20, 1):
            tile_kind.clip_draw(5 + (42 * ((tile_information[j][i]) % 2)),4 + ((42*4)-(42 * ((tile_information[j][i]+2)// 2))),
                                tile_size, tile_size, 20 + i*tile_size, 20 + j * tile_size)

    if(character_state != state.death):
        character.clip_draw(frame * 100, 0, 100, 100, character_xpos, character_ypos)
    if move == True:
        frame = (frame + 1) % 8
    else:
        frame = 0

    if (character_state != state.hold):
        character_xpos, character_ypos = character_move_calculation(character_xpos, character_ypos,
                                                                character_xspeed, character_yspeed, character_state)
    character_state = contact_character(character_xpos, character_ypos, character_xspeed, character_yspeed)
    update_canvas()
    handle_events()



while running:
    draw_scene()

close_canvas()