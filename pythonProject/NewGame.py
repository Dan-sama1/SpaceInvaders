import pygame
import random
import math
from pygame import mixer

# INITIALIZE THE PYGAME
pygame.init()
# CREATE THE SCREEN
screen = pygame.display.set_mode((800, 600))

# BACKGROUND
background = pygame.image.load('background.png')

#BACKGROUND SOUND
mixer.music.load('background music.wav')
mixer.music.play(-1)

#LOAD MUSIC
bullet_sound = mixer.Sound('laser.wav')
explosion_sound = mixer.Sound('explosion.wav')
game_over_sound = mixer.Sound('game over.wav')

# TITLE AND ICON
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# PLAYER
playerImg = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 445
playerX_Change = 0

# BULLET
# READY STATE - BULLET IS NOT VISIBLE
# FIRE - THE BULLET IS CURRENTLY MOVING
bulletIMG = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_Change = 0
bulletY_Change = 1
bullet_state = 'ready'

# ENEMY
enemyImg = []
enemyX = []
enemyY = []
enemyX_Change = []
enemyY_Change = []
num_of_enemies = 6

# SCORE
score_value = 0
font = pygame.font.Font('ARCADE.TTF', 40)
textX = 15
textY = 15

#GAME OVER TEXT
gameover_font = pygame.font.Font('ARCADE.TTF', 80)


for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_Change.append(0.2)
    enemyY_Change.append(40)

# PLAYER
def player(x, y, blink):
    if blink:
        white_surface = pygame.Surface((64, 64))
        white_surface.fill((255, 255, 255))
        screen.blit(white_surface, (x, y))
    # draw the player on our game
    screen.blit(playerImg, (x, y))


# BULLET
def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletIMG, (x + 16, y + 5))


# ENEMY
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# COLLISION
def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    return False


def is_player_collision(enemyX, enemyY, playerX, playerY):
    distance = math.sqrt(math.pow(enemyX - playerX, 2) + (math.pow(enemyY - playerY, 2)))
    return distance < 27


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def gameover_text(blink):
    if blink:
        gameover = gameover_font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(gameover, (250, 250))


# GAME LOOP TO MAKE SURE THAT THE GAME IS ALWAYS RUNNING
running = True
game_over = False
blink = False
blink_event = pygame.USEREVENT + 1
pygame.time.set_timer(blink_event, 500)
blink_timer = 0
game_over_sound_played = False

while running:
    # ADD COLORS (R, G ,B)
    screen.fill((0, 0, 0))

    # BACKGROUND IMAGE
    screen.blit(background, (0, 0))

    # CREATE EVENT
    for event in pygame.event.get():
        # CLOSING THE GAME
        if event.type == pygame.QUIT:
            running = False
        # IF KEY IS PRESSED CHECK IF IT'S LEFT OR RIGHT
        if event.type == pygame.KEYDOWN:

            # LEFT ARROW KEY
            if event.key == pygame.K_LEFT:
                playerX_Change = -0.4

            # LEFT A KEY
            if event.key == pygame.K_a:
                playerX_Change = -0.4

            # RIGHT ARROW KEY
            if event.key == pygame.K_d:
                playerX_Change = 0.4

            # RIGHT ARROW KEY
            if event.key == pygame.K_RIGHT:
                playerX_Change = 0.4

            # SPACE KEY - FIRE BULLET
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bullet_sound.play()
                    # GET THE CURRENT X COORDINATE OF THE SPACESHIP
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        # IF THE KEY IS UNPRESSED
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_Change = 0

            if event.key == pygame.K_a or event.key == pygame.K_d:
                playerX_Change = 0

        #BLINK EVENT
        if event.type == blink_event and game_over:
            blink = not blink
            blink_timer += 1

    #CHECKS IF THE ENEMY COLLIDED WITH THE PLAYER:
    if not game_over:
        # ALGORITHM OF THE GAME
        # UPDATE PLAYER MOVEMENT(SIDEWAYS)
        playerX += playerX_Change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # ENEMY MOVEMENTS
        for i in range(num_of_enemies):

            #GAME OVER
            if is_player_collision(enemyX[i], enemyY[i], playerX, playerY):
                game_over = True
                blink_timer = 0
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                mixer.music.pause()
                if not game_over_sound_played:
                    game_over_sound.play()
                    game_over_sound_played = True
                break
            #IF THE ENEMY HITS THE WALL
            enemyX[i] += enemyX_Change[i]
            if enemyX[i] <= 0:
                enemyX_Change[i] = 0.1
                enemyY[i] += enemyY_Change[i]
            elif enemyX[i] >= 736:
                enemyX_Change[i] = -0.1
                enemyY[i] += enemyY_Change[i]

            # COLLISION
            collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                explosion_sound.play()
                bulletY = 480
                bullet_state = 'ready'
                score_value += 1
                enemyX[i] = random.randint(0, 735)
                enemyY[i] = random.randint(50, 150)
            # ENEMY
            enemy(enemyX[i], enemyY[i], i)

        # BULLET MOVEMENT
        if bulletY <= 0:
            bulletY = 480
            bullet_state = 'ready'

        # CHECK BULLET STATE
        if bullet_state == 'fire':
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_Change

        # ADD THE PLAYER IN THE SCREEN
        player(playerX, playerY, blink)
        show_score(textX, textY)
    else:
        if blink_timer < 5:
            player(playerX, playerY, blink)
        gameover_text(blink)

    pygame.display.update()  # THIS LINE IS ALWAYS NEEDED BECAUSE WE NEED OUR GAME TO ALWAYS UPDATE
