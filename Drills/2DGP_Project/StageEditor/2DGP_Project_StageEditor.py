from pico2d import *

open_canvas()

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
    #for event in events:
        #if event.type == SDL_MOUSEBUTTONDOWN:
            # 마우스 위치 값, 현재 선택한 타일 정보 필요

def draw_scene():
    clear_canvas()
    whiteboard.clip_draw(0,0,800-1,600-1,(800-1)/2, (600-1)/2)
    imposible_collocate.clip_draw(0, 0, 150 - 1, 400 - 1, (150 - 1) / 2, (400-1)/2)
    imposible_collocate.clip_draw(0, 0, 150 - 1, 400 - 1, 800 - ((150 - 1) / 2), ((400 - 1) / 2))
    update_canvas()
    handle_events()

running = True
whiteboard = load_image('whiteboard.png')
imposible_collocate = load_image('imposible_collocate.png')


while running:
    draw_scene()

close_canvas()

