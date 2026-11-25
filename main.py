
import pygame
import random
from enemy import Enemy
from enemy_bullet import EnemyBullet

pygame.init()

# Game window
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")

clock = pygame.time.Clock()

# -------------------------
# PLAYER SETTINGS
# -------------------------

player = pygame.Rect(375, 530, 50, 30)
player_speed = 8

player_image = pygame.image.load("images/Space_invaders.character.png")
player_image = pygame.transform.scale(player_image, (50, 30))

# Player bullets
bullets = []
bullet_speed = 8
shoot_delay = 700
last_shot = pygame.time.get_ticks()

# Player lives
lives = 3
last_player_hit = -1000
hit_cooldown = 1000

font = pygame.font.SysFont(None, 36)

# -------------------------
# ENEMY SETTINGS
# -------------------------

alien_images = [
    pygame.image.load("images/alien 1 transparent.png"),
    pygame.image.load("images/alien 2 transparent.png"),
    pygame.image.load("images/alien 3 transparent.png")
]

enemies = []
enemy_bullets = []
# WAVE SETTINGS
wave = 1
speed_multiplier = 1.0

# CREATE ENEMY FORMATION
def create_enemies(speed_multiplier):

    new_enemies = []

    for row in range(5):
        for col in range(7):

            x = 190 + col * 60
            y = 40 + row * 50

            image = alien_images[row % len(alien_images)]

            enemy = Enemy(x, y, image, speed_multiplier)
            new_enemies.append(enemy)

    return new_enemies


# Create first wave
enemies = create_enemies(speed_multiplier)



# Enemy shooting
last_shot_time = pygame.time.get_ticks()
shot_delay = 800

# -------------------------
# MAIN GAME LOOP
# -------------------------

running = True

while running:

    current_time = pygame.time.get_ticks()

    screen.fill((0, 0, 0))

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # -------------------------
    # PLAYER SHOOTING
    # -------------------------

    if keys[pygame.K_SPACE] and current_time - last_shot > shoot_delay:

        bullet = pygame.Rect(
            player.centerx - 2,
            player.top,
            5,
            10
        )

        bullets.append(bullet)
        last_shot = current_time

    # Move player bullets
    for bullet in bullets[:]:
        bullet.y -= bullet_speed

        pygame.draw.rect(screen, (255, 255, 255), bullet)

        if bullet.bottom < 0:
            bullets.remove(bullet)

    # -------------------------
    # PLAYER MOVEMENT
    # -------------------------

    if keys[pygame.K_LEFT]:
        player.x -= player_speed
        player.x = max(player.x, 0)

    if keys[pygame.K_RIGHT]:
        player.x += player_speed
        player.x = min(player.x, 750)

    # Draw player
    screen.blit(player_image, player)

    
    # -------------------------
    # ENEMY MOVEMENT
    # -------------------------

    for enemy in enemies:
        enemy.move()

    # Draw enemies
    for enemy in enemies:
        enemy.draw(screen)
    # CHECK IF WAVE IS COMPLETED

    if len(enemies) == 0:

        wave += 1

        speed_multiplier += 0.2

        enemies = create_enemies(speed_multiplier)

        enemy_bullets.clear()
    # PLAYER BULLET - ENEMY COLLISION

    for bullet in bullets[:]:
        for enemy in enemies[:]:

            if bullet.colliderect(enemy.rect):

                bullets.remove(bullet)
                enemies.remove(enemy)

                break

    # ENEMY SHOOTING

    if enemies and current_time - last_shot_time >= shot_delay:

        shooter = random.choice(enemies)

        bullet = EnemyBullet(
            shooter.rect.centerx - 2,
            shooter.rect.bottom
        )

        enemy_bullets.append(bullet)
        last_shot_time = current_time

    # ENEMY BULLET MOVEMENT

    for bullet in enemy_bullets[:]:

        bullet.move()
        bullet.draw(screen)

        if bullet.rect.colliderect(player):

            enemy_bullets.remove(bullet)

            if current_time - last_player_hit >= hit_cooldown:

                lives -= 1
                last_player_hit = current_time
                player.x = 375

                if lives <= 0:
                    running = False

        elif bullet.rect.top > 600:
            enemy_bullets.remove(bullet)

    
    # DISPLAY PLAYER LIVES

    lives_text = font.render(
        f"Lives: {lives}", True, (255, 255, 255)
    )

    screen.blit(lives_text, (20, 15))

    # DISPLAY WAVE NUMBER

    wave_text = font.render(
        f"Wave: {wave}", True, (255, 255, 255)
    )

    screen.blit(wave_text, (650, 15))

    pygame.display.flip()
    clock.tick(60)


pygame.quit()

