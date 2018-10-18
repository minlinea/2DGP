import game_framework
import stage_run
from pico2d import *


pause_image = None
choose_menu = None
choose_menu_pivot_num = 0

def enter():
    global pause_image, choose_menu
    pause_image = load_image('pause.png')
    choose_menu = load_image('pause_choose_menu.png')



def exit():
    global pause_image, choose_menu
    del(pause_image)
    del(choose_menu)


def update():
    pass


def draw():
    global pause_image, choose_menu
    clear_canvas()
    #choose_menu.clip_draw(400,300)
    pause_image.draw(400,300)
    update_canvas()




def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.pop_state()
    pass


def pause(): pass


def resume(): pass




