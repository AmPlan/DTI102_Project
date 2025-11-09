import os
import json 
import math

FILE_PATH = "playerData/player.json" 
COINS_TEXT = "coins"
coins = 0

def loadData():
    global coins
    
    
    folder_path = os.path.dirname(FILE_PATH)
    if folder_path and not os.path.exists(folder_path):
        os.makedirs(folder_path)

    if os.path.exists(FILE_PATH):
        try:
            with open(FILE_PATH, "r") as file:
                data = json.load(file)
                coins = data.get(COINS_TEXT, 0)
                print(f"Data Loaded. Coins: {coins}")
        except Exception as e:
            print(f"Error loading data: {e}")
            coins = 0
    else:
        print("Save file not found. Starting with 0 coins.")
        saveData()
        
def addCoins(amount):
    global coins 
    coins += amount
    saveData() 
    
def saveData():
    global coins 
    try:
        folder_path = os.path.dirname(FILE_PATH)
        if folder_path and not os.path.exists(folder_path):
            os.makedirs(folder_path)
            
        dataToSave = {
            COINS_TEXT : coins
        }
        with open(FILE_PATH, "w") as playerFile:
            json.dump(dataToSave, playerFile)
    except Exception as e:
        print(f"Error saving data: {e}")


loadData()