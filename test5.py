import pygame
import random
import math
import time 
import sys

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("./Asset/Elevator.mp3")
pygame.mixer.music.play(-1)

screen = pygame.display.set_mode((1530, 850))
pygame.display.set_caption("Escape The Office Simulator")

background = pygame.image.load("./Asset/A.jpg")
background = pygame.transform.scale(background, (10000, 10000))


# object_img = pygame.image.load("./Asset/Obstacle.png").convert_alpha()

# object_img = pygame.transform.scale(object_img, (10000, 10000))

bg_width, bg_height = background.get_size()

icon = pygame.image.load("./Asset/game-controller.png")
pygame.display.set_icon(icon)

playerImg = pygame.image.load("./Asset/Player.png")
playerRun = pygame.image.load("./Asset/Running.png")
playerImg = pygame.transform.scale(playerImg, (300, 300))
playerRun = pygame.transform.scale(playerRun, (300, 300))
Player = playerImg
playerX, playerY = 9500, 9500

#miniBoss

miniBoss1 = pygame.image.load("./Asset/mini_Boss1.png")
miniBoss1 = pygame.transform.scale(miniBoss1, (400, 400))
miniBoss1X, miniBoss1Y = 500, 5800
miniBoss2 = pygame.image.load("./Asset/mini_Boss2.png")
miniBoss2 = pygame.transform.scale(miniBoss2, (400, 400))
miniBoss2X, miniBoss2Y = 9500, 5500 
miniBoss3 = pygame.image.load("./Asset/mini_Boss3.png")
miniBoss3 = pygame.transform.scale(miniBoss3, (550, 550))
miniBoss3X, miniBoss3Y = 9080, 4000

player_speed = 5
frame_timer = 0
frame_delay = 1000
toggle = False
facingLeft = False
camX = camY = 0
#-----------------------------------------------------------------------------
wallColor = (255, 255, 255, 255)
def wall(x, y):
    if 0 <= x < bg_width and 0 <= y < bg_height:
        try:
            pixel_color = background.get_at((int(x), int(y)))
            return pixel_color == wallColor
        except IndexError:
            return False
    return True

def player():
    screen.blit(Player, (playerX - camX, playerY - camY))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    moving = False
    newX, newY = playerX, playerY

    if keys[pygame.K_a]:
        newX -= player_speed
        moving = True
        facingLeft = True
    if keys[pygame.K_d]:
        newX += player_speed
        moving = True
        facingLeft = False
    if keys[pygame.K_w]:
        newY -= player_speed
        moving = True
    if keys[pygame.K_s]:
        newY += player_speed
        moving = True
#--------------------------
    collision = False
    check_points = [
        (newX + 150, newY + 50), 
        (newX + 150, newY + 280),
        (newX + 50, newY + 150), 
        (newX + 250, newY + 150),
    ]
    for px, py in check_points:
        if wall(px, py):
            collision = True
            break

    if not collision:
        playerX, playerY = newX, newY

    if moving:
        frame_timer += 1
        if frame_timer >= frame_delay:
            frame_timer = 0
            toggle = not toggle  # Flip between frames
        Player = playerRun if toggle else playerImg
    else:
        Player = playerImg
        toggle = False
    if facingLeft:
        Player = pygame.transform.flip(Player, True, False)


    playerX = max(0, min(playerX, bg_width - 300))
    playerY = max(0, min(playerY, bg_height - 300))

    camX = playerX - screen.get_width() // 2 + 150
    camY = playerY - screen.get_height() // 2 + 150

    camX = max(0, min(camX, bg_width - screen.get_width()))
    camY = max(0, min(camY, bg_height - screen.get_height()))


    screen.fill((255, 255, 255))
    screen.blit(background, (-camX, -camY))
    screen.blit(miniBoss1, (miniBoss1X - camX, miniBoss1Y - camY))
    screen.blit(miniBoss2, (miniBoss2X - camX, miniBoss2Y - camY))
    screen.blit(miniBoss3, (miniBoss3X - camX, miniBoss3Y - camY))
    player()
    pygame.display.update()
pygame.quit
# def player():
#     screen.blit(Player, (playerX - camX, playerY - camY))


# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     keys = pygame.key.get_pressed()
#     moving = False

#     if keys[pygame.K_a]:
#         playerX -= player_speed
#         moving = True
#         facingLeft = True
#     if keys[pygame.K_d]:
#         playerX += player_speed
#         moving = True
#         facingLeft = False
#     if keys[pygame.K_w]:
#         playerY -= player_speed
#         moving = True
#     if keys[pygame.K_s]:
#         playerY += player_speed
#         moving = True

#     if moving:
#         frame_timer += 1
#         if frame_timer >= frame_delay:
#             frame_timer = 0
#             toggle = not toggle
#         Player = playerRun if toggle else playerImg
#     else:
#         Player = playerImg
#         toggle = False

#     if facingLeft:
#         Player = pygame.transform.flip(Player, True, False)

#     playerX = max(0, min(playerX, bg_width - 300))
#     playerY = max(0, min(playerY, bg_height - 300))
#     camX = max(0, min(playerX - screen.get_width() // 2 + 150, bg_width - screen.get_width()))
#     camY = max(0, min(playerY - screen.get_height() // 2 + 150, bg_height - screen.get_height()))

 
#     screen.fill((255, 255, 255))
#     screen.blit(background, (-camX, -camY))
#     player()
#     pygame.display.update()

# pygame.quit()
