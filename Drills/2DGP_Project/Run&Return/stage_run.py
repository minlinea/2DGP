import game_framework
import title_state
import pause_state

from character import Character
from tile import Tile
from pico2d import *


stage_count = 0




def load_stage():  # 'save_stage'에 저장되어 있는 타일 파일 로드하여 정보 저장
    global tile, stage_count
    file = open("save_stage.txt", 'r')
    for load_temp in range(0, 15 * stage_count, 1):
        line = file.readline()
    for j in range(0, 15, 1):
        line = file.readline()
        for i in range(0, 20, 1):
            tile[j][i].type = int(line[i:i + 1])

    line = file.readline()
    if line:
        stage_count += 1
    file.close()



def enter():
    global character, tile, time
    time = 10
    character = Character()
    tile = [([(Tile(j,i)) for i in range(20)]) for j in range(15)]
    load_stage()


def exit():
    global character, tile
    del(character)
    del(tile)



def pause():
    pass


def resume():
    pass


def update():
    global character
    character.update()


def draw():
    clear_canvas()

    for j in range(0, 15, 1):
        for i in range(0, 20, 1):
            tile[j][i].draw()
    character.draw()

    update_canvas()


def handle_events():
    global character
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)
#------------------------------------------- 마우스 처리----------------------------------------------------#

# ------------------------------------------- 마우스 처리----------------------------------------------------#

# --------------------------------------- 키보드 입력 처리----------------------------------------------------#
        elif event.type == SDL_KEYDOWN:
            if (event.key == SDLK_LEFT or event.key == SDLK_RIGHT or event.key == SDLK_UP or event.key == SDLK_DOWN):
                character.move_keyboard(event.type, event.key)
            if(event.key == SDLK_p):
                game_framework.push_state(pause_state)
        elif event.type == SDL_KEYUP:
            if (event.key == SDLK_LEFT or event.key == SDLK_RIGHT or event.key == SDLK_UP or event.key == SDLK_DOWN):
                character.move_keyboard(event.type, event.key)
# --------------------------------------- 키보드 입력 처리----------------------------------------------------#



