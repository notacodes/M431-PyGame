import pygame
import sys

# Initialisierung von pygame
pygame.init()

# Bildschirmgröße und Farben definieren
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Bildschirm erstellen
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Jump and Run")
clock = pygame.time.Clock()

# Skalierungsfaktor für Spielfiguren und Plattformen
scale_factor = WIDTH / 1920

# Spieler und Plattform-Eigenschaften
player_image = pygame.image.load("spieler.png")  # Lade das Spieler-Bild
player_image = pygame.transform.scale(player_image, (50, 50))  # Skalieren des Spieler-Bilds
player = pygame.Rect(100 * scale_factor, HEIGHT - 150 * scale_factor, 50 * scale_factor, 50 * scale_factor)
player_speed = 7 * scale_factor
player_velocity_y = 0
player_on_ground = False
can_double_jump = False

# Gegner-Eigenschaften
enemies = [
    pygame.Rect(600 * scale_factor, HEIGHT - 150 * scale_factor, 50 * scale_factor, 50 * scale_factor),
    pygame.Rect(1200 * scale_factor, HEIGHT - 200 * scale_factor, 50 * scale_factor, 50 * scale_factor)
]

enemy_speed = 3 * scale_factor

# Schwerkraft und Bewegung
gravity = 0.9 * scale_factor
jump_strength = -18 * scale_factor

# Plattformen: (bewegende und feste)
platforms = [
    pygame.Rect(0, HEIGHT - 100 * scale_factor, WIDTH, 50 * scale_factor),  # Boden jetzt bildschirmbreit
    pygame.Rect(400 * scale_factor, HEIGHT - 300 * scale_factor, 200 * scale_factor, 20 * scale_factor),
    pygame.Rect(800 * scale_factor, HEIGHT - 400 * scale_factor, 300 * scale_factor, 20 * scale_factor),
    pygame.Rect(1300 * scale_factor, HEIGHT - 500 * scale_factor, 150 * scale_factor, 20 * scale_factor)
]

moving_platforms = [
    {"rect": pygame.Rect(600 * scale_factor, HEIGHT - 350 * scale_factor, 200 * scale_factor, 20 * scale_factor), "speed": 3 * scale_factor, "direction": 1},
    {"rect": pygame.Rect(1000 * scale_factor, HEIGHT - 250 * scale_factor, 150 * scale_factor, 20 * scale_factor), "speed": 4 * scale_factor, "direction": -1}
]

# UI-Eigenschaften
font = pygame.font.SysFont("Arial", 30)  # Kleinere Schrift für kompaktere Anzeige
hearts = 3  # Anzahl der Leben
start_time = pygame.time.get_ticks()

# Funktionen für die Benutzeroberfläche
def display_hearts():
    """Zeigt die Lebensanzeige (Herzen) oben links an."""
    heart_img = pygame.Surface((30, 30))  # Kleinere Herzen
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
    screen.fill(WHITE)

    # Ereignisse verarbeiten
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.size
            scale_factor = WIDTH / 1920

            # Spielfiguren und Plattformen neu skalieren
            player.width, player.height = 50 * scale_factor, 50 * scale_factor
            player_image = pygame.transform.scale(pygame.image.load("spielr.png"), (int(50 * scale_factor), int(50 * scale_factor)))
            platforms[0].width = WIDTH
            for p in platforms[1:]:
                p.width, p.height = p.width * scale_factor, p.height * scale_factor
            for mp in moving_platforms:
                mp["rect"].width, mp["rect"].height = mp["rect"].width * scale_factor, mp["rect"].height * scale_factor

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
                hearts -= 1  # Ein Leben verlieren
                if hearts <= 0:
                    print("Spieler hat alle Leben verloren!")
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
    screen.blit(player_image, (player.x, player.y))  # Spielerbild zeichnen

    # UI anzeigen
    display_hearts()
    display_timer()

    # Bildschirm aktualisieren
    pygame.display.flip()
    clock.tick(60)

# Spiel beenden
pygame.quit()
sys.exit()
