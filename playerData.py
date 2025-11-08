# import json

import pygame

SCREEN_WIDTH  = 1280
SCREEN_HEIGHT = 720

screenMode = pygame.FULLSCREEN | pygame.SCALED

coins = 0

# def saveData():
#     global coins
#     playerFile = open(FILE_PATH, "w")
# 
#     dataToSave = {
#     }
# 
#     json.dump(dataToSave, playerFile)
#     playerFile.close()
#     
# 
# def loadData():
#     try:
#         playerFile = open(FILE_PATH, "r")
#         playerDataJSON = playerFile.read()
#         playerData = json.loads(playerDataJSON)
# 
#         
#         playerFile.close()
# 
#     except FileNotFoundError:
#         pass
