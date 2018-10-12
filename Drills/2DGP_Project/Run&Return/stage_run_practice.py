import game_framework
import stage_run_practice
from pico2d import *

from enum import Enum

state = Enum('state', 'ground, air, hold, death, waiting')


WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600

character = None


class Character:
    def __init__(self):
        self.xpos, self.ypos = 650//2, 270
        self.frame = 0
        self.image = load_image('run_animation.png')
        self.dir = 1
        self.xspeed, self.yspeed = 0, 0
        self.state = state.hold
        self.move = False

    def update(self):
        if(self.move == True):
            self.frame = (self.frame + 1) % 8
        self.contact()
        if(self.state != state.death):
            self.xpos += self.xspeed
            self.ypos += self.yspeed

    def draw(self):
        if (self.state != state.death):
            self.clip_draw(self.frame * 100, 0, 100, 100, self.xpos, self.ypos)

    def move_left(self, movement):
        self.xspeed += movement
        # 바라보는 방향 추가
        pass

    def move_move_right(self, movement):
        self.xspeed += movement
        # 바라보는 방향 추가
        pass

    def move_jump(self):
        pass

    def move_instant_down(self):
        pass

    def move(self, type, key):
        if (type == SDL_KEYDOWN):
            if (key == SDLK_LEFT):
                self.move_left(-0.5)
            elif (key == SDLK_RIGHT):
                self.move_right(0.5)
            elif (key == SDLK_UP):
                self.move_jump()
            elif (key == SDLK_DOWN):
                self. move_instant_down()
            self.move = True
        elif (type == SDL_KEYUP):
            if (key == SDLK_LEFT):
                self.move_left(0.5)
            elif (key == SDLK_RIGHT):
                self.move_right(-0.5)
            self.move = False

        pass


    def contact(self):
        global tile_information
        character_xbox = int(((20 + self.xpos) // 40))
        character_ybox = int(((20 + self.ypos) // 40) - 1)

        if (self.xspeed > 0):
            predict_character_xbox = int(((40 + self.xpos + self.xspeed) // 40))
        elif (self.xspeed < 0):
            predict_character_xbox = int(((0 + self.xpos + self.xspeed) // 40))
        else:
            predict_character_xbox = int(((20 + self.xpos + self.xspeed) // 40))

        if (self.yspeed > 0):
            predict_charactet_ybox = int(((40 + self.ypos + self.yspeed) // 40) - 1)
        elif (self.yspeed < 0):
            predict_charactet_ybox = int(((0 + self.ypos + self.yspeed) // 40) - 1)
        else:
            predict_charactet_ybox = int(((20 + self.ypos + self.yspeed) // 40) - 1)

        if (abs(character_xbox - predict_character_xbox) + abs(character_ybox - predict_charactet_ybox) < 1):
            pass
        elif (abs(character_xbox - predict_character_xbox) != 0):
            if (tile_information[predict_charactet_ybox][predict_character_xbox] == 2):
                return state.death
            pass
        elif (abs(character_ybox - predict_charactet_ybox) != 0):
            pass
        pass

    def set_state(self, type):
        if (type == state.ground):
            self.state = state.ground
        elif (type == state.air):
            self.state = state.air
        elif (type == state.hold):
            self.state = state.hold
        elif (type == state.death):
            self.state = state.death
        elif (type == state.waiting):
            self.state = state.waiting



def load_stage():           # 'save_stage'에 저장되어 있는 타일 파일 로드하여 정보 저장
    global tile_information
    file = open("save_stage.txt",'r')
    for j in range(0, 15, 1):
        line = file.readline()
        for i in range(0, 20, 1):
            tile_information[j][i] = int(line[i:i+1])
    file.close()


def draw_scene():


    for j in range(0, 15, 1):
        for i in range(0, 20, 1):
            tile_kind.clip_draw(5 + (42 * ((tile_information[j][i]) % 2)),4 + ((42*4)-(42 * ((tile_information[j][i]+2)// 2))),
                                tile_size, tile_size, 20 + i*tile_size, 20 + j * tile_size)




def enter():
    global character
    character = Character()
    load_stage()
    pass


def exit():
    global character
    del(character)



def pause():
    pass


def resume():
    pass


def update():
    global character
    character.update()
    pass


def draw():
    clear_canvas()

    character.draw()


    update_canvas()

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
        elif event.type == SDL_KEYDOWN or event.type == SDL_KEYUP:
            if (event.key == SDLK_LEFT or event.key == SDLK_RIGHT or event.key == SDLK_UP or event.key == SDLK_DOWN):
                character.move(event.type, event.key)
# --------------------------------------- 키보드 입력 처리----------------------------------------------------#



tile_size = 40
tile_information = [([(0) for i in range(20)]) for j in range(15)]

tile_kind = load_image('tile_kind.png')
