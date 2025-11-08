import json

FILE_PATH = r"PlayerData\player.json"
COINS_TEXT = "coins"

coins = 0

def addCoins(amount):
    global coins

    coins += amount
    saveData()

def saveData():
    global coins
    playerFile = open(FILE_PATH, "w")

    dataToSave = {
        COINS_TEXT : coins
    }

    json.dump(dataToSave, playerFile)
    playerFile.close()
    

def loadData():
    global coins
    coins = 0
    try:
        playerFile = open(FILE_PATH, "r")
        playerDataJSON = playerFile.read()
        playerData = json.loads(playerDataJSON)

        
        coins = playerData[COINS_TEXT]

        playerFile.close()

    except FileNotFoundError:
        pass

loadData()