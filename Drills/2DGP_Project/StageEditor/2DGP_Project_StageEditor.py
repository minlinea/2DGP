from pico2d import *

open_canvas()

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
tile_size = 40
mouse_xpos, mouse_ypos = 0,0

tile_information_kind = [([(0) for i in range(20)]) for j in range(15)]

running = True
click = False
whiteboard = load_image('whiteboard.png')
imposible_collocate = load_image('imposible_collocate.png')
tile_kind = load_image('tile_kind.png')
tile_choose = load_image('tile_choose.png')
ex_tile_direction = load_image('ex_tile_direction.png')

tile_choose_place = [(33,214),(87,214), (33,155),(87,155) , (33,96),(87,96),(33,35),(87,35)]
tile_choose_num = 0

def collocate_tile(tile, mouse_x, mouse_y):
    global tile_information_kind
    i = (mouse_x) // 40
    j = (mouse_y) // 40
    tile_information_kind[j][i] = tile

def set_collocate_tile(num):
    pass

def clear_stage():
    global tile_information_kind
    set_tile_inforamtion_kind(tile_information_kind, 0)

def save_stage():
    pass

def load_stage():
    pass




def handle_events():
    global running, click, mouse_xpos, mouse_ypos, tile_choose_num, tile_information_kind
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
            collocate_tile(tile_choose_num, mouse_xpos, mouse_ypos)    #elif 어떤 범위 안이면
            # 마우스 위치 값, 현재 선택한 타일 정보 필요
            pass
        elif event.type == SDL_MOUSEMOTION and click == True:
            mouse_xpos, mouse_ypos = event.x, window_to_pico_coordinate_system(event.y)
            #collocate_tile()  # elif 어떤 범위 안이면
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
                pass
            elif event.key == SDLK_2:
                tile_choose_num = 1
                pass
            elif event.key == SDLK_3:
                tile_choose_num = 2
                set_tile_inforamtion_kind(tile_information_kind, tile_choose_num)
                pass
            elif event.key == SDLK_4:
                tile_choose_num = 3
                set_tile_inforamtion_kind(tile_information_kind, tile_choose_num)
                pass
            elif event.key == SDLK_5:
                tile_choose_num = 4
                set_tile_inforamtion_kind(tile_information_kind, tile_choose_num)
                pass
            elif event.key == SDLK_6:
                tile_choose_num = 5
                set_tile_inforamtion_kind(tile_information_kind, tile_choose_num)
                pass
            elif event.key == SDLK_7:
                tile_choose_num = 6
                set_tile_inforamtion_kind(tile_information_kind, tile_choose_num)
                pass
            elif event.key == SDLK_8:
                tile_choose_num = 7
                set_tile_inforamtion_kind(tile_information_kind, tile_choose_num)
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

def set_tile_inforamtion_kind(information, set_tile):
    for j in range(0, 15, 1):
        for i in range(0, 20, 1):
            information[j][i] = set_tile
    return information


def draw_scene():
    clear_canvas()
    whiteboard.draw((WINDOW_WIDTH)/2, (WINDOW_HEIGHT)/2)

    for j in range(0, 15, 1):
        for i in range(0, 20, 1):
            tile_kind.clip_draw(5 + (42 * ((tile_information_kind[j][i]) % 2)),4 + ((42*4)-(42 * ((tile_information_kind[j][i]+2)// 2))),
                                tile_size, tile_size, 20 + i*tile_size, 20 + j * tile_size)
    #타일그리기
    imposible_collocate.clip_draw(0, 0, 120, 400, (120/ 2), (400/2))
    imposible_collocate.clip_draw(0, 0, 120, 400, WINDOW_WIDTH - (120 / 2), (400 / 2))
    tile_kind.clip_draw(0,0, 120, 250, (120/2), (250/2))
    tile_choose.clip_draw(0,0, 53+1, 61+1, tile_choose_place[tile_choose_num][0], tile_choose_place[tile_choose_num][1])            # 투명화가 필요한데..
    ex_tile_direction.clip_draw(0,0,100,100, WINDOW_WIDTH - (100/2), (400/2))

    update_canvas()
    handle_events()



while running:
    draw_scene()

close_canvas()