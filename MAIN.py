import random

WIDTH = 800
HEIGHT = 600
TITLE = "TURTLE TURRET"
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

game_over = False
survival_time = 0
# pgzrun MAIN.py

player = PlayerTurtle(CENTER_X, CENTER_Y)

spawn_timer = 0

def draw():
    screen.clear()
    
    screen.fill((20, 40, 85))
    
    if not game_over:
        screen.draw.angle(player.image, (player.x, player.y), player.angle)
    
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

def on_mouse_move(pos):
    if not game_over:
        player.aim_at_mouse(pos)

def on_key_down(key):
    global game_over, survival_time, player
    if key == keys.R and game_over:
        player.hearts = 5
        survival_time = 0
        spawn_timer = 0
        game_over = False

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
        
def check_collisions():
    global game_over
    
    #for lettuce, bubbles and plastic