import pygame
import random
import math
import time 
pygame.init()
pygame.mixer.init()
# breakingST = "./Asset/BreakIn.mp4"
AUGH = pygame.mixer.Sound("./Asset/AUGH.mp3")
AUGH.play(0)
# pygame.mixer.music.play(0)
pygame.mixer.music.load("./Asset/BreakIn.mp3")
# pygame.mixer.music.play(0)
screen = pygame.display.set_mode((1530, 850))
pygame.display.set_caption("Escape The Office Simulator")
background = pygame.image.load("./Asset/juri.jpg")
icon = pygame.image.load("./Asset/game-controller.png")
pygame.display.set_icon(icon)
Final_BossImg = pygame.image.load("./Asset/Final Boss1.png")
Final_BossX = 1190
Final_BossY = 405
Final_Boss = pygame.transform.scale(Final_BossImg, (500,500))


playerImg = pygame.image.load("./Asset/Player.png")
playerX = 570
playerY = 520
playerImg = pygame.transform.scale(playerImg, (300, 300))


playerImg = playerImg.subsurface((0, 0, playerImg.get_width(), 170))
Ani_speed = 10


def player():
    screen.blit(playerImg, (playerX, playerY))



font = pygame.font.Font(None, 48)
# text = font.render("AHHH", True, (0, 0, 0))5
text = "AUGHHH WTH IS THIS SUBJECT! I CAN'T DO THIS ANYMORE!!!"
text1 = ""


dialogue_box = pygame.Surface((1050, 120), pygame.SRCALPHA)
pygame.draw.rect(dialogue_box, (255, 255, 255), dialogue_box.get_rect(), border_radius=20)
pygame.draw.rect(dialogue_box, (0, 0, 0), dialogue_box.get_rect(), 4, border_radius=20)

start_time = pygame.time.get_ticks()


text_index = 0
last_update = time.time()
text_speed = 0.05

flipped = False
breakInST = False
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    

    if text_index < len(text) and (time.time() - last_update) > text_speed:
        text1 += text[text_index]
        text_index += 1
        last_update = time.time()

    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))

    screen.blit(Final_Boss, (Final_BossX, Final_BossY))
    
    screen.blit(dialogue_box, (50, 703))

    text_surface = font.render(text1, True, (0, 0, 0))
    screen.blit(text_surface, (60, 745))

    elapsed_time = pygame.time.get_ticks() - start_time
    if elapsed_time > 3000 and playerX > 0 and not flipped: #playerX ทำไมไม่กำหนดเป็น0จริงๆ?
        playerImg = pygame.transform.flip(playerImg, True, False)
        flipped = True
    if flipped:
        playerX -= Ani_speed
        
    if playerX <= 0 and not breakInST:
        pygame.mixer.music.play(0)
        breakInST = True

    player()

    # screen.blit(text, (90, 740))
    pygame.display.update()
pygame.quit()

#-------------------------------------------------------------------------------

