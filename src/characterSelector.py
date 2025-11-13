import pygame
from playerData import SCREEN_HEIGHT, SCREEN_WIDTH
import playerData

def init(screen, clock):
    global selectingCharacter, changeScene

    # Variables
    selectingCharacter = None
    changeScene = False
    running = True

    # Game sounds
    CLICK_SOUND = pygame.mixer.Sound(r"Asset\sounds\Minimalist3.mp3")

    # Background
    background = pygame.image.load(r"Asset\images\1.png")
    background = pygame.transform.scale_by(background, 3)

    # Background Rect
    backgroundRect = background.get_rect()
    backgroundRect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    # Fonts
    charSelectFont = pygame.font.Font(r"Asset\fonts\Jacquard12-Regular.ttf", 100)
    selectButtonFont = pygame.font.Font(r"Asset\fonts\Jersey10-Regular.ttf", 50) 

    # character selector
    charSelectLabel = charSelectFont.render("Select your character", 1, (255, 255, 255))

    # character selector Rect
    charSelectRect = charSelectLabel.get_rect()
    charSelectRect.center = (SCREEN_WIDTH / 2, 120)

    # Select Button
    selectButtonLabel = selectButtonFont.render("Select", 1, (255, 255, 255))

    # Select Button Rect
    selectButtonRect = selectButtonLabel.get_rect()
    selectButtonRect.center = (SCREEN_WIDTH / 2, 650)

    # character to select [{image = image, rect = rect}] 
    characters = []

    def createCharacter(path, xOffset):
        character = pygame.image.load(path).convert_alpha()
        character = pygame.transform.scale(character, (120, 130))

        rect = character.get_rect()

        rect.center = (SCREEN_WIDTH / 2 + xOffset, SCREEN_HEIGHT - 250)
        
        characters.append({"character" : character, "rect" : rect, "path" : path})

    createCharacter(r"Asset\Player.png", -300)
    createCharacter(r"Asset\Player2.png", 0)
    createCharacter(r"Asset\Player3.png", 300)

    
    # render characters on screen
    def renderCharacters():
        # draw every characters on screen
        for characterData in characters:
            screen.blit(characterData["character"], characterData["rect"])

        # show border around character if this character is selected
        if selectingCharacter is not None:
            characterRect = characters[selectingCharacter]["rect"]

            pygame.draw.rect(screen, (255, 0, 0), characterRect, 3)


    def mouseInput():
        global changeScene, selectingCharacter
        mousePos = pygame.mouse.get_pos()

        # Select Character
        for i in range(len(characters)):
            characterData = characters[i]
            
            rect = characterData["rect"]

            if not rect.collidepoint(mousePos):
                continue

            selectingCharacter = i
            playerData.playerCharacter = characterData["path"]

            CLICK_SOUND.play()    

        if (selectingCharacter is not None) and (selectButtonRect.collidepoint(mousePos)):
            changeScene = True

    while running:
        for event in pygame.event.get():
            # user clicked X to close window
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                mouseInput()

        screen.blit(background, backgroundRect)
  
        renderCharacters()
  
        screen.blit(charSelectLabel, charSelectRect)

        # show if player already selected character
        if selectingCharacter is not None:
            screen.blit(selectButtonLabel, selectButtonRect)

        if changeScene:
            return "combat"

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
