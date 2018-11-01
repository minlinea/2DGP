import game_framework
import tile

from pico2d import *


# Boy Run Speed
# fill expressions correctly
PIXEL_PER_METER = (10.0 / 0.3) # 10pixel 30cm
RUN_SPEED_KMPH = 20.0 #km / hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
# fill expressions correctly
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8


character = None

# Character Event
RIGHT_DOWN, RIGHT_UP, LEFT_DOWN, LEFT_UP, JUMP, INSTANT_DOWN = range(6)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_UP): JUMP,
    (SDL_KEYDOWN, SDLK_UP): INSTANT_DOWN,
}


#state

class Ground:
    def enter(character, event):
        if event == RIGHT_DOWN:
            character.xspeed += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            character.xspeed -=  RUN_SPEED_PPS
        elif event == RIGHT_UP:
            character.xspeed -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            character.xspeed += RUN_SPEED_PPS

        character.dir = clamp(-1, character.xspeed, 1)
        character.y_axiscount=0
        pass

    @staticmethod
    def exit(character, event):
        pass

    @staticmethod
    def do(character):
        #character.frame = (character.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        character.xpos += character.xspeed * game_framework.frame_time
        character.xpos = clamp(25, character.xpos, 1600 - 25)

    @staticmethod
    def draw(character):
        character.image.clip_draw(int(character.frame * 100), character.direction * 100, 100, 100, character.xpos, character.ypos)
        pass


class Air:
    def enter(character, event):
        pass

    @staticmethod
    def exit(character, event):
        pass

    @staticmethod
    def do(character):
        pass

    @staticmethod
    def draw(character):
        character.image.clip_draw(character.frame * 100, character.direction * 100, 100, 100, character.xpos, character.ypos)
        pass



class Hold:
    def enter(character, event):
        pass

    @staticmethod
    def exit(character, event):
        pass

    @staticmethod
    def do(character):
        pass

    @staticmethod
    def draw(character):
        character.image.clip_draw(character.frame * 100, character.direction * 100, 100, 100, character.xpos, character.ypos)
        pass

class Death:
    def enter(character, event):
        pass

    @staticmethod
    def exit(character, event):
        pass

    @staticmethod
    def do(character):
        pass

    @staticmethod
    def draw(character):
        character.image.clip_draw(character.frame * 100, character.direction * 100, 100, 100, character.xpos, character.ypos)
        pass




next_state_table = {
    Ground: {RIGHT_DOWN: Ground, LEFT_UP: Ground, RIGHT_UP: Ground, LEFT_DOWN: Ground, JUMP: Air, INSTANT_DOWN: Ground},
    Air: {RIGHT_DOWN: Air, RIGHT_UP: Air, LEFT_UP: Air, LEFT_DOWN: Air, JUMP: Air, INSTANT_DOWN: Air},
    Hold: {LEFT_DOWN: Ground, RIGHT_DOWN: Ground, LEFT_UP: Ground, RIGHT_UP: Air, INSTANT_DOWN: Ground}
}




class Character:
    def __init__(self):
        self.xpos, self.ypos = 150, 270
        self.frame = 0
        self.image = load_image('resource\\character\\animation_sheet.png')
        self.direction = 1
        self.xspeed, self.yspeed = 0, 0
        self.y_axiscount = 0
        self.event_que = []
        self.cur_state = Ground
        self.cur_state.enter(self, None)


    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)




    def draw(self):
        self.cur_state.draw(self)


    def move_y_axis(self):
        if(self.y_axiscount % 8 == 1):
            self.yspeed = -((self.y_axiscount)//8) + 15
        else:
            self.yspeed = 0
        self.y_axiscount = (self.y_axiscount + 1) % 243
        if(self.y_axiscount == 0):
            self.y_axiscount = 234

    def move_instant_down(self):
        self.y_axiscount = 234

    def move_keyboard(self, type, key):
        if (type == SDL_KEYDOWN):
            if (key == SDLK_UP):
                self.move_y_axis()
            elif (key == SDLK_DOWN):
                self.move_instant_down()
            self.move = True
        elif (type == SDL_KEYUP):

            self.move = False

        pass



    def contact(self):
        pass
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

        #if (predict_character_xbox >= 20):
            #stage_run.load_stage()
#            self.xpos = 500
#        if(predict_character_ybox >= 15 or predict_character_ybox <= -1 or predict_character_xbox >=20 or predict_character_xbox <= -1):
#            self.change_state(state.death)

#        elif (abs(character_xbox - predict_character_xbox) != 0):
#            if (tile[predict_character_ybox][predict_character_xbox].type == 2):
#                self.change_state(state.death)
#            elif (tile[predict_character_ybox][predict_character_xbox].type != 0
#            or tile[predict_character_ybox+1][predict_character_xbox].type != 0): #진행 방향 박스가 빈 박스가 아닌 경우
#                self.xspeed = 0
#
#            if (tile[character_ybox - 1][character_xbox].type == 0):
#                if (self.state == state.ground):
#                    self.change_state(state.air)
#                    self.y_axiscount = 127
#            pass
#        elif (abs(character_ybox - predict_character_ybox) != 0):
#            if (tile[predict_character_ybox][predict_character_xbox].type == 2):
#                self.change_state(state.death)
#            elif (tile[predict_character_ybox][predict_character_xbox].type != 0):
#                if (self.state == state.air):
#                    if(tile[character_ybox - 1][character_xbox].type == 0):
#                        self.y_axiscount = 243 - self.y_axiscount
#                        self.y_pos = predict_character_ybox * 40 - 30
#                    else:
#                        self.change_state(state.ground)
#            elif (tile[character_ybox - 1][character_xbox].type != 0):
#                if(self.state == state.air and self.y_axiscount > 120):
#                    self.change_state(state.ground)
#            pass
#        elif (abs(character_xbox - predict_character_xbox) + abs(character_ybox - predict_character_ybox) ==2):
#            if (tile[predict_character_ybox][predict_character_xbox].type == 2):
#               self.change_state(state.death)
#           elif (tile[predict_character_ybox][predict_character_xbox].type != 0):
#                if (self.state == state.air):
#                    self.change_state(state.ground)

        pass

    def add_event(self, event):
        self.event_que.insert(0, event)

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)