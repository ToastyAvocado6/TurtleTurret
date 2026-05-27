
# pgzrun MAIN.py
import random
import sys
import pgzrun
import pygame
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'

from character import PlayerTurtle
from items import PlasticBottle, Lettuce, Bubble
from pgzero.builtins import Actor, animate, keyboard

WIDTH = 800
HEIGHT = 600
TITLE = "TURTLE TURRET"
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

game_over = False
game_started = False
survival_time = 0
spawn_timer = 0
spawn_frequency = 90  

player = PlayerTurtle(CENTER_X, CENTER_Y)
initialized = False

bottles = []
lettuces = []
bubbles = []
ripples = []

IMAGE_CACHE = {}

def get_cached_image(image_name, size=None):
    """Loads and smooth-scales images once, keeping them in RAM for speed."""
    cache_key = (image_name, size)
    if cache_key in IMAGE_CACHE:
        return IMAGE_CACHE[cache_key]
    
    raw_surf = images.load(image_name)
    if size:
        processed_surf = pygame.transform.smoothscale(raw_surf, size)
    else:
        processed_surf = raw_surf
        
    IMAGE_CACHE[cache_key] = processed_surf
    return processed_surf

def draw():
    global initialized
    
    if not initialized:
        pygame.display.set_mode((WIDTH, HEIGHT)) 
        pygame.event.pump()
        player.aim_at_mouse(pygame.mouse.get_pos())
        initialized = True

    screen.clear()
    
    bg_scaled = get_cached_image('water', (1000, HEIGHT))
    screen.blit(bg_scaled, (0, 0))
    
    if not game_started:
        screen.draw.text(TITLE, center=(CENTER_X, CENTER_Y - 40), fontsize=65, color="cyan")
        screen.draw.text("PRESS SPACE TO POP UP", center=(CENTER_X, CENTER_Y + 30), fontsize=35, color="white")
        
    elif not game_over:
        for b in bubbles:
            scaled_img = get_cached_image(b.image, (30, 30))
            screen.blit(scaled_img, (b.x - 15, b.y - 15))
            
        for bottle in bottles:
            scaled_img = get_cached_image(bottle.image, (45, 65))
            rotated_bottle = pygame.transform.rotate(scaled_img, bottle.render_angle)
            rect = rotated_bottle.get_rect(center=(bottle.x, bottle.y))
            screen.blit(rotated_bottle, rect)
            
        for lettuce in lettuces:
            scaled_img = get_cached_image(lettuce.image, (40, 40))
            rotated_lettuce = pygame.transform.rotate(scaled_img, lettuce.render_angle)
            rect = rotated_lettuce.get_rect(center=(lettuce.x, lettuce.y))
            screen.blit(rotated_lettuce, rect)
            
        for ripple in ripples:
            surf_size = int(ripple['radius'] * 2) + 4
            ripple_surf = pygame.Surface((surf_size, surf_size), pygame.SRCALPHA)
            color = (135, 235, 255, int(ripple['alpha']))
            pygame.draw.circle(ripple_surf, color, (surf_size // 2, surf_size // 2), int(ripple['radius']), 6)
            
            screen.blit(ripple_surf, (player.x - surf_size // 2, player.y - surf_size // 2))
            
        if not hasattr(player, 'current_size'):
            player.current_size = 0.0
        if player.current_size < 70.0:
            player.current_size += 3.5
            
            
        base_turtle_img = images.load(player.image)
        scaled_turtle = pygame.transform.smoothscale(base_turtle_img, (int(player.current_size), int(player.current_size)))
        
        corrected_angle = -player.angle - 90
        
        rotated_image = pygame.transform.rotate(scaled_turtle, corrected_angle)
        rect = rotated_image.get_rect(center=(player.x, player.y))
        screen.blit(rotated_image, rect)
            
        screen.draw.text(f"Survival Time: {int(survival_time)}s", topleft=(30, 30), fontsize=35, color="white")
        screen.draw.text(f"HP: {player.hearts} / 5", topright=(WIDTH - 30, 30), fontsize=35, color="pink")
    else:
        screen.draw.text("GAME OVER", center=(CENTER_X, CENTER_Y - 50), fontsize=60, color="red")
        screen.draw.text(f"Final Survival Time: {int(survival_time)} Seconds", center=(CENTER_X, CENTER_Y + 10), fontsize=40, color="white")
        screen.draw.text("Press R to Restart", center=(CENTER_X, CENTER_Y + 70), fontsize=30, color="yellow")

def update():
    global game_over, game_started, survival_time, spawn_timer, spawn_frequency
    
    if not game_started or game_over: 
        return
    
    survival_time += 1 / 60
    spawn_timer += 1
    
    spawn_frequency = max(25, 90 - int(survival_time // 10) * 10)
    
    if spawn_timer >= spawn_frequency:
        spawn_timer = 0
        generate_random_item()

    if int(survival_time * 60) % 150 == 0:
        ripples.append({
            'radius': 10.0,   # Starts tight near the turtle core
            'alpha': 80.0,   # Starts quite visible (out of 255 max transparency)
            'speed': 0.5,     # Speed expanding outward
            'fade': 0.3      # Speed fading away
        })

    for ripple in ripples[:]:
        ripple['radius'] += ripple['speed']
        ripple['alpha'] -= ripple['fade']
        
        # If the wave is completely invisible or too large, delete it from memory
        if ripple['alpha'] <= 0:
            ripples.remove(ripple)

    for b in bubbles[:]:
        b.update_position(bubbles)  # Pass array reference directly to fix bubble removal
    for bottle in bottles[:]:
        bottle.update_position()
    for lettuce in lettuces[:]:
        lettuce.update_position()

    check_collisions()

def on_mouse_move(pos):
    if not game_over:
        player.aim_at_mouse(pos)

def on_mouse_down(pos):
    if game_started and not game_over:
        import math

        shooting_angle = player.angle 
        
        rad = math.radians(shooting_angle)
        
        spawn_x = player.x + math.cos(rad) * 35
        spawn_y = player.y + math.sin(rad) * 35
        
        new_bubble = Bubble(spawn_x, spawn_y, pos[0], pos[1])
        bubbles.append(new_bubble)
        
        player.current_size = 56.0

def on_key_down(key):
    global game_over, game_started, survival_time, spawn_timer, spawn_frequency, bottles, lettuces, bubbles, player
    if key == keys.SPACE and not game_started:
        game_started = True
        
    if key == keys.R and game_over:
        player.hearts = 5
        player.current_size = 0.0
        survival_time = 0
        spawn_timer = 0
        spawn_frequency = 90
        bottles.clear()
        lettuces.clear()
        bubbles.clear()
        game_over = False
    
    if key == keys.ESCAPE:
        pygame.quit()
        sys.exit()

def generate_random_item():
    edge = random.choice(["top", "bottom", "left", "right"])
    if edge == "top": sx, sy = random.randint(0, WIDTH), -50
    elif edge == "bottom": sx, sy = random.randint(0, WIDTH), HEIGHT + 50
    elif edge == "left": sx, sy = -50, random.randint(0, HEIGHT)
    else: sx, sy = WIDTH + 50, random.randint(0, HEIGHT)
        
    if random.random() < 0.75:
        bottles.append(PlasticBottle(sx, sy, CENTER_X, CENTER_Y))
    else:
        lettuces.append(Lettuce(sx, sy, CENTER_X, CENTER_Y))

def check_collisions():
    global game_over
    for b in bubbles[:]:
        if b.is_popping:
            continue
        for bottle in bottles[:]:
            distance = ((b.x - bottle.x)**2 + (b.y - bottle.y)**2)**0.5
            if distance < 25:  
                b.pop()
                if bottle.hit(): 
                    bottles.remove(bottle)
                break
        if b.is_popping:
            continue
        for lettuce in lettuces[:]:
            distance = ((b.x - lettuce.x)**2 + (b.y - lettuce.y)**2)**0.5
            if distance < 25:  
                b.pop()
                if lettuce.hit(): 
                    lettuces.remove(lettuce)
                break

    for bottle in bottles[:]:
        dist_to_center = ((bottle.x - CENTER_X)**2 + (bottle.y - CENTER_Y)**2)**0.5
        if dist_to_center < 35:
            player.hearts -= 1
            bottles.remove(bottle)
            if player.hearts <= 0:
                game_over = True

    for lettuce in lettuces[:]:
        dist_to_center = ((lettuce.x - CENTER_X)**2 + (lettuce.y - CENTER_Y)**2)**0.5
        if dist_to_center < 35:
            if player.hearts < 5:
                player.hearts += 1
            lettuces.remove(lettuce)

pgzrun.go()