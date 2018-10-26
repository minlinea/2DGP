from pico2d import *
from ball import Ball

import game_world

# Boy Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SLEEP_TIMER, SPACE, DASH_DOWN, DASH_UP, DASH_TIMER= range(9)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE,
    (SDL_KEYDOWN, SDLK_LSHIFT): DASH_DOWN,
    (SDL_KEYDOWN, SDLK_RSHIFT): DASH_DOWN,
    (SDL_KEYUP, SDLK_LSHIFT): DASH_UP,
    (SDL_KEYUP, SDLK_RSHIFT): DASH_UP
}


# Boy States

class DashState:
    @staticmethod
    def enter(boy, event):
        if event == DASH_DOWN:
            if(boy.velocity > 0):
                boy.velocity += 3
                boy.dir = 1
            else:
                boy.velocity -= 3
                boy.dir = -1


        boy.timer = 200



    @staticmethod
    def exit(boy, event):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.timer -= 1
        boy.x += boy.velocity
        boy.x = clamp(25, boy.x, 1600 - 25)
        if boy.timer ==0:
            boy.add_event(DASH_TIMER)

    @staticmethod
    def draw(boy):
        if boy.dir > 0:
            boy.image.clip_draw(boy.frame * 100, 100, 100, 100, boy.x, boy.y)
        else:
            boy.image.clip_draw(boy.frame * 100, 0, 100, 100, boy.x, boy.y)

class SleepState:
    @staticmethod
    def enter(boy, event):
        boy.frame = 0

    @staticmethod
    def exit(boy, event):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame+1) % 8

    def draw(boy):
        if boy.dir > 0:
            boy.image.clip_composite_draw(boy.frame * 100, 300, 100, 100, 3.141592 / 2, '', boy.x - 25,
                                                boy.y - 25, 100, 100)
        else: boy.image.clip_composite_draw(
            boy.frame * 100, 200, 100, 100, -3.141592 / 2, '', boy.x + 25, boy.y - 25, 100, 100)




class IdleState:

    @staticmethod
    def enter(boy, event):
        if event == RIGHT_DOWN:
            boy.velocity = 0
            boy.dir = 1
        elif event == LEFT_DOWN:
            boy.velocity = 0
            boy.dir = -1
        elif event == RIGHT_UP:
            boy.velocity = 0
            boy.dir = 1
        elif event == LEFT_UP:
            boy.velocity = 0
            boy.dir = -1
        boy.timer = 1000

    @staticmethod
    def exit(boy, event):
        if event == SPACE:
            boy.fire_ball()
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        # fill here
        boy.timer -= 1
        if boy.timer ==0:
            boy.add_event(SLEEP_TIMER)

    @staticmethod
    def draw(boy):
        if boy.dir > 0:
            boy.image.clip_draw(boy.frame * 100, 300, 100, 100, boy.x, boy.y)
        else:
            boy.image.clip_draw(boy.frame * 100, 200, 100, 100, boy.x, boy.y)


class RunState:

    @staticmethod
    def enter(boy, event):
        if event == RIGHT_DOWN:
            boy.velocity += 1
        elif event == LEFT_DOWN:
            boy.velocity -= 1
        elif event == RIGHT_UP:
            boy.velocity -= 1
        elif event == LEFT_UP:
            boy.velocity += 1
        elif event == DASH_UP:
            if(boy.velocity > 0):
                boy.velocity = 1
            else :
                boy.velocity = -1
        elif event == DASH_TIMER:
            if(boy.velocity > 0):
                boy.velocity = 1
            else :
                boy.velocity = -1
        boy.dir = boy.velocity

    @staticmethod
    def exit(boy, event):
        if event == SPACE:
            boy.fire_ball()
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.timer -= 1
        boy.x += boy.velocity
        boy.x = clamp(25, boy.x, 1600 - 25)

    @staticmethod
    def draw(boy):
        if boy.dir > 0:
            boy.image.clip_draw(boy.frame * 100, 100, 100, 100, boy.x, boy.y)
        else:
            boy.image.clip_draw(boy.frame * 100, 0, 100, 100, boy.x, boy.y)



next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
                SLEEP_TIMER: SleepState, SPACE: IdleState, DASH_DOWN:IdleState, DASH_UP:IdleState, DASH_TIMER:IdleState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
               SPACE: RunState, DASH_UP:RunState,  DASH_DOWN:DashState},
    SleepState: {LEFT_DOWN: RunState, RIGHT_DOWN: RunState, LEFT_UP: RunState, RIGHT_UP: RunState, SPACE: IdleState,
                 DASH_DOWN: SleepState, DASH_UP: SleepState, DASH_TIMER: SleepState},
    DashState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
               SPACE: RunState, DASH_DOWN:DashState, DASH_UP:RunState, DASH_TIMER:RunState}
}

class Boy:

    def __init__(self):
        self.x, self.y = 1600 // 2, 90
        self.image = load_image('animation_sheet.png')
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)


    def fire_ball(self):
        ball = Ball(self.x ,self.y, self.dir*3)
        game_world.add_object(ball, 1)
        pass



    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)


    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def fire_ball(self):
        ball = Ball(self.x, self.y, self.dir*3)
        game_world.add_object(ball, 1)