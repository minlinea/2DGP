from pico2d import *
import random
# Game object class here
class Grass:
    def __init__(self):     #생성자 함수 self = this, 속성을 정의해준다.
        self.image = load_image('grass.png')    #속성의 생성과 함께 초기화도 해준다.

    def draw(self):         #행위, 속성을 변화시키는 것
        self.image.draw(400, 30)

class Boy:
    def __init__(self):
        self.x, self.y = random.randint(100, 700), 90
        self.frame = random.randint(0,7)
        self.image = load_image('run_animation.png')


    def update(self):
        self.frame = (self.frame + 1) % 8
        self.x += 5

    def draw(self):
        self.image.clip_draw(self.frame*100, 0, 100, 100, self.x, self.y)

class Smallball:
    def __init__(self):
        self.x, self.y = random.randint(0, 800), 599
        self.speed = random.randint(5, 15)
        self.image = load_image('ball21x21.png')

    def update(self):
        if(self.y > 21//2 + 60 - 2):
            self.y -= self.speed
        if (self.y < 21//2 + 60 - 2):
            self.y = 21//2 + 60 - 2

    def draw(self):
        self.image.clip_draw(0, 0, 21, 21, self.x, self.y)


class Bigball:
    def __init__(self):
        self.x, self.y = random.randint(0, 800), 599
        self.speed = random.randint(5, 15)
        self.image = load_image('ball41x41.png')

    def update(self):
        if (self.y > 41 // 2 + 60 - 2):
            self.y -= self.speed
        if (self.y < 41 // 2 + 60 - 2):
            self.y = 41 // 2 + 60 - 2

    def draw(self):
        self.image.clip_draw(0, 0, 41, 41, self.x, self.y)

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

team = [Boy() for i in range(11)]
grass = Grass()

randomnum = random.randint(1,20)
smallballs = [Smallball() for i in range(randomnum) ]
bigballs = [Bigball() for i in range(20-randomnum)]

running = True

# game main loop code

while running:
    handle_events()     #사용자 입력

    for boy in team:
        boy.update()        #게임 로직

    for bigball in bigballs:
        bigball.update()

    for smallball in smallballs:
        smallball.update()
#------------------------------------------렌더링 파트------------------------------------#
    clear_canvas()      #렌더링
    grass.draw()

    for boy in team:
        boy.draw()

    for bigball in bigballs:
        bigball.draw()

    for smallball in smallballs:
        smallball.draw()
    update_canvas()

    delay(0.05)     # --> handle_events(사용자 입력)로 돌아가는 것 = 게임 루프

# ------------------------------------------렌더링 파트------------------------------------#





# finalization code

close_canvas()