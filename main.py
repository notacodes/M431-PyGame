import pygame
import sys

# Initialisierung von pygame
pygame.init()

# Bildschirmgröße und Farben definieren
WIDTH, HEIGHT = 1920, 1080
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Bildschirm erstellen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jump and Run")
clock = pygame.time.Clock()

# Spieler und Plattform-Eigenschaften
player = pygame.Rect(100, HEIGHT - 150, 50, 50)
player_speed = 7
player_velocity_y = 0
player_on_ground = False
can_double_jump = False

# Gegner-Eigenschaften
enemies = [
    pygame.Rect(600, HEIGHT - 150, 50, 50),
    pygame.Rect(1200, HEIGHT - 200, 50, 50)
]

enemy_speed = 3

# Schwerkraft und Bewegung
gravity = 0.9
jump_strength = -18

# Plattformen: (bewegende und feste)
platforms = [
    pygame.Rect(0, HEIGHT - 100, WIDTH, 50),  # Boden jetzt bildschirmbreit
    pygame.Rect(400, HEIGHT - 300, 200, 20),
    pygame.Rect(800, HEIGHT - 400, 300, 20),
    pygame.Rect(1300, HEIGHT - 500, 150, 20)
]

moving_platforms = [
    {"rect": pygame.Rect(600, HEIGHT - 350, 200, 20), "speed": 3, "direction": 1},
    {"rect": pygame.Rect(1000, HEIGHT - 250, 150, 20), "speed": 4, "direction": -1}
]

# Spiel-Loop
running = True
while running:
    screen.fill(WHITE)

    # Ereignisse verarbeiten
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Spielerbewegung
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player.x += player_speed
    if keys[pygame.K_SPACE]:
        if player_on_ground:
            player_velocity_y = jump_strength
            can_double_jump = True
            player_on_ground = False
        elif can_double_jump:
            player_velocity_y = jump_strength
            can_double_jump = False

    # Schwerkraft und Bewegung nach unten
    player_velocity_y += gravity
    player.y += player_velocity_y

    # Kollisionsprüfung mit festen Plattformen
    player_on_ground = False
    for platform in platforms:
        if player.colliderect(platform) and player_velocity_y > 0:
            player.y = platform.y - player.height
            player_velocity_y = 0
            player_on_ground = True

    # Kollisionsprüfung mit bewegenden Plattformen
    for moving in moving_platforms:
        platform = moving["rect"]
        if player.colliderect(platform) and player_velocity_y > 0:
            player.y = platform.y - player.height
            player_velocity_y = 0
            player_on_ground = True

        # Plattformbewegung
        platform.x += moving["speed"] * moving["direction"]
        if platform.left < 0 or platform.right > WIDTH:
            moving["direction"] *= -1

    # Gegnerbewegung
    for enemy in enemies:
        enemy.x += enemy_speed
        if enemy.left < 0 or enemy.right > WIDTH:
            enemy_speed *= -1

    # Kollisionsprüfung mit Gegnern
    for enemy in enemies[:]:
        if player.colliderect(enemy):
            if player_velocity_y > 0:  # Spieler springt auf Gegner
                enemies.remove(enemy)
                player_velocity_y = jump_strength  # Spieler springt erneut
            else:
                print("Spieler getroffen!")
                running = False

    # Spieler am Bildschirmrand halten
    if player.x < 0:
        player.x = 0
    if player.x > WIDTH - player.width:
        player.x = WIDTH - player.width
    if player.y > HEIGHT:
        player.y = HEIGHT - player.height
        player_velocity_y = 0

    # Plattformen zeichnen
    for platform in platforms:
        pygame.draw.rect(screen, GREEN, platform)

    for moving in moving_platforms:
        pygame.draw.rect(screen, BLACK, moving["rect"])

    # Gegner zeichnen
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)

    # Spieler zeichnen
    pygame.draw.rect(screen, BLUE, player)

    # Bildschirm aktualisieren
    pygame.display.flip()
    clock.tick(60)

# Spiel beenden
pygame.quit()
sys.exit()
