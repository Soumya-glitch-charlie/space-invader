import pygame
import math
import random
from pygame import mixer

# initialize the game
pygame.init()
clock = pygame.time.Clock()

# create the visual screen
gamescreen = pygame.display.set_mode((900, 600))

# Background Music addition
mixer.music.load("background.wav")
mixer.music.play(-1)

# Title and Logo
pygame.display.set_caption("SPACE-INVADERS")
icon = pygame.image.load("logo.png")
background = pygame.image.load("background.png")
pygame.display.set_icon(icon)

# player
ship_image = pygame.image.load("space-ship.png")
playerposition_X = 400
playerposition_Y = 500
playerpositionX_change = 0
playerpositionY_change = 0

# enemy
enemy_image = []
enemyposition_X = []
enemyposition_Y = []
enemypositionX_change = []
enemypositionY_change = []
num_enemy = 6

for i in range(num_enemy):
    enemy_image.append(pygame.image.load("enemy.png"))
    enemyposition_X.append(random.randint(0, 835))
    enemyposition_Y.append(random.randint(50, 100))
    enemypositionX_change.append(3)
    enemypositionY_change.append(25)

# bullets
bullet_image = pygame.image.load("bullets.png")
bulletposition_X = 0
bulletposition_Y = 500
bulletpositionX_change = 0
bulletpositionY_change = 15
bullet_state = "ready"


#  default score
score = 0
font = pygame.font.Font("Fatal Fighter.ttf", 30)
textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font("Fatal Fighter.ttf", 69)

# Replay text
replay_button_font = pygame.font.Font("Fatal Fighter.ttf", 69)


# Funtion definition


def score_create(x, y):
    score_value = font.render("Your Score: " + str(score), True, (255, 255, 255))
    gamescreen.blit(score_value, (x, y))


def game_over_text():
    GO_text = over_font.render("GAME OVER!! :-( ", True, (255, 255, 255))
    gamescreen.blit(GO_text, (230, 200))


def replay_game_text():
    replay_text = replay_button_font.render("REPLAY :-)", True, (255, 255, 255))
    gamescreen.blit(replay_text, (230, 300))


def player(x, y):
    gamescreen.blit(ship_image, (x, y))


def enemy(x, y, i):
    gamescreen.blit(enemy_image[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    gamescreen.blit(bullet_image, (x + 15, y + 15))


def isCollision(enemyposition_X, enemyposition_Y, bulletposition_X, bulletposition_Y):
    distance = math.sqrt(
        math.pow(enemyposition_X - bulletposition_X, 2)
        + math.pow(enemyposition_Y - bulletposition_Y, 2)
    )
    if distance < 30:
        return True
    else:
        return False


# Game loop
running = True
while running:
    # rgb color setting for bg color
    gamescreen.fill((0, 0, 0))

    # background inclusion
    gamescreen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # basically to check the keystroke whether it is pressed right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerpositionX_change = -7
            if event.key == pygame.K_RIGHT:
                playerpositionX_change = 7
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()

                    # get the current x coordinate of space ship
                    bulletposition_X = playerposition_X
                    fire_bullet(bulletposition_X, bulletposition_Y)
        
        # restart the game
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Reset the game state
                score = 0
                for i in range(num_enemy):
                    enemyposition_X[i] = random.randint(0, 835)
                    enemyposition_Y[i] = random.randint(50, 100)

        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerpositionX_change = 0

    # checking for player space ship so that it doesn't go out of bounds
    playerposition_X += playerpositionX_change
    if playerposition_X <= 0:
        playerposition_X = 0
    elif playerposition_X >= 836:
        playerposition_X = 836

    # enemy movement tracker
    for i in range(num_enemy):
        # Game Over
        if enemyposition_Y[i] > 369:
            for j in range(num_enemy):
                enemyposition_Y[j] = 2000
            game_over_text()
        
        if enemyposition_Y[i] > 369:
            for j in range(num_enemy):
                enemyposition_Y[j] = 2000
            replay_game_text()
            break
        
        enemyposition_X[i] += enemypositionX_change[i]
        if enemyposition_X[i] <= 0:
            enemypositionX_change[i] = 4.56
            enemyposition_Y[i] += enemypositionY_change[i]
        elif enemyposition_X[i] >= 836:
            enemypositionX_change[i] = -5.67
            enemyposition_Y[i] += enemypositionY_change[i]

        # Collision detection with enemy
        collision = isCollision(
            enemyposition_X[i], enemyposition_Y[i], bulletposition_X, bulletposition_Y
        )
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletposition_Y = 500
            bullet_state = "ready"
            score += 1
            print(score)
            enemyposition_X[i] = random.randint(0, 835)
            enemyposition_Y[i] = random.randint(50, 100)

        enemy(enemyposition_X[i], enemyposition_Y[i], i)

    # bullet movement
    if bulletposition_Y <= 0:
        bulletposition_Y = 500
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletposition_X, bulletposition_Y)
        bulletposition_Y -= bulletpositionY_change

    player(playerposition_X, playerposition_Y)
    score_create(textX, textY)
    pygame.display.update()
