from pico2d import *

open_canvas()

def collocate_tile():
    pass

def set_collocate_tile():
    pass

def clear_stage():
    pass

def save_stage():
    pass

def load_stage():
    pass

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        #if event.type == SDL_MOUSEBUTTONDOWN:
            # 마우스 위치 값, 현재 선택한 타일 정보 필요

def draw_scene():
    clear_canvas()
    whiteboard.clip_draw(0,0,800-1,600-1,(800-1)/2, (600-1)/2)
    imposible_collocate.clip_draw(0, 0, 150 - 1, 400 - 1, (150 - 1) / 2, (400-1)/2)
    imposible_collocate.clip_draw(0, 0, 150 - 1, 400 - 1, 800 - ((150 - 1) / 2), ((400 - 1) / 2))
    update_canvas()
    handle_events()




#-------------------------------------------------------선언부분-------------------------------------------------------#

running = True
whiteboard = load_image('whiteboard.png')
imposible_collocate = load_image('imposible_collocate.png')

#-------------------------------------------------------선언부분-------------------------------------------------------#


#-------------------------------------------------------메인부분-------------------------------------------------------#

while running:
    draw_scene()

close_canvas()
#-------------------------------------------------------메인부분-------------------------------------------------------#

