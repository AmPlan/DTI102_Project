import pygame

FILE_PATH = "playerData/player.json" 
COINS_TEXT = "coins"
coins = 0

SCREEN_WIDTH  = 1280
SCREEN_HEIGHT = 720
screenMode = pygame.FULLSCREEN | pygame.SCALED

def addCoins(amount):
    global coins 
    coins += amount
