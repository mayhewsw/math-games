import pygame
import math

from key_accumulator import KeyAccumulator
from math_problems import get_math_problem

WIDTH = 500
HEIGHT = 500
ASTEROID_SPEED = 3

alien = Actor('alien')
alien.pos = WIDTH/2, HEIGHT-50

asteroid = Actor('asteroid')
asteroid.pos = WIDTH/2, 0

key_accumulator = KeyAccumulator()
math_text, solution = get_math_problem()

streak = 0
longest_streak = 0

num_questions = 0
num_correct = 0

# length of game in seconds
game_length = 1 * 60
game_over = False


def end_game():
    global game_over
    # draw success text, maybe some statistics
    game_over = True

ticks_at_start = pygame.time.get_ticks()
clock.schedule(end_game, game_length)

def get_seconds_elapsed():
    return math.floor((pygame.time.get_ticks() - ticks_at_start) / 1000.)

def draw():
    screen.clear()
    alien.draw()
    
    # stats on the side of the screen
    screen.draw.text(f"Num Correct:    {num_correct}", [10,10])
    screen.draw.text(f"Num Questions:  {num_questions}", [10,30])
    screen.draw.text(f"Your answer:    {key_accumulator.answer_string}", [10, 50])

    if not game_over:
        asteroid.draw()
        screen.draw.text(math_text, center=asteroid.pos, owidth=1.5, ocolor=(255,255,0), color=(0,0,0))
        
        seconds_elapsed = get_seconds_elapsed()
        screen.draw.text(f"{game_length - seconds_elapsed}", [10, 70])
        
    else:
        screen.draw.text(f"Game over!", center=(WIDTH/2, HEIGHT/2), fontsize=60)
        screen.draw.text(f"Accuracy: {num_correct / num_questions:.2%}", center=(WIDTH/2, HEIGHT/2 + 40))


def reset_asteroid():
    global solution
    global math_text
    global num_questions
    asteroid.y = 0
    asteroid.x = WIDTH/2
    math_text, solution = get_math_problem()
    num_questions += 1
    
def update():
    if not game_over:
        # TODO: make this increase with time
        asteroid.y += ASTEROID_SPEED
        if asteroid.y > HEIGHT:
            reset_asteroid()
        
        if alien.colliderect(asteroid):
            set_alien_hurt()
            reset_asteroid()

def on_mouse_down(pos):
    if alien.collidepoint(pos):
        set_alien_hurt()
    else:
        pass

def on_key_down(key):
    global key_accumulator
    global streak
    global longest_streak
    global num_correct

    key_accumulator.add_key(key)

    if key == key.RETURN:
        # submit if len > 0
        if len(key_accumulator.answer_string) == 0:
            return
        answer_num = int(key_accumulator.answer_string)
        if answer_num == solution:
            print("Correct answer!")
            num_correct += 1
            reset_asteroid()
            streak += 1
            if streak > longest_streak:
                longest_streak = streak
        else:
            print("WRONG!")
        key_accumulator.answer_string = ""
        
    
def set_alien_hurt():
    global streak
    alien.image = 'alien_hurt'
    sounds.eep.play()
    clock.schedule_unique(set_alien_normal, 1.0)
    streak = 0

def set_alien_normal():
    alien.image = 'alien'
