from pygame import *
from random import randint
import sys

init()

window_size = 1200, 800
window = display.set_mode(window_size)
display.set_caption("Flappy-ish")
clock = time.Clock()

player_rect = Rect(150, window_size[1] // 2 - 100, 100, 100)

def generate_pipes(count, pipe_width=140, gap=280, min_height=50, max_height=440, distance=450):
    pipes = []
    start_x = window_size[0] + 50
    for _ in range(count):
        height = randint(min_height, max_height)
        top_pipe = Rect(start_x, 0, pipe_width, height)
        bottom_pipe = Rect(start_x, height + gap, pipe_width, window_size[1] - (height + gap))
        pipes.extend([top_pipe, bottom_pipe])
        start_x += distance
    return pipes

pipes = generate_pipes(6)
main_font = font.Font(None, 100)
score = 0
lose = False
y_vel = 2

while True:
    for e in event.get():
        if e.type == QUIT:
            quit()
            sys.exit()

    window.fill('sky blue')

    keys = key.get_pressed()
    if keys[K_w] and not lose: 
        player_rect.y -= 15
    if keys[K_s] and not lose: 
        player_rect.y += 15

    for pie in pipes[:]: 
        if not lose:
            pie.x -= 10
        draw.rect(window, 'green', pie)

        if pie.x < -200:
            pipes.remove(pie)
            score += 0.5

        if player_rect.colliderect(pie):
            lose = True

    if len(pipes) < 8:
        pipes += generate_pipes(4)

    draw.rect(window, 'red', player_rect)

    if player_rect.y >= window_size[1] - player_rect.h:
        lose = True
    if player_rect.y <= 0:
        lose = True

    if lose:
        player_rect.y += y_vel
        y_vel *= 1.1

    score_surf = main_font.render(str(int(score)), True, 'black')
    score_rect = score_surf.get_rect(center=(window_size[0] // 2, 40))
    window.blit(score_surf, score_rect)

    display.update()
    clock.tick(60)

    if keys[K_r] and lose:
        lose = False
        score = 0
        pipes = generate_pipes(6)
        player_rect.y = window_size[1] // 2 - 100
        y_vel = 2 