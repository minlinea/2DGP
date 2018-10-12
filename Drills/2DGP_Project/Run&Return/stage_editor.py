import game_framework
import title_state
from pico2d import *


#----------------------------------------게임 오브젝트 클래스--------------------------------------#
class Image:
    def __init__(self, x, y, left, bottom, width, height, title):
        self.x, self.y = x,y
        self.left, self.bottom = left, bottom
        self.width, self.height =  width, height
        self.image = load_image(title)

    def draw(self, x, y):
        self.image.draw(x, y)

    def clip_draw(self, x, y, left, bottom, width, height):
        self.image.clip_draw(left,bottom,width, height,x,y)

class Tile:
    def __init__(self, vertical, horizon):
        self.y, self.x = vertical, horizon
        self.type = 0
        self.size = 40
        self.image = load_image('tile_kind.png')
        tile_information = [([(0) for i in range(20)]) for j in range(15)]
        pass

    def draw(self):
        self.image.clip_draw(5 + (42 * (self.type % 2)), 4 + ((42 * 4) - (42 * ((self.type + 2) // 2))),
                            self.size, self.size, 20 + self.x * self.size, 20 + self.y * self.size)

#----------------------------------------게임 오브젝트 클래스--------------------------------------#



#------------------------------------------함수 선언 부분----------------------------------------#

def collocate_tile(tile, mouse_x, mouse_y):     # 마우스 값을 입력 받아 해당된 곳에, 현재 설정된 타일 배치
    global tile_information_kind
    i = (mouse_x) // 40
    j = (mouse_y) // 40
    tile_information_kind[j][i] = tile

def clear_stage(information, set_tile):          # 타일 초기화, 모든 타일을 빈타일로 만듬
    for j in range(0, 15, 1):
        for i in range(0, 20, 1):
            information[j][i] = set_tile
    return information

def save_stage():           # 현재까지 그린 정보 저장
    global tile_information_kind
    file = open("save_stage.txt",'w')
    for j in range(0, 15, 1):
        for i in range(0, 20, 1):
            if ((j >= 5 and j<=8) and ((i>=0 and i<=2) or (i>=17 and i<=19))):  # 생성 불가능 지역 빈 공간
                data = str(0)
            elif ((j >= 9) and ((i>=0 and i<=2) or (i>=17 and i<=19))):     # 생성 불가능 지역 일반 블록 부분
                data = str(1)
            else:
                data = str(tile_information_kind[j][i])     # 생성 불가능 지역이 아니면 저장된 정보 저장
            file.write(data)
        file.write("\n")
    file.close()

def load_stage():           # 'save_stage'에 저장되어 있는 타일 파일 로드하여 정보 저장
    global tile_information_kind
    file = open("save_stage.txt",'r')
    for j in range(0, 15, 1):           #한 줄씩 읽는다.
        line = file.readline()
        for i in range(0, 20, 1):
            tile_information_kind[j][i] = int(line[i:i+1])      # 한글자씩 슬라이스 해서 읽는다.
    file.close()

def handle_events():
    global running, click, tile_information_kind
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT or (event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE):
            running = False



def event_MOUSE(type, x, y, click, tile):      # 마우스 처리
    if type == SDL_MOUSEBUTTONDOWN:  # 클릭 시 해당지점 타일 배치
        click = True
        collocate_tile(tile, x, y)
    elif type == SDL_MOUSEMOTION and click == True:  # 누른채로 이동하면 해당 이동 구역 전부 타일 배치
        collocate_tile(tile, x, y)

    elif type == SDL_MOUSEBUTTONUP:
        click = False  # 마우스 버튼 뗀 순간 마우스모션과 연계 안되게끔
    return click

def event_KEYDOWN(key):         # 키보드 처리
    global tile_information_kind, tile_choose_num
    if key == SDLK_1:  # 왼쪽 1번째줄 타일 셋
        tile_choose_num = 0
    elif key == SDLK_2:  # 오른쪽 1번째줄 타일 셋
        tile_choose_num = 1
    elif key == SDLK_3:  # 왼쪽 2번째줄 타일 셋
        tile_choose_num = 2
    elif key == SDLK_4:  # 오른쪽 2번째줄 타일 셋
        tile_choose_num = 3
    elif key == SDLK_5:  # 왼쪽 3번째줄 타일 셋
        tile_choose_num = 4
    elif key == SDLK_6:  # 오른쪽 3번째줄 타일 셋
        tile_choose_num = 5
    elif key == SDLK_7:  # 왼쪽 4번째줄 타일 셋
        tile_choose_num = 6
    elif key == SDLK_8:  # 오른쪽 4번째줄 타일 셋
        tile_choose_num = 7
    elif key == SDLK_9:  # 현재 그려진 타일 저장
        save_stage()
    elif key == SDLK_0:  # save_stage.txt에 저장된 타일 로드
        load_stage()
    elif key == SDLK_r:  # 모든 타일 빈타일로 초기화
        clear_stage(tile_information_kind, 0)


def window_to_pico_coordinate_system(num):      # pico 환경과, 윈도우 환경 마우스 좌표 값 조정 함수
    return WINDOW_HEIGHT - 1 - num

def draw_scene():
    clear_canvas()

    whiteboard.draw(whiteboard.x , whiteboard.y)

    for j in range(0, 15, 1):
        for i in range(0, 20, 1):
            tile_kind.clip_draw(20 + i*tile_size, 20 + j * tile_size,
                                5 + (42 * ((tile_information_kind[j][i]) % 2)),4 + ((42*4)-(42 * ((tile_information_kind[j][i]+2)// 2))),
                                tile_size, tile_size)


    imposible_collocate.clip_draw((120/2), imposible_collocate.y, imposible_collocate.left,
                                  imposible_collocate.bottom, imposible_collocate.width, imposible_collocate.height)

    imposible_collocate.clip_draw(WINDOW_WIDTH - (120 / 2), imposible_collocate.y, imposible_collocate.left,
                                  imposible_collocate.bottom, imposible_collocate.width, imposible_collocate.height)

    tile_kind.clip_draw(tile_kind.x, tile_kind.y, tile_kind.left,tile_kind.bottom, tile_kind.width, tile_kind.height)

    tile_choose.clip_draw(tile_choose_place[tile_choose_num][0], tile_choose_place[tile_choose_num][1],
                          tile_choose.left, tile_choose.bottom, tile_choose.width, tile_choose.height)

    # 이미지를 회전 시켜봅시다. 윽 안된다.

    update_canvas()

#------------------------------------------함수 선언 부분----------------------------------------#


#--------------------- initialization code ---------------------#

open_canvas()

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
tile_size = 40

tile_choose_place = [(33,214),(87,214), (33,155),(87,155) , (33,96),(87,96),(33,35),(87,35)]
tile_choose_num = 0

tile_information_kind = [([(0) for i in range(20)]) for j in range(15)]

running = True
click = False


tile_kind = Image((120/2), (250/2), 0,0, 120, 250, 'tile_kind.png')
whiteboard = Image(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 , 0,0,0,0, 'whiteboard.png')
imposible_collocate = Image((120/2), (400/2), 0, 0, 120, 400, 'imposible_collocate.png')
tile_choose = Image(tile_choose_place[tile_choose_num][0], tile_choose_place[tile_choose_num][1],
                    0,0, 53+1, 61+1, 'tile_choose.png')


#--------------------- initialization code ---------------------#






#--------------------- game main loop code ---------------------#
while running:
    # -----------------------------------사용자 입력----------------------------------#

    handle_events()

    # ------------------------------------사용자 입력----------------------------------#

    # ------------------------------------게임 로직-------------------------------------#

    # 스테이지 에디터에서는 존재하지 않음

    # ------------------------------------게임 로직-------------------------------------#

    # -------------------------------------렌더링--------------------------------------#
    draw_scene()
    # -------------------------------------렌더링--------------------------------------#
#--------------------- game main loop code ---------------------#


class Tile:
    def __init__(self, vertical, horizon):
        self.y, self.x = vertical, horizon
        self.type = 0
        self.size = 40
        self.image = load_image('tile_kind.png')
        tile_information = [([(0) for i in range(20)]) for j in range(15)]
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
    global tile
    tile = [([(Tile(j,i)) for i in range(20)]) for j in range(15)]
    load_stage()
    pass


def exit():
    global tile
    del(tile)


def pause():
    pass


def resume():
    pass


def update():
    pass


def draw():
    clear_canvas()

    for j in range(0, 15, 1):
        for i in range(0, 20, 1):
            tile[j][i].draw()
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_stage(title_state)
        elif event.type == SDL_MOUSEBUTTONDOWN or (
                event.type == SDL_MOUSEMOTION and click == True) or event.type == SDL_MOUSEBUTTONUP:
            mouse_xpos, mouse_ypos = event.x, window_to_pico_coordinate_system(event.y)
            click = event_MOUSE(event.type, mouse_xpos, mouse_ypos, click, tile_choose_num)

        elif event.type == SDL_KEYDOWN:
            event_KEYDOWN(event.key)