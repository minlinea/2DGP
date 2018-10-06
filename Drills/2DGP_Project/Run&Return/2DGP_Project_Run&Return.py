from pico2d import *

open_canvas()

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
tile_size = 40

tile_information_kind = [([(0) for i in range(20)]) for j in range(15)]

tile_kind = load_image('tile_kind.png')
running = True



def load_stage():           # 'save_stage'에 저장되어 있는 타일 파일 로드하여 정보 저장
    global tile_information_kind
    file = open("save_stage.txt",'r')
    for j in range(0, 15, 1):
        line = file.readline()
        for i in range(0, 20, 1):
            tile_information_kind[j][i] = int(line[i:i+1])
    file.close()

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
#------------------------------------------- 마우스 처리----------------------------------------------------#
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_1:      #왼쪽 1번째줄 타일 셋
                load_stage()
# ------------------------------------------- 마우스 처리----------------------------------------------------#

# --------------------------------------- 키보드 입력 처리----------------------------------------------------#

# --------------------------------------- 키보드 입력 처리----------------------------------------------------#

def window_to_pico_coordinate_system(num):      # pico 환경과, 윈도우 환경 마우스 좌표 값 조정 함수
    return WINDOW_HEIGHT - 1 - num

def draw_scene():
    clear_canvas()

    for j in range(0, 15, 1):
        for i in range(0, 20, 1):
            tile_kind.clip_draw(5 + (42 * ((tile_information_kind[j][i]) % 2)),4 + ((42*4)-(42 * ((tile_information_kind[j][i]+2)// 2))),
                                tile_size, tile_size, 20 + i*tile_size, 20 + j * tile_size)

    update_canvas()
    handle_events()



while running:
    draw_scene()

close_canvas()