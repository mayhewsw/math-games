import random
import math
from key_accumulator import KeyAccumulator
from math_problems import get_math_problem

WIDTH = 1200
HEIGHT = 800
NUM_ASTEROIDS = 5

key_accumulator = KeyAccumulator()

def generate_asteroid():
    asteroid = Actor('asteroid')
    asteroid.pos = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    # this is in radians
    asteroid.direction = random.random() * math.pi * 2
    asteroid.is_large = True
    asteroid.math_text, asteroid.math_solution = get_math_problem()
    return asteroid

def reset_game():
    global game_over
    global asteroids
    asteroids = [generate_asteroid() for _ in range(NUM_ASTEROIDS)]
    game_over = False
    
alien = Actor('alien')
alien.pos = WIDTH/2, HEIGHT/2
asteroids = None
game_over = None

reset_game()

def draw():

    if len(asteroids) > 0 and not game_over:
        screen.clear()


        for asteroid in asteroids:
            asteroid.draw()
            screen.draw.text(asteroid.math_text, center=asteroid.pos, owidth=1.5, ocolor=(255,255,0), color=(0,0,0))

        alien.draw()
    else:
        screen.draw.text(f"Game over!", center=(WIDTH/2, HEIGHT/2), fontsize=60)

    
def update():
    global game_over 
    for asteroid in asteroids:
        
        speed = 0.5 if asteroid.is_large else 1
        asteroid.y += speed * math.sin(asteroid.direction)
        asteroid.x += speed * math.cos(asteroid.direction)

        if asteroid.x > WIDTH:
            asteroid.x = 0
        if asteroid.x < 0:
            asteroid.x = WIDTH
        if asteroid.y > HEIGHT:
            asteroid.y = 0
        if asteroid.y < 0:
            asteroid.y = HEIGHT

        if asteroid.collidepoint(alien.pos):
            game_over = True

def on_key_down(key):
    global key_accumulator
    global asteroids
    key_accumulator.add_key(key)

    if game_over:
        reset_game()
        return

    if key == key.RETURN:

        # submit if len > 0
        if len(key_accumulator.answer_string) == 0:
            return
        answer_num = int(key_accumulator.answer_string)

        new_asteroids = []
        for asteroid in asteroids:
            if asteroid.math_solution == answer_num:
                if asteroid.is_large:
                    for _ in range(2):
                        a = generate_asteroid()
                        a.pos = asteroid.pos
                        a.is_large = False
                        a.image = "asteroid_small"
                        new_asteroids.append(a)
            else:
                # keep it around, it hasn't been solved
                new_asteroids.append(asteroid)
        asteroids = new_asteroids
        key_accumulator.answer_string = ""