import pygame
import math
import random
from pygame import mixer

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 600))

mixer.music.load("background.wav")
mixer.music.play(-1)

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo(1).png")
pygame.display.set_icon(icon)

playerImage = pygame.image.load("ufo(5).png")
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0


def player(x, y):
    screen.blit(playerImage, (x, y))


invaderImage = []
invaderX = []
invaderY = []
invaderX_change = []
invaderY_change = []
noofinvaders = 6
for i in range(noofinvaders):
    invaderImage.append(pygame.image.load("ufo(7).png"))
    invaderX.append(random.randint(0, 736))
    invaderY.append(random.randint(50, 150))
    invaderX_change.append(0.3)
    invaderY_change.append(40)


def invader(x, y, i):
    screen.blit(invaderImage[i], (x, y))


bulletImage = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1
bullet_state = "ready"

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

over_font = pygame.font.Font('freesansbold.ttf', 64)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (200,250))


def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x,y))


def firebullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImage, (x + 16, y + 10))


def iscolliding(invaderX, invaderY, bulletX, bulletY):
    distance = math.sqrt((bulletX - invaderX) ** 2 + (bulletY - invaderY) ** 2)
    if distance < 30:
        return True
    return False


running = True
while running:
    screen.fill((0, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state=='ready':
                    #bulletsound = mixer.Sound("laser.wav")
                    #bulletsound.play()
                    bulletX = playerX
                    firebullet(bulletX, bulletY)



        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
    playerX += playerX_change

    if playerX <= 0:
        playerX_change = 0.5
    if playerX >= 736:
        playerX_change = -0.5

    for i in range(noofinvaders):

        if invaderY[i] > 436:
            for j in range(noofinvaders):
                invaderY[j] = 2000
            game_over_text()
            break
        invaderX[i] += invaderX_change[i]
        if invaderX[i] <= 0:
            invaderX_change[i] = 0.3
            invaderY[i] += invaderY_change[i]
        if invaderX[i] >= 736:
            invaderX_change[i] = -0.3
            invaderY[i] += invaderY_change[i]
        if iscolliding(invaderX[i], invaderY[i], bulletX, bulletY):
            # explosionsound = mixer.music.load('explosion.wav')
            # mixer.music.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            invaderX[i] = random.randint(0, 736)
            invaderY[i] = random.randint(50, 150)

        invader(invaderX[i], invaderY[i], i)

    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 480
    if bullet_state is "fire":
        firebullet(bulletX, bulletY)
        bulletY -= bulletY_change
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
