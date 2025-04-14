import pygame
import sys
import random

pygame.init()
WIDTH, HEIGHT = 1490, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blob Shooter")

clock = pygame.time.Clock()

# Load images
try:
    player_right = pygame.image.load("player_right.png").convert_alpha()
    player_left = pygame.image.load("player_left.png").convert_alpha()
    player_down = pygame.image.load("player_down.png").convert_alpha()
    player_up = pygame.image.load("player_up.png").convert_alpha()  # Add this image if missing
    floor_tile = pygame.image.load("floor_tile.png").convert()
    enemy_img = pygame.image.load("enemy_blob2.png").convert_alpha()
except:
    print("Make sure all image files are in the same folder")
    pygame.quit()
    sys.exit()

# Resize player images
player_right = pygame.transform.scale(player_right, (50, 50))
player_left = pygame.transform.scale(player_left, (50, 50))
player_down = pygame.transform.scale(player_down, (50, 50))
player_up = pygame.transform.scale(player_up, (50, 50))
enemy_img = pygame.transform.scale(enemy_img, (40, 40))

# Default player image
player_img = player_right
player_rect = player_img.get_rect(center=(400, 300))
player_speed = 5
player_hp = 100
last_move_direction = "right"

font = pygame.font.SysFont(None, 30)

# Enemy data
enemies = []
enemy_speed = 1
kills = 0
level = 1

def spawn_enemy():
    x = random.choice([0, WIDTH])
    y = random.randint(0, HEIGHT)
    rect = enemy_img.get_rect(center=(x, y))
    return rect

# Load and play background music
pygame.mixer.music.load("background_ost.wav")
pygame.mixer.music.play(-1, 0.0)  # Loop indefinitely

# Bullets
bullets = []
bullet_speed = 10

# Touch controls
button_size = 60
buttons = {
    "left": pygame.Rect(50, HEIGHT - 110, button_size, button_size),
    "right": pygame.Rect(170, HEIGHT - 110, button_size, button_size),
    "up": pygame.Rect(110, HEIGHT - 170, button_size, button_size),
    "down": pygame.Rect(110, HEIGHT - 50, button_size, button_size),
    "fire": pygame.Rect(WIDTH - 120, HEIGHT - 100, button_size, button_size)
}

def draw_buttons():
    for name, rect in buttons.items():
        pygame.draw.rect(screen, (100, 100, 100), rect)
        label = font.render(name[0].upper(), True, (255, 255, 255))
        screen.blit(label, (rect.x + 20, rect.y + 15))

def draw_floor():
    tile_size = 10
    for x in range(0, WIDTH, tile_size):
        for y in range(0, HEIGHT, tile_size):
            screen.blit(floor_tile, (x, y))

def draw_status():
    hp_text = font.render(f"HP: {player_hp}", True, (255, 0, 0))
    level_text = font.render(f"Level: {level}", True, (0, 0, 0))
    screen.blit(hp_text, (10, 10))
    screen.blit(level_text, (WIDTH - 120, 10))

# Load sound effects
try:
    shoot_sound = pygame.mixer.Sound("shoot.wav")
    enemy_hit_sound = pygame.mixer.Sound("enemy_hit.wav")
    player_hit_sound = pygame.mixer.Sound("player_hit.wav")
    level_up_sound = pygame.mixer.Sound("level_up.wav")
except pygame.error as e:
    print(f"Error loading sounds: {e}")
    pygame.quit()
    sys.exit()

# Spawn first wave
for _ in range(3):
    enemies.append(spawn_enemy())

# Game loop
running = True
while running:
    draw_floor()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    touch = pygame.mouse.get_pressed()
    if touch[0]:
        pos = pygame.mouse.get_pos()
        if buttons["left"].collidepoint(pos):
            player_rect.x -= player_speed
            last_move_direction = "left"
            player_img = player_left
        if buttons["right"].collidepoint(pos):
            player_rect.x += player_speed
            last_move_direction = "right"
            player_img = player_right
        if buttons["up"].collidepoint(pos):
            player_rect.y -= player_speed
            last_move_direction = "up"
            player_img = player_up
        if buttons["down"].collidepoint(pos):
            player_rect.y += player_speed
            last_move_direction = "down"
            player_img = player_down
        if buttons["fire"].collidepoint(pos):
            bullet = pygame.Rect(player_rect.centerx, player_rect.centery, 8, 5)
            if last_move_direction == "right":
                bullet.x += 20
                bullets.append((bullet, "right"))
            elif last_move_direction == "left":
                bullet.x -= 20
                bullets.append((bullet, "left"))
            elif last_move_direction == "up":
                bullet.y -= 20
                bullet.width = 5
                bullet.height = 8
                bullets.append((bullet, "up"))
            elif last_move_direction == "down":
                bullet.y += 20
                bullet.width = 5
                bullet.height = 8
                bullets.append((bullet, "down"))
            shoot_sound.play()  # Play shooting sound

    for bullet_data in bullets[:]:
        bullet, direction = bullet_data
        if direction == "right":
            bullet.x += bullet_speed
        elif direction == "left":
            bullet.x -= bullet_speed
        elif direction == "up":
            bullet.y -= bullet_speed
        elif direction == "down":
            bullet.y += bullet_speed

        if bullet.left > WIDTH or bullet.right < 0 or bullet.top < 0 or bullet.bottom > HEIGHT:
            bullets.remove(bullet_data)

    for enemy in enemies[:]:
        if enemy.centerx < player_rect.centerx:
            enemy.x += enemy_speed
        if enemy.centerx > player_rect.centerx:
            enemy.x -= enemy_speed
        if enemy.centery < player_rect.centery:
            enemy.y += enemy_speed
        if enemy.centery > player_rect.centery:
            enemy.y -= enemy_speed

        if player_rect.colliderect(enemy):
            player_hp -= 1
            enemies.remove(enemy)
            player_hit_sound.play()  # Play player hit sound
            if player_hp <= 0:
                print("Game Over!")
                running = False

    for bullet_data in bullets[:]:
        bullet, _ = bullet_data
        for enemy in enemies[:]:
            if bullet.colliderect(enemy):
                bullets.remove(bullet_data)
                enemies.remove(enemy)
                enemy_hit_sound.play()  # Play enemy hit sound
                kills += 1
                break

    if kills >= 2:
        level += 1
        kills = 1
        for _ in range(level + 2):
            enemies.append(spawn_enemy())
        level_up_sound.play()  # Play level up sound

    screen.blit(player_img, player_rect)
    for enemy in enemies:
        screen.blit(enemy_img, enemy)
    for bullet_data in bullets:
        bullet, _ = bullet_data
        pygame.draw.rect(screen, (0, 0, 0), bullet)

    draw_buttons()
    draw_status()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
