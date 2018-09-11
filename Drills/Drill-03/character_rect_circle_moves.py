from pico2d import *
import math

open_canvas()

grass = load_image('grass.png')
character = load_image('character.png')

# fill here

right = 0
up = 1
left = 2
down = 3
circle = 4
current_state = [right, up, left, down, circle]
state = 0
x=400
y = 100
rad = -1.5
circle_move = False
while(1):
    clear_canvas_now()
    grass.draw_now(400,30)
    if(state == current_state[0]):
        x = x+2
        delay(0.01)
        character.draw_now(x,y)
        if(x > 400):
           if(circle_move == True):
                state = circle
        if(x > 778):
            state = up
    elif(state == current_state[1]):
        y = y+2
        delay(0.01)
        character.draw_now(x,y)
        if(y > 558):
            state = left
    elif(state == current_state[2]):
        x = x-2
        delay(0.01)
        character.draw_now(x,y)
        if(x < 22):
            state = down
    elif(state == current_state[3]):
        y = y-2
        delay(0.01)
        character.draw_now(x,y)
        if(y < 102):
            state = right
            circle_move = True
    elif(state == current_state[4]):
        x = 400
        y = 300
        character.draw_now(x + 350 * math.cos(rad),y + 200 * math.sin(rad))
        rad = rad + 0.1
        delay(0.1)
        if(rad > 4.7):
            state = right
            rad = -1.5
            y = 100
            circle_move = False
        
    
close_canvas()
