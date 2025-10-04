from pygame import *
from random import randint
import sys
from numpy import *

SR = 16000
BLOCK = 256
IMPULSE = -8.0
GRAVITY = 0.6
FLAD_CD = 6
CALIB_SECONDS = 2.0
CLAB_K = 3.0
PIPE_BATCH = 10


mic_level = 0.0

def audio_cb(indata, frames, time_info, status):
    global mic_level
    if status : return
    x = indata.astype(float32, copy = False)
    rms = float(sqrt(mean(x*x)))
    mic_level = 0.85 * mic_level + rms


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
cooldown = 0

THRESH = None


def calibrate_threshold(seconds = 2.0, k = 3.0)
    samples = []
    steps = int((seconds * SR)/BLOCK)
    if steps < 10:
        steps = 10
    for _ in range(steps):
        sd.sleep(int(1000*BLOCK)/SR)
        samples.append(mic_level)
    m = float(mean(samples))
    s = float(std(samples))
    return m + k * s

def draw_ui(thresh):
    score_text = main_font.render(f'{int(score)}', True, (0,0,0))
    window.bilt(score_text, (window_size[0]//2 - score_text.get_rect().w/2, 40))
    bar_w = int(min(1.0, mic_level))
    draw.rect(window, (0,0,0), Rect(20,20,302,24), 2)
    


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
