from pico2d import *

open_canvas()

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600

mouse_xpos, mouse_ypos = 0,0

tile_information_kind = [([(0) for i in range(20)]) for j in range(15)]



running = True
click = False
whiteboard = load_image('whiteboard.png')
imposible_collocate = load_image('imposible_collocate.png')
tile_kind = load_image('tile_kind.png')
tile_choose = load_image('tile_choose.png')
ex_tile_direction = load_image('ex_tile_direction.png')

tile_choose_place = [(33,34),(87,34), (33,95), (87,95), (33,156),(87,156),(33,217),(87,217)]
tile_choose_num = 0

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
    global running, click, mouse_xpos, mouse_ypos, tile_choose_num
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

#------------------------------------------- 마우스 처리----------------------------------------------------#
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
# ------------------------------------------- 마우스 처리----------------------------------------------------#

# --------------------------------------- 키보드 입력 처리----------------------------------------------------#
        elif event.type == SDL_KEYDOWN:         #
            if event.key == SDLK_1:
                tile_choose_num = 0
                set_collocate_tile(0)
                pass
            elif event.key == SDLK_2:
                set_collocate_tile(1)
                tile_choose_num = 1
                pass
            elif event.key == SDLK_3:
                set_collocate_tile(2)
                tile_choose_num = 2
                pass
            elif event.key == SDLK_4:
                set_collocate_tile(3)
                tile_choose_num = 3
                pass
            elif event.key == SDLK_5:
                set_collocate_tile(4)
                tile_choose_num = 4
                pass
            elif event.key == SDLK_6:
                set_collocate_tile(5)
                tile_choose_num = 5
                pass
            elif event.key == SDLK_7:
                set_collocate_tile(6)
                tile_choose_num = 6
                pass
            elif event.key == SDLK_8:
                set_collocate_tile(7)
                tile_choose_num = 7
                pass
            elif event.key == SDLK_9:
                save_stage()
                pass  # 그렸던 것 저장
            elif event.key == SDLK_0:
                load_stage()
                pass  # 그렸던 것 로드
            elif event.key == SDLK_r:
                clear_stage()
                pass  # 맵 초기화
# --------------------------------------- 키보드 입력 처리----------------------------------------------------#

def window_to_pico_coordinate_system(num):
    return WINDOW_HEIGHT - 1 - num


def draw_scene():
    clear_canvas()
    whiteboard.draw((WINDOW_WIDTH)/2, (WINDOW_HEIGHT)/2)

    #for j in (0, 15 + 1, 1):
    #    for i in (0, 20 + 1, 1):
    #        tile_kind.clip_draw(5, 4, 52, 58, tile_information_place[j][i],
    #                      tile_information_place[j][i])
    #타일그리기
    imposible_collocate.clip_draw(0, 0, 120, 400, (120/ 2), (400/2))
    imposible_collocate.clip_draw(0, 0, 120, 400, WINDOW_WIDTH - (120 / 2), (400 / 2))
    tile_kind.draw((120/2), (250/2))
    tile_choose.clip_draw(0,0, 53+1, 61+1, tile_choose_place[tile_choose_num][0], tile_choose_place[tile_choose_num][1])            # 투명화가 필요한데..
    ex_tile_direction.clip_draw(0,0,100,100, WINDOW_WIDTH - (100/2), (400/2))

    update_canvas()
    handle_events()



while running:
    draw_scene()

close_canvas()