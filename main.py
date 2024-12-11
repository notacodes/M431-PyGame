import pygame
import sys

# Initialisierung von pygame
pygame.init()

# Bildschirmgröße und Farben definieren
WIDTH, HEIGHT = 1280, 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Bildschirm erstellen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jump and Run")
clock = pygame.time.Clock()

# Hintergrundbild laden
bg_image = pygame.image.load("kenney_pixel-platformer/BG.jpg")
bg_width = bg_image.get_width()
bg_image = pygame.transform.scale(bg_image, (bg_width, HEIGHT))

# Spieler und Plattform-Eigenschaften
player_image = pygame.image.load("spieler.png")
player_image = pygame.transform.scale(player_image, (50, 50))
player = pygame.Rect(100, HEIGHT - 150, 50, 50)
player_speed = 7
player_velocity_y = 0
player_on_ground = False
can_double_jump = False

# Gegner-Eigenschaften
enemies = [
    pygame.Rect(600, HEIGHT - 120, 50, 50),
    pygame.Rect(1200, HEIGHT - 120, 50, 50),
    pygame.Rect(1800, HEIGHT - 120, 50, 50),
    pygame.Rect(2000, HEIGHT - 120, 50, 50),
    pygame.Rect(2100, HEIGHT - 120, 50, 50)
]
enemy_speed = 2

# Schwerkraft und Bewegung
gravity = 0.9
jump_strength = -18

# Plattformen
platforms = [
    pygame.Rect(0, HEIGHT - 70, bg_width * 3, 70),  # Boden über die gesamte Levelbreite
    pygame.Rect(400, HEIGHT - 300, 200, 20),
    pygame.Rect(800, HEIGHT - 400, 300, 20),
    pygame.Rect(1300, HEIGHT - 500, 150, 20)
]

# Zielbereich
goal = pygame.Rect(bg_width * 3 - 100, HEIGHT - 150, 50, 50)

# UI-Eigenschaften
font = pygame.font.SysFont("Arial", 30)
hearts = 3  # Anzahl der Leben
start_time = pygame.time.get_ticks()

# Scroll-Offset
scroll_x = 0

# Funktionen für die Benutzeroberfläche
def display_hearts():
    """Zeigt die Lebensanzeige oben links an."""
    heart_img = pygame.Surface((30, 30))
    heart_img.fill(RED)
    for i in range(hearts):
        screen.blit(heart_img, (10 + i * 40, 10))

def display_timer():
    """Zeigt den Timer oben rechts an."""
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    timer_text = font.render(f"Zeit: {elapsed_time}s", True, BLACK)
    screen.blit(timer_text, (WIDTH - timer_text.get_width() - 10, 10))

# Spiel-Loop
running = True
while running:
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

    # Kollisionsprüfung mit Plattformen
    player_on_ground = False
    for platform in platforms:
        if player.colliderect(platform) and player_velocity_y > 0:
            player.y = platform.y - player.height
            player_velocity_y = 0
            player_on_ground = True

    # Spieler am Bildschirmrand halten
    if player.x < 0:
        player.x = 0
    if player.y > HEIGHT:
        hearts -= 1  # Ein Leben verlieren
        player.y = HEIGHT - 150
        player_velocity_y = 0
        if hearts <= 0:
            print("Spieler hat alle Leben verloren!")
            running = False

    # Scroll-Logik
    if player.x > WIDTH // 2:
        scroll_x = player.x - WIDTH // 2
    else:
        scroll_x = 0

    # Gegnerbewegung
    for enemy in enemies[:]:
        enemy.x += enemy_speed
        if enemy.left < 0 or enemy.right > bg_width * 3:
            enemy_speed *= -1

        # Kollisionsprüfung mit Spieler
        enemy_rect = enemy.move(-scroll_x, 0)
        if player.colliderect(enemy):
            if player_velocity_y > 0:  # Spieler springt auf den Gegner
                enemies.remove(enemy)
                player_velocity_y = jump_strength  # Spieler springt erneut
            else:  # Spieler kollidiert seitlich mit Gegner
                hearts -= 1
                if hearts <= 0:
                    print("Spieler hat alle Leben verloren!")
                    running = False

    # Ziel erreichen
    if player.colliderect(goal):
        print("Herzlichen Glückwunsch! Du hast das Ziel erreicht!")
        running = False

    # Hintergrund zeichnen (nahtlos wiederholen)
    for i in range(3):  # 3 Hintergrundteile für Levelbreite
        screen.blit(bg_image, ((i * bg_width) - scroll_x, 0))

    # Plattformen zeichnen
    for platform in platforms:
        pygame.draw.rect(screen, WHITE, platform.move(-scroll_x, 0))

    #   zeichnen
    for enemy in enemies:
        enemy_rect = enemy.move(-scroll_x, 0)
        pygame.draw.rect(screen, RED, enemy_rect)

    # Zielbereich zeichnen
    pygame.draw.rect(screen, BLUE, goal.move(-scroll_x, 0))

    # Spieler zeichnen
    screen.blit(player_image, (player.x - scroll_x, player.y))

    # UI anzeigen
    display_hearts()
    display_timer()

    # Bildschirm aktualisieren
    pygame.display.flip()
    clock.tick(60)

# Spiel beenden
pygame.quit()
sys.exit()
