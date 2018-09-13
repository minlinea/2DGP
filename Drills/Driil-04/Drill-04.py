from pico2d import *
open_canvas()
grass = load_image('grass.png')
character = load_image('animation_sheet.png')


# 여기를 채우세요.
state = 0
x = 0
frame = 0
while (1):
    clear_canvas()
    grass.draw(400, 30)
    if(state ==1):
        x += 5
        if(x>=805):
            state = 0
            frame = 0
    else:
        x -= 5
        if(x<=-5):
            state = 1
            frame =0
    character.clip_draw(frame * 100, state * 100, 100, 100, x, 90)
    update_canvas()
    frame = (frame + 1) % 8
    delay(0.05)
    get_events()


close_canvas()

