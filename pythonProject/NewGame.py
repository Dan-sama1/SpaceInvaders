import pygame
import random
import math
from pygame import mixer
import os

# INITIALIZE THE PYGAME
pygame.init()
# CREATE THE SCREEN
screen = pygame.display.set_mode((800, 600))

# BACKGROUND
background = pygame.image.load('background.png')

# HOME SCREEN BUTTON
button = pygame.image.load('PLAY BUTTON.png')

# BACKGROUND SOUND
mixer.music.load('background music.wav')
mixer.music.play(-1)

# LOAD MUSIC
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
bulletY_Change = 4
bullet_state = 'ready'

# ENEMY
enemyImg = []
enemyX = []
enemyY = []
enemyX_Change = []
enemyY_Change = []
num_of_enemies = 30

# SCORE
score_value = 0
font = pygame.font.Font('ARCADE.TTF', 40)
textX = 15
textY = 15

# BEST SCORE
best_score_file = 'BEST_SCORE.txt'

# GAME OVER TEXT
home_screen_font = pygame.font.Font('ARCADE.TTF', 80)
gameover_font = pygame.font.Font('ARCADE.TTF', 80)
anykey_font = pygame.font.Font('ARCADE.TTF', 25)
display_score_font = pygame.font.Font('ARCADE.TTF', 40)
best_score_font = pygame.font.Font('ARCADE.TTF', 60)

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_Change.append(2)
    enemyY_Change.append(40)


def load_best_score():
    if os.path.exists(best_score_file):
        try:
            with open(best_score_file, 'r') as file:
                score = file.read().strip()
                if score:
                    print(f"Loaded score from file: {score}")  # Debugging line
                    return int(score)
                else:
                    print("File is empty.")  # Debugging line
                    return 0
        except ValueError:
            print("Error: File content is not an integer.")  # Debugging line
            return 0
    else:
        print("File does not exist.")  # Debugging line
        return 0


def save_best_score(score):
    try:
        with open(best_score_file, 'w') as file:
            file.write(str(score))
    except IOError:
        print("Error saving best score.")


# UPDATE BEST SCORE
best_score = load_best_score()


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
        screen.blit(gameover, (214, 250))
    # DISPLAY SCORE
    display_score = display_score_font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(display_score, (327, 310))

    # DISPLAY INSTRUCTION
    key = anykey_font.render("PRESS ANY KEY TO CONTINUE...", True, (255, 255, 255))
    screen.blit(key, (225, 350))


# HOME SCREEN
def home_screen():
    screen.fill((0, 0, 0))

    screen.blit(background, (0, 0))

    home_text = home_screen_font.render("SPACE INVADERS", True, (255, 255, 255))
    screen.blit(home_text, (107, 60))

    display_highest_score = best_score_font.render("BEST SCORE: " + str(best_score), True, (255, 255, 255))
    screen.blit(display_highest_score, (211, 130))

    button_rect = button.get_rect(center=(400, 250))
    screen.blit(button, button_rect)

    pygame.display.update()
    waiting = True
    while waiting:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
                exit()
            if events.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(events.pos):
                    waiting = False
                    reset_game()


def reset_game():
    global playerX, playerY, playerX_change, bullet_state, bulletY, score_value, enemyX, enemyY, enemyX_change, enemyY_change, game_over_sound_played, game_over
    game_over = False
    game_over_sound_played = False
    bullet_state = 'ready'
    bulletY = 480
    score_value = 0
    playerX = 370
    playerY = 445
    playerX_change = 0
    for i in range(num_of_enemies):
        enemyX[i] = random.randint(0, 735)
        enemyY[i] = random.randint(50, 150)
    mixer.music.unpause()
    return game_over


# GAME LOOP TO MAKE SURE THAT THE GAME IS ALWAYS RUNNING
running = True
game_over = False
blink = False
blink_event = pygame.USEREVENT + 1
pygame.time.set_timer(blink_event, 500)
blink_timer = 0
game_over_sound_played = False

home_screen()

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
            if not game_over:
                # LEFT ARROW KEY
                if event.key in [pygame.K_LEFT, pygame.K_a]:
                    playerX_Change = -1
                # RIGHT ARROW KEY
                if event.key in [pygame.K_RIGHT, pygame.K_d]:
                    playerX_Change = 1
                # SPACE KEY - FIRE BULLET
                if event.key == pygame.K_SPACE:
                    if bullet_state == 'ready':
                        bullet_sound.play()
                        # GET THE CURRENT X COORDINATE OF THE SPACESHIP
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)

            else:
                if score_value > best_score:
                    best_score = score_value
                    save_best_score(best_score)
                # RESET THE STATE OF THE GAME IN CASE THE PLAYER TRIES TO PLAY AGAIN
                reset_game()
                home_screen()

        # IF THE KEY IS UNPRESSED
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d]:
                playerX_Change = 0

        # BLINK EVENT
        if event.type == blink_event and game_over:
            blink = not blink
            blink_timer += 1

    # CHECKS IF THE ENEMY COLLIDED WITH THE PLAYER:
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
            # GAME OVER
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

            # IF THE ENEMY HITS THE WALL
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
