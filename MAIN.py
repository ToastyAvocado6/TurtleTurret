import random
import sys
import pgzrun
import pygame
from character import PlayerTurtle
from items import PlasticBottle, Lettuce, Bubble

if "pgzrun" not in sys.modules:
    from pgzero.builtins import Actor, animate, keyboard
    screen = None
    input = None
    sounds = None
    mouse = None


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

bottles = []
lettuces = []
bubbles = []

def draw():
    screen.clear()
    screen.fill((20, 40, 85))

    if not game_over:

        rotated_image = pygame.transform.rotate(images.load(player.image), -player.angle)
        rect = rotated_image.get_rect(center=(player.x, player.y))
        screen.blit(rotated_image, rect)

        for b in bubbles:
            screen.blit(images.load(b.image), (b.x, b.y))

        for bottle in bottles:
            screen.blit(images.load(bottle.image), (bottle.x, bottle.y))

        for lettuce in lettuces:
            screen.blit(images.load(lettuce.image), (lettuce.x, lettuce.y))

        screen.draw.text(f"Survival Time: {int(survival_time)}s", topleft=(30, 30), fontsize=35, color="white")
        screen.draw.text(f"Hearts: {'❤️' * player.hearts}", topright=(WIDTH - 30, 30), fontsize=35)
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
        new_bubble = Bubble(CENTER_X, CENTER_Y, pos[0], pos[1])
        bubbles.append(new_bubble)


def on_key_down(key):
    global game_over, survival_time, spawn_timer, bottles, lettuces, bubbles, player
    if key == keys.R and game_over:
        player.hearts = 5
        survival_time = 0
        spawn_timer = 0
        bottles.clear()
        lettuces.clear()
        bubbles.clear()
        game_over = False


def generate_random_item():
    """Selects a random edge coordinate along the perimeter to spawn an item."""
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
    """Evaluates intersections between projectiles, hazards, and the player entity."""
    global game_over

    for b in bubbles[:]:
        for bottle in bottles[:]:
            distance = ((b.x - bottle.x)**2 + (b.y - bottle.y)**2)**0.5
            if distance < 30:
                bubbles.remove(b)
                bottles.remove(bottle)
                break

    for bottle in bottles[:]:
        dist_to_center = ((bottle.x - CENTER_X)**2 + (bottle.y - CENTER_Y)**2)**0.5
        if dist_to_center < 40:
            player.hearts -= 1
            bottles.remove(bottle)
            if player.hearts <= 0:
                game_over = True

    for lettuce in lettuces[:]:
        dist_to_center = ((lettuce.x - CENTER_X)**2 + (lettuce.y - CENTER_Y)**2)**0.5
        if dist_to_center < 40:
            if player.hearts < 5:
                player.hearts += 1
            lettuces.remove(lettuce)

pgzrun.go()
