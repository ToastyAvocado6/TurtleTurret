import random
import sys
import pgzrun
import pygame
from character import PlayerTurtle
from items import PlasticBottle, Lettuce, Bubble

from pgzero.builtins import Actor, animate, keyboard

WIDTH = 800
HEIGHT = 600
TITLE = "TURTLE TURRET"
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2
# pgzrun MAIN.py

game_over = False
survival_time = 0
spawn_timer = 0

player = PlayerTurtle(CENTER_X, CENTER_Y)
scaled_turtle_base = None
initialized = False

bottles = []
lettuces = []
bubbles = []

#main game
def draw():
    global scaled_turtle_base, initialized
    
    if not initialized:
        pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        base_turtle_img = images.load(player.image)
        scaled_turtle_base = pygame.transform.scale(base_turtle_img, (70, 70))
        pygame.event.pump()
        player.aim_at_mouse(pygame.mouse.get_pos())
        initialized = True

    screen.clear()
    screen.fill((20, 40, 85))
    
    
    if not game_over:
        
        for b in bubbles:
            raw_img = images.load(b.image)
            scaled_img = pygame.transform.scale(raw_img, (30, 30)) 
            screen.blit(scaled_img, (b.x - 15, b.y - 15))
            
        for bottle in bottles:
            raw_img = images.load(bottle.image)
            scaled_img = pygame.transform.scale(raw_img, (45, 65))
            screen.blit(scaled_img, (bottle.x - 22, bottle.y - 32))
            
        for lettuce in lettuces:
            raw_img = images.load(lettuce.image)
            scaled_img = pygame.transform.scale(raw_img, (40, 40))
            screen.blit(scaled_img, (lettuce.x - 20, lettuce.y - 20))
            
        #drawing turtle on top
        rotated_image = pygame.transform.rotate(scaled_turtle_base, -player.angle)
        rect = rotated_image.get_rect(center=(player.x, player.y))
        screen.blit(rotated_image, rect)
            
        # HUD Interface elements
        screen.draw.text(f"Survival Time: {int(survival_time)}s", topleft=(30, 30), fontsize=35, color="white")
        screen.draw.text(f"HP: {player.hearts} / 5", topright=(WIDTH - 30, 30), fontsize=35, color="pink")
    else:
        screen.draw.text("GAME OVER", center=(CENTER_X, CENTER_Y - 50), fontsize=60, color="red")
        screen.draw.text(f"Final Survival Time: {int(survival_time)} Seconds", center=(CENTER_X, CENTER_Y + 10), fontsize=40, color="white")
        screen.draw.text("Press R to Restart", center=(CENTER_X, CENTER_Y + 70), fontsize=30, color="yellow")


def update():
    global game_over, survival_time, spawn_timer
    
    if game_over:
        return
    
    survival_time += 1 / 60
    spawn_timer += 1
    
    if spawn_timer >= 90:
        spawn_timer = 0
        generate_random_item()

    for b in bubbles:
        b.update_position()
    for bottle in bottles:
        bottle.update_position()
    for lettuce in lettuces:
        lettuce.update_position()

    check_collisions()


def on_mouse_move(pos):
    if not game_over:
        player.aim_at_mouse(pos)


def on_mouse_down(pos):
    if not game_over:
        import math
        # Offset by -90 degrees because your turtle art faces UP by default
        rad = math.radians(player.angle - 90)
        
        # Moves the spawn location forward along its line of sight
        spawn_x = player.x + math.cos(rad) * 35
        spawn_y = player.y + math.sin(rad) * 35
        
        new_bubble = Bubble(spawn_x, spawn_y, pos[0], pos[1])
        bubbles.append(new_bubble)


def on_key_down(key):
    global game_over, survival_time, bottles, lettuces, bubbles, player
    if key == keys.R and game_over:
        player.hearts = 5
        survival_time = 0
        spawn_timer = 0
        bottles.clear()
        lettuces.clear()
        bubbles.clear()
        game_over = False
    
    if key == keys.ESCAPE:
        pygame.quit()
        sys.exit()


def generate_random_item():
    edge = random.choice(["top", "bottom", "left", "right"])
    
    if edge == "top":
        sx, sy = random.randint(0, WIDTH), -50
    elif edge == "bottom":
        sx, sy = random.randint(0, WIDTH), HEIGHT + 50
    elif edge == "left":
        sx, sy = -50, random.randint(0, HEIGHT)
    else:
        sx, sy = WIDTH + 50, random.randint(0, HEIGHT)
        
    if random.random() < 0.75:
        bottles.append(PlasticBottle(sx, sy, CENTER_X, CENTER_Y))
    else:
        lettuces.append(Lettuce(sx, sy, CENTER_X, CENTER_Y))


def check_collisions():
    global game_over
    
    bubbles hitting items loop
    for b in bubbles:
        if b.is_popping:
            continue
            
       #check Bottles
        for bottle in bottles[:]:
            distance = ((b.x - bottle.x)**2 + (b.y - bottle.y)**2)**0.5
            if distance < 25:  
                b.pop()
                if bottle.hit(): # runs health drop, removes if returns True
                    bottles.remove(bottle)
                break
                
        if b.is_popping:
            continue
            
        # check Lettuce
        for lettuce in lettuces[:]:
            distance = ((b.x - lettuce.x)**2 + (b.y - lettuce.y)**2)**0.5
            if distance < 25:  
                b.pop()
                if lettuce.hit(): 
                    lettuces.remove(lettuce)
                break

    #plastic bottle movement
    for bottle in bottles[:]:
        dist_to_center = ((bottle.x - CENTER_X)**2 + (bottle.y - CENTER_Y)**2)**0.5
        if dist_to_center < 35:
            player.hearts -= 1
            bottles.remove(bottle)
            if player.hearts <= 0:
                game_over = True

    #defines where and when the lettuce should move
    for lettuce in lettuces[:]:
        dist_to_center = ((lettuce.x - CENTER_X)**2 + (lettuce.y - CENTER_Y)**2)**0.5
        if dist_to_center < 35:
            if player.hearts < 5:
                player.hearts += 1
            lettuces.remove(lettuce)

pgzrun.go()