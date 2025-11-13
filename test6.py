import math
import pygame
import random
import time
import sys

pygame.init()
pygame.display.set_caption("Escape The Office Simulator")
icon = pygame.image.load("./Asset/game-controller.png")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((1530, 850))
background = pygame.image.load("./Asset/Boss1.png")
background = pygame.transform.scale(background, (1530,850))
pygame.mixer.init()
pygame.mixer.music.load("./Asset/mini.mp3")
pygame.mixer.music.play(-1)
Boss1 = pygame.image.load("./Asset/mini_Boss1.png")
Boss1 = pygame.transform.scale(Boss1, (500, 500))
Boss1X, Boss1Y = (900, 250)
C1 = pygame.image.load("./Asset/C1.png")
C1 = pygame.transform.scale(C1, (600, 600))
C1X, C1Y = (900, 250)
player = pygame.image.load("./Asset/Player.png")
player = pygame.transform.scale(player, (450, 450))
playerX, playerY = (0, 440)
Hurt = pygame.image.load("./Asset/HURT.png")
Hurt = pygame.transform.scale(Hurt, (600, 700))
HurtX, HurtY = (0, 360)

font = pygame.font.Font(None, 48)
text = "AJ.Noh: You're too weak to confront an inferrior being"
text1 = ""
text_index = 0
text_speed = 0.05
last_update = time.time()


ShowBoss = True
ShowC1 = False
ShowPlayer = True
ShowHurt = False
CHurt = 0
Defeat = False
C1_time = 0
Hurt_time = 0


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # keys = pygame.key.get_pressed()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ShowC1 = True
                ShowBoss = False
                C1_time = pygame.time.get_ticks()

            if event.key == pygame.K_LSHIFT:
                ShowHurt = True
                ShowPlayer = False
                Hurt_time = pygame.time.get_ticks()
                CHurt += 1
    
    if ShowC1 and pygame.time.get_ticks() - C1_time > 300:
        ShowC1 = False
        ShowBoss = True

    if ShowHurt and pygame.time.get_ticks() - Hurt_time > 300 and not Defeat:
        ShowHurt = False
        ShowPlayer = True

    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    if ShowBoss == True:
        screen.blit(Boss1, (Boss1X, Boss1Y))
    else:
        screen.blit(C1, (C1X, C1Y))
    if ShowPlayer == True:
        screen.blit(player, (playerX, playerY))
    else:
        screen.blit(Hurt, (HurtX, HurtY))
    if CHurt >= 3:
        Defeat = True
    if Defeat:
        ShowPlayer = False
        ShowHurt = True
        dialogue_box = pygame.Surface((890, 120))
        dialogue_box.fill((255, 255, 255))
        pygame.draw.rect(dialogue_box, (0, 0, 0), dialogue_box.get_rect(), 4, border_radius=20)
        # start_time = pygame.time.get_ticks()
        if text_index < len(text) and (time.time() - last_update) > text_speed:
            text1 += text[text_index]
            text_index += 1
            last_update = time.time()
        screen.blit(dialogue_box, (320, 703))
        text_surface = font.render(text1, True, (0, 0, 0))
        screen.blit(text_surface, (335, 745))
        

    pygame.display.update()
pygame.quit