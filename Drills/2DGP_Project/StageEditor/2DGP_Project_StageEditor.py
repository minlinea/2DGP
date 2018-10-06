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

def collocate_tile(tile, mouse_x, mouse_y):     # 마우스 값을 입력 받아 해당된 곳에, 현재 설정된 타일 배치
    global tile_information_kind
    i = (mouse_x) // 40
    j = (mouse_y) // 40
    tile_information_kind[j][i] = tile

def clear_stage():          # 타일 초기화, 모든 타일을 빈타일로 만듬
    global tile_information_kind
    set_tile_inforamtion_kind(tile_information_kind, 0)

def set_tile_inforamtion_kind(information, set_tile):   #clear_stage 사용 함수, 모든 타일을 해당 타일로 변환시켜줌
    for j in range(0, 15, 1):
        for i in range(0, 20, 1):
            information[j][i] = set_tile
    return information

def save_stage():           # 현재까지 그린 정보 저장
    global tile_information_kind
    file = open("save_stage.txt",'w')
    for j in range(0, 15, 1):
        for i in range(0, 20, 1):
            if ((j >= 5 and j<=8) and ((i>=0 and i<=2) or (i>=17 and i<=19))):
                data = str(0)
            elif ((j >= 9) and ((i>=0 and i<=2) or (i>=17 and i<=19))):
                data = str(1)
            else:
                data = str(tile_information_kind[j][i])
            file.write(data)
        file.write("\n")
    file.close()

def load_stage():           # 'save_stage'에 저장되어 있는 타일 파일 로드하여 정보 저장
    global tile_information_kind
    file = open("save_stage.txt",'r')
    for j in range(0, 15, 1):
        line = file.readline()
        for i in range(0, 20, 1):
            tile_information_kind[j][i] = int(line[i:i+1])
    file.close()



def handle_events():
    global running, click, mouse_xpos, mouse_ypos, tile_choose_num, tile_information_kind
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

#------------------------------------------- 마우스 처리----------------------------------------------------#
        elif event.type == SDL_MOUSEBUTTONDOWN:         #클릭 시 해당지점 타일 배치
            mouse_xpos, mouse_ypos = event.x, window_to_pico_coordinate_system(event.y)
            click = True
            collocate_tile(tile_choose_num, mouse_xpos, mouse_ypos)
            pass
        elif event.type == SDL_MOUSEMOTION and click == True:      # 누른채로 이동하면 해당 이동 구역 전부 타일 배치
            mouse_xpos, mouse_ypos = event.x, window_to_pico_coordinate_system(event.y)
            collocate_tile(tile_choose_num, mouse_xpos, mouse_ypos)
            pass
        elif event.type == SDL_MOUSEBUTTONUP:         # 마우스 떼면 더이상 안그려지게끔
            click = False # 마우스 버튼 뗀 순간 마우스모션과 연계 안되게끔
            pass
# ------------------------------------------- 마우스 처리----------------------------------------------------#

# --------------------------------------- 키보드 입력 처리----------------------------------------------------#
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_1:      #왼쪽 1번째줄 타일 셋
                tile_choose_num = 0
                pass
            elif event.key == SDLK_2:    #오른쪽 1번째줄 타일 셋
                tile_choose_num = 1
                pass
            elif event.key == SDLK_3:   #왼쪽 2번째줄 타일 셋
                tile_choose_num = 2
                pass
            elif event.key == SDLK_4:   #오른쪽 2번째줄 타일 셋
                tile_choose_num = 3
                pass
            elif event.key == SDLK_5:   #왼쪽 3번째줄 타일 셋
                tile_choose_num = 4
                pass
            elif event.key == SDLK_6:   #오른쪽 3번째줄 타일 셋
                tile_choose_num = 5
                pass
            elif event.key == SDLK_7:   #왼쪽 4번째줄 타일 셋
                tile_choose_num = 6
                pass
            elif event.key == SDLK_8:   #오른쪽 4번째줄 타일 셋
                tile_choose_num = 7
                pass
            elif event.key == SDLK_9:   #현재 그려진 타일 저장
                save_stage()
                pass  # 그렸던 것 저장
            elif event.key == SDLK_0:   #save_stage.txt에 저장된 타일 로드
                load_stage()
                pass  # 그렸던 것 로드
            elif event.key == SDLK_r:   # 모든 타일 빈타일로 초기화
                clear_stage()
                pass  # 맵 초기화
# --------------------------------------- 키보드 입력 처리----------------------------------------------------#

def window_to_pico_coordinate_system(num):      # pico 환경과, 윈도우 환경 마우스 좌표 값 조정 함수
    return WINDOW_HEIGHT - 1 - num

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