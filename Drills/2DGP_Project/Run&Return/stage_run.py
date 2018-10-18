import game_framework
import title_state
import stage_run

from pico2d import *

from enum import Enum

state = Enum('state', 'ground, air, hold, death, waiting')

character = None
tile = None




class Character:
    def __init__(self):
        self.xpos, self.ypos = 650//2, 270
        self.frame = 0
        self.image = load_image('animation_sheet.png')
        self.direction = 1
        self.xspeed, self.yspeed = 0, 0
        self.state = state.hold
        self.move = False
        self.jumpcount = 0


    def update(self):
        if(self.move == True):
            self.frame = (self.frame + 1) % 8
        self.contact()
        if(self.state == state.air):
            self.move_jump()
        if(self.state != state.death):
            self.xpos += self.xspeed
            self.ypos += self.yspeed


    def draw(self):
        if (self.state != state.death):
            self.image.clip_draw(self.frame * 100, self.direction * 100, 100, 100, self.xpos, self.ypos)

    def move_left(self, movement):
        self.xspeed += movement
        self.direction = 0

    def move_right(self, movement):
        self.xspeed += movement
        self.direction = 1

    def move_jump(self):
        if(self.jumpcount < 3):
            self.yspeed += self.jumpcount + 1
        elif(self.jumpcount < 11):
            self.yspeed += -self.jumpcount + 6
        self.jumpcount = (self.jumpcount + 1) % 11
        if(self.jumpcount ==0):
            self.ypos -= 2
            self.yspeed = 0
            self.state = state.ground
        #if (self.state == state.air):
        #    self.cardinal_spline()
# a*x**2 + b*x + 1 = y
    # 36a + 6b = 9
    # 18a + 6b = 4 18a = -5
# 속도와 누적운동량의 관계를 파악해 보자. c = 1
# 0 1 2 3 4 5 6 7  8   9  10 11
# 1 2 3 3 2 1 0 -1 -2 -3 -4 -3
# 1 3 6 9 11 12 12 11 9 6 2 -1
#실제 좌표 변화 1 4 10 19 20 32 44 55 64 73 79 80

    def move_instant_down(self, movement):
        self.yspeed += movement
        pass

    def move_keyboard(self, type, key):
        if (type == SDL_KEYDOWN):
            if (key == SDLK_LEFT):
                self.move_left(-0.5)
            elif (key == SDLK_RIGHT):
                self.move_right(0.5)
            elif (key == SDLK_UP):
                self.set_state(state.air)
                self.move_jump()
                #self.set_state(state.air)
            elif (key == SDLK_DOWN):
                self. move_instant_down(-0.5)
            self.move = True
        elif (type == SDL_KEYUP):
            if (key == SDLK_LEFT):
                if (self.xspeed != 0):
                    self.move_left(0.5)
            elif (key == SDLK_RIGHT):
                if (self.xspeed != 0):
                    self.move_right(-0.5)
            elif (key == SDLK_UP):
                    pass
            elif (key == SDLK_DOWN):
                if (self.yspeed != 0):
                    self.move_instant_down(0.5)

            self.move = False

        pass



    def contact(self):
        global tile
        character_xbox = int(((20 + self.xpos) // 40))
        character_ybox = int(((20 + self.ypos) // 40) - 1)

        if (self.xspeed > 0):
            predict_character_xbox = int(((40 + self.xpos + self.xspeed) // 40))
        elif (self.xspeed < 0):
            predict_character_xbox = int(((0 + self.xpos + self.xspeed) // 40)-1)
        else:
            predict_character_xbox = int(((20 + self.xpos + self.xspeed) // 40))

        if (self.yspeed > 0):
            predict_charactet_ybox = int(((70 + self.ypos + self.yspeed) // 40) - 1)
        elif (self.yspeed < 0):
            predict_charactet_ybox = int(((0 + self.ypos + self.yspeed) // 40) - 1)
        else:
            predict_charactet_ybox = int(((30 + self.ypos + self.yspeed) // 40) - 1)

        if (abs(character_xbox - predict_character_xbox) != 0):
            if (tile[predict_charactet_ybox][predict_character_xbox].type == 2):
                self.state = state.death
            elif (tile[predict_charactet_ybox][predict_character_xbox].type != 0):
                self.xspeed = 0
            pass
        elif (abs(character_ybox - predict_charactet_ybox) != 0):
            if (tile[predict_charactet_ybox][predict_character_xbox].type == 2):
                self.state = state.death
            elif (tile[predict_charactet_ybox][predict_character_xbox].type != 0):
                self.yspeed = 0
            pass
        elif (abs(character_xbox - predict_character_xbox) + abs(character_ybox - predict_charactet_ybox) ==2):
            if (tile[predict_charactet_ybox][predict_character_xbox].type == 2):
                self.state = state.death
            elif (tile[predict_charactet_ybox][predict_character_xbox].type != 0):
                self.xspeed, self.yspeed = 0,0

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

class Tile:
    def __init__(self, vertical, horizon):
        self.y, self.x = vertical, horizon
        self.type = 0
        self.size = 40
        self.image = load_image('tile_kind.png')
        pass

    def draw(self):
        self.image.clip_draw(5 + (42 * (self.type % 2)), 4 + ((42 * 4) - (42 * ((self.type + 2) // 2))),
                            self.size, self.size, 20 + self.x * self.size, 20 + self.y * self.size)


def load_stage():  # 'save_stage'에 저장되어 있는 타일 파일 로드하여 정보 저장
    global tile
    file = open("save_stage.txt", 'r')
    for j in range(0, 15, 1):
        line = file.readline()
        for i in range(0, 20, 1):
            tile[j][i].type = int(line[i:i + 1])
    file.close()

def enter():
    global character, tile
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
        elif event.type == SDL_KEYUP:
            if (event.key == SDLK_LEFT or event.key == SDLK_RIGHT or event.key == SDLK_UP or event.key == SDLK_DOWN):
                character.move_keyboard(event.type, event.key)
# --------------------------------------- 키보드 입력 처리----------------------------------------------------#



