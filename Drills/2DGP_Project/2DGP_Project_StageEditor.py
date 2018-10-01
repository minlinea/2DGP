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
    update_canvas()
    handle_events()

running = True

while running:
    draw_scene()

close_canvas()

