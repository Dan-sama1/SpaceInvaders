import pygame
import random

# INITIALIZE THE PYGAME
pygame.init()
# CREATE THE SCREEN
screen = pygame.display.set_mode((800, 600))

# TITLE AND ICON
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# PLAYER
playerImg = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 445
playerX_Change = 0

# ENEMY
enemyImg = pygame.image.load('alien.png')
enemyX = random.randint(0, 800)
enemyY = random.randint(50, 150)
enemyX_Change = 0.3
enemyY_Change = 40


def player(x, y):
    # draw the player on our game
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


# GAME LOOP TO MAKE SURE THAT THE GAME IS ALWAYS RUNNING
running = True
while running:
    # ADD COLORS (R, G ,B)
    screen.fill((0, 0, 0))

    # CREATE EVENT
    for event in pygame.event.get():
        # CLOSING THE GAME
        if event.type == pygame.QUIT:
            running = False
        # IF KEY IS PRESSED CHECK IF IT'S LEFT OR RIGHT
        if event.type == pygame.KEYDOWN:

            # LEFT ARROW KEY
            if event.key == pygame.K_LEFT:
                playerX_Change = -0.3

            # RIGHT ARROW KEY
            if event.key == pygame.K_RIGHT:
                playerX_Change = 0.3

        # IF THE KEY IS UNPRESSED
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_Change = 0

    #ALGORIITHM OF THE GAME
    # UPDATE PLAYER MOVEMENT(SIDEWAYS)
    playerX += playerX_Change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    #ENEMY MOVEMENTS
    enemyX += enemyX_Change
    if enemyX <= 0:
        enemyX_Change = 0.2
        enemyY += enemyY_Change
    elif enemyX >= 736:
        enemyX_Change = -0.2
        enemyY += enemyY_Change
    # ADD THE PLAYER IN THE SCREEN
    player(playerX, playerY)
    enemy(enemyX, enemyY)
    pygame.display.update()  # THIS LINE IS ALWAYS NEEDED BECAUSE WE NEED OUR GAME TO ALWAYS UPDATE
