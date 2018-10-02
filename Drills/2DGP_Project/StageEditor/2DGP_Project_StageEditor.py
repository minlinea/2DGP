from pico2d import *

open_canvas()

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600

mouse_xpos, mouse_ypos = 0,0

running = True
click = False
whiteboard = load_image('whiteboard.png')
imposible_collocate = load_image('imposible_collocate.png')
tile_kind = load_image('tile_kind.png')
ex_tile_direction = load_image('ex_tile_direction.png')

def collocate_tile():
    pass

def set_collocate_tile(num):
    pass

def clear_stage():
    pass

def save_stage():
    pass

def load_stage():
    pass

def handle_events():
    global running, click, mouse_xpos, mouse_ypos
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:                  # 마우스쪽
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_MOUSEBUTTONDOWN:
            mouse_xpos, mouse_ypos = event.x, window_to_pico_coordinate_system(event.y)
            click = True # 선택한 상태에서 마우스모션과 연계
            collocate_tile()    #elif 어떤 범위 안이면
            # 마우스 위치 값, 현재 선택한 타일 정보 필요
            pass
        elif event.type == SDL_MOUSEMOTION and click == True:
            mouse_xpos, mouse_ypos = event.x, window_to_pico_coordinate_system(event.y)
            # 마우스를 누른채로 움직이면 한번에 타일이 쫘르륵 그려지게끔 만들자.
            pass
        elif event.type == SDL_MOUSEBUTTONUP:
            click = False # 마우스 버튼 뗀 순간 마우스모션과 연계 안되게끔
            pass
        elif event.type == SDL_KEYDOWN:         #키 입력 부분
            if event.key == SDLK_1:
                set_collocate_tile(1)
                pass        #1번타일 로드
            elif event.key == SDLK_2:
                set_collocate_tile(2)
                pass        #2번타일 로드.. 아마 8번 타일까지 만드려나?
            elif event.key == SDLK_9:
                save_stage()
                pass        # 그렸던 것 저장
            elif event.key == SDLK_0:
                load_stage()
                pass        # 그렸던 것 로드
            elif event.key == SDLK_r:
                clear_stage()
                pass        #맵 초기화

def window_to_pico_coordinate_system(num):
    return WINDOW_HEIGHT - 1 - num


def draw_scene():
    clear_canvas()
    whiteboard.clip_draw(0,0,WINDOW_WIDTH,WINDOW_HEIGHT,(WINDOW_WIDTH)/2, (WINDOW_HEIGHT)/2)
    imposible_collocate.clip_draw(0, 0, 100, 400, (100/ 2), (400/2))
    imposible_collocate.clip_draw(0, 0, 100, 400, WINDOW_WIDTH - (100 / 2), (400 / 2))
    tile_kind.clip_draw(0,0,100,250, (100/2), (250/2))
    ex_tile_direction.clip_draw(0,0,100,100, WINDOW_WIDTH - (100/2), (400/2))
    update_canvas()
    handle_events()




while running:
    draw_scene()

close_canvas()

