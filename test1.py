import pygame
import random
import math
import time 
pygame.init()
screen = pygame.display.set_mode((1530, 850))
pygame.display.set_caption("Escape The Office Simulator")
background = pygame.image.load("./Asset/Classroomm.png")
icon = pygame.image.load("./Asset/game-controller.png")
pygame.display.set_icon(icon)


font = pygame.font.Font(None, 48)
# text = font.render("AHHH", True, (0, 0, 0))
text = "AHHHHHHHHHHHHHH"
text1 = ""
dialogue_box = pygame.Surface((1000, 120))
dialogue_box.fill((255, 255, 255))
pygame.draw.rect(dialogue_box, (0, 0, 0), dialogue_box.get_rect(), 4, border_radius=20)


running = True
text_index = 0
last_update = time.time()
text_speed = 0.1



while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if text_index < len(text) and time.time() - last_update > text_speed:
        text1 += text[text_index]
        text_index += 1
        last_update = time.time()

    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))
    
    screen.blit(dialogue_box, (50, 700))

    text_surface = font.render(text1, True, (0, 0, 0))
    screen.blit(text_surface, (90, 740))

    # screen.blit(text, (90, 740))
    pygame.display.update()
pygame.quit()
