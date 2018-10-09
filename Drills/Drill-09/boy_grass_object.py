from pico2d import *

# Game object class here
class Grass:
    def __init__(self):     #생성자 함수 self = this, 속성을 정의해준다.
        self.image = load_image('grass.png')    #속성의 생성과 함께 초기화도 해준다.

    def draw(self):         #행위, 속성을 변화시키는 것
        self.image.draw(400, 30)

class Boy:
    def __init__(self):
        self.x, self.y = 0, 90
        self.frame = 0
        self.image = load_image('run_animation.png')

    def update(self):
        self.frame = (self.frame + 1) % 8
        self.x += 5

    def draw(self):
        self.image.clip_draw(self.frame*100, 0, 100, 100, self.x, self.y)


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

# initialization code
open_canvas()

boy = Boy()
grass = Grass()

running = True

# game main loop code

while running:
    handle_events()     #사용자 입력

    boy.update()        #게임 로직

    clear_canvas()      #렌더링
    grass.draw()
    boy.draw()
    update_canvas()

    delay(0.05)     # --> handle_events(사용자 입력)로 돌아가는 것 = 게임 루프

# finalization code

close_canvas()