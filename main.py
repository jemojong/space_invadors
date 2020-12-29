import pygame
import random
import math
from pygame import mixer

# initialize
pygame.init()

# Background
background = pygame.image.load("background.png")
# Backgroubd Sound
mixer.music.load("background.wav")
mixer.music.play(-1)
# create the screen
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Space-invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("playerr.png")
playerX = 370
playerY = 500
playerXchange = 0

# Enemy
enemyImg = pygame.image.load("space-invaders.png")
enemyX = random.randint(0, 736)
enemyY = random.randint(40, 150)
enemyXchange = 4
enemyYchange = 40

# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletYchange = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10


def show_score(x, y):
    score = font.render("Score:" + str(score_value), True, (2, 255, 25))
    screen.blit(score, (textX, textY))


def game_over_text():
    over_score = font.render("GAME OVER YOU LOST", True, (2, 255, 25))
    screen.blit(over_score, (200, 250))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def enemy(enemyX, enemyY):
    screen.blit(enemyImg, (enemyX, enemyY))


def player(x, y):
    screen.blit(playerImg, (playerX, playerY))


# Collision
def isCollision(enemyX, bulletX, enemyY, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop

running = True
while running:
    # Screen color
    screen.fill((0, 0, 0))
    # Screen Background
    screen.blit(background, (0, 0))

    # Quit Game Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerXchange = -5

            if event.key == pygame.K_RIGHT:
                playerXchange = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerXchange = 0
            if event.key == pygame.K_RIGHT:
                playerXchange = 0

    # Enemy Movement
    enemyX += enemyXchange
    if enemyX > 736:
        enemyXchange = enemyXchange * -1
        enemyY += enemyYchange
    elif enemyX < 0:
        enemyXchange = enemyXchange * -1
        enemyY += enemyYchange

    # checking boundaries
    playerX += playerXchange
    if playerX < 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletYchange

    if enemyY > 440:
        aenemyY = 2000
        game_over_text()
        break
    # Collision
    collision = isCollision(enemyX, bulletX, enemyY, bulletY)
    if collision:
        collision_sound = mixer.Sound('explosion.wav')
        collision_sound.play()
        bulletY = 480
        bullet_state = "ready"
        score_value += 1
        enemyX = random.randint(0, 736)
        enemyY = random.randint(40, 150)

    player(playerX, playerY)
    show_score(textX, textY)
    enemy(enemyX, enemyY)
    pygame.display.update()
