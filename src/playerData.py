import pygame
import json

FILE_PATH = "playerData/player.json" 
COINS_TEXT = "coins"

SCREEN_WIDTH  = 1280
SCREEN_HEIGHT = 720

screenMode = pygame.FULLSCREEN | pygame.SCALED

coins = 0

def addCoins(amount):
    global coins 
    coins += amount

def saveData():
    global coins
    playerFile = open(FILE_PATH, "w")

    dataToSave = {
        COINS_TEXT: coins
    }

    json.dump(dataToSave, playerFile)
    playerFile.close()
    

def loadData():
    global coins
    try:
        playerFile = open(FILE_PATH, "r")
        playerDataJSON = playerFile.read()
        playerData = json.loads(playerDataJSON)

        coins = playerData[COINS_TEXT] 
        
        playerFile.close()

    except FileNotFoundError:
        pass

loadData()