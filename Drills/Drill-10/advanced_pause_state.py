import game_framework
import main_state
from pico2d import *


name = "PauseState"
image = None
delay_time = 0

def enter():
    global image, delay_time
    delay_time = 0
    image = load_image('pause.png')



def exit():
    global image
    del(image)


def update():
    global delay_time
    delay_time = (delay_time + 1) % 250
    pass


def draw():
    global image
    clear_canvas()

    main_state.boy.draw()
    main_state.grass.draw()
    if(delay_time < 150):
        image.draw(400,300, 100, 100)

    update_canvas()




def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            game_framework.pop_state()


def pause(): pass


def resume(): pass




