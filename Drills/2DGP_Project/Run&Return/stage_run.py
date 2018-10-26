import game_framework
import title_state
import stage_run
import pause_state
import threading

from pico2d import *

from enum import Enum

state = Enum('state', 'ground, air, hold, death, waiting')

character = None
tile = None
time = 300
stage_count = 0


class Character:
    def __init__(self):
        self.xpos, self.ypos = 150, 270
        self.frame = 0
        self.image = load_image('resource\\character\\animation_sheet.png')
        self.direction = 1
        self.xspeed, self.yspeed = 0, 0
        self.state = state.ground
        self.y_axiscount = 0


    def update(self):
        if(self.y_axiscount != 0):
            self.move_y_axis()
        self.contact()
        if(self.xspeed != 0 or self.yspeed != 0):
            self.xpos += self.xspeed
            self.ypos += self.yspeed
            self.frame = (self.frame + 1) % 8




    def draw(self):
        if (self.state != state.death):
            self.image.clip_draw(self.frame * 100, self.direction * 100, 100, 100, self.xpos, self.ypos)

    def move_left(self, movement):
        self.xspeed += movement
        self.direction = 0

    def move_right(self, movement):
        self.xspeed += movement
        self.direction = 1

    def move_y_axis(self):
        if(self.y_axiscount % 8 == 1):
            self.yspeed = -((self.y_axiscount)//8) + 15
        else:
            self.yspeed = 0
        self.y_axiscount = (self.y_axiscount + 1) % 243
        if(self.y_axiscount == 0):
            if(self.state != state.ground):
                self.y_axiscount = 234

    def move_instant_down(self):
        self.change_state(state.air)
        self.y_axiscount = 234

    def move_keyboard(self, type, key):
        if (type == SDL_KEYDOWN):
            if (key == SDLK_LEFT):
                self.move_left(-0.5)
            elif (key == SDLK_RIGHT):
                self.move_right(0.5)
            elif (key == SDLK_UP):
                self.change_state(state.air)
                self.move_y_axis()
            elif (key == SDLK_DOWN):
                self.change_state(state.air)
                self.move_instant_down()
            self.move = True
        elif (type == SDL_KEYUP):
            if (key == SDLK_LEFT):
                if (self.xspeed != 0):
                    self.move_left(0.5)
            elif (key == SDLK_RIGHT):
                if (self.xspeed != 0):
                    self.move_right(-0.5)

            self.move = False

        pass



    def contact(self):
        global tile
        character_xbox = int(((20 + self.xpos) // 40))
        character_ybox = int(((20 + self.ypos) // 40) - 1)

        if (self.xspeed > 0):
            predict_character_xbox = int(((30 + self.xpos + self.xspeed) // 40))
        elif (self.xspeed < 0):
            predict_character_xbox = int(((10 + self.xpos + self.xspeed) // 40)-1)
        else:
            predict_character_xbox = int(((20 + self.xpos + self.xspeed) // 40))

        if (self.yspeed > 0):
            predict_character_ybox = int(((60 + self.ypos + self.yspeed) // 40) - 1)
        elif (self.yspeed < 0):
            predict_character_ybox = int(((0 + self.ypos + self.yspeed) // 40) - 1)
        else:
            predict_character_ybox = int(((30 + self.ypos + self.yspeed) // 40) - 1)

        if (predict_character_xbox >= 20):
            load_stage()
            self.xpos = 500
        elif(predict_character_ybox >= 15 or predict_character_ybox <= -1 or predict_character_xbox >=20 or predict_character_xbox <= -1):
            self.change_state(state.death)

        elif (abs(character_xbox - predict_character_xbox) != 0):
            if (tile[predict_character_ybox][predict_character_xbox].type == 2):
                self.change_state(state.death)
            elif (tile[predict_character_ybox][predict_character_xbox].type != 0
            or tile[predict_character_ybox+1][predict_character_xbox].type != 0): #진행 방향 박스가 빈 박스가 아닌 경우
                self.xspeed = 0

            if (tile[character_ybox - 1][character_xbox].type == 0):
                if (self.state == state.ground):
                    self.change_state(state.air)
                    self.y_axiscount = 127
            pass
        elif (abs(character_ybox - predict_character_ybox) != 0):
            if (tile[predict_character_ybox][predict_character_xbox].type == 2):
                self.change_state(state.death)
            elif (tile[predict_character_ybox][predict_character_xbox].type != 0):
                if (self.state == state.air):
                    if(tile[character_ybox - 1][character_xbox].type == 0):
                        self.y_axiscount = 243 - self.y_axiscount
                        self.y_pos = predict_character_ybox * 40 - 30
                    else:
                        self.change_state(state.ground)
            elif (tile[character_ybox - 1][character_xbox].type != 0):
                if(self.state == state.air and self.y_axiscount > 120):
                    self.change_state(state.ground)
            pass
        elif (abs(character_xbox - predict_character_xbox) + abs(character_ybox - predict_character_ybox) ==2):
            if (tile[predict_character_ybox][predict_character_xbox].type == 2):
                self.change_state(state.death)
            elif (tile[predict_character_ybox][predict_character_xbox].type != 0):
                if (self.state == state.air):
                    self.change_state(state.ground)

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


    def change_state(self, type):
        if(type == state.death):
            self.set_state(state.death)

        elif(self.state == state.ground):
            if(type == state.air):
                self.set_state(state.air)
            elif(type == state.hold):
                self.set_state(state.hold)
                pass
            pass

        elif(self.state == state.air):
            if(type == state.ground):
                self.set_state(state.ground)
                self.ypos = int(((20 + self.ypos) // 40) - 1) * 40 + 30
                self.y_axiscount = 0
                self.yspeed = 0
            elif(type == state.hold):
                self.set_state(state.hold)
                pass
            pass

        elif(self.state == state.hold):
            if(type == state.ground):
                self.set_state(state.ground)
                pass
            elif(type == state.air):
                self.set_state(state.air)
                pass
            pass

        pass

class Tile:
    def __init__(self, vertical, horizon):
        self.y, self.x = vertical, horizon
        self.type = 0
        self.size = 40
        self.image = load_image('resource\\tile\\tile_kind.png')
        pass

    def draw(self):
        self.image.clip_draw(5 + (42 * (self.type % 2)), 4 + ((42 * 4) - (42 * ((self.type + 2) // 2))),
                            self.size, self.size, 20 + self.x * self.size, 20 + self.y * self.size)


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

def game_timer():
    global time
    time -= 1
    #if(time == 8):
        #game_framework.change_state(title_state)

    timer = threading.Timer(1, game_timer)
    timer.start()

if __name__ == '__main__':
    game_timer()



def enter():
    global character, tile, time
    time = 10
    character = Character()
    tile = [([(Tile(j,i)) for i in range(20)]) for j in range(15)]
    load_stage()
    game_timer()


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



