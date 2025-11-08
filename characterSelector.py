import pygame

SCREEN_WIDTH  = 1280
SCREEN_HEIGHT = 720



pygame.init()
screen  = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock   = pygame.time.Clock()
running = True

background = pygame.image.load(r"Asset\images\1.png")
background = pygame.transform.scale_by(background, 3)

backgroundRect = background.get_rect()
backgroundRect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

charSelectFont = pygame.font.Font(r"Asset\fonts\Jacquard12-Regular.ttf", 100)
selectButtonFont = pygame.font.Font(r"Asset\fonts\Jersey10-Regular.ttf", 50) 

charSelectLabel = charSelectFont.render("Select your character", 1, (255, 255, 255))
selectButtonLabel = selectButtonFont.render("Select", 1, (255, 255, 255))

charSelectRect = charSelectLabel.get_rect()
charSelectRect.center = (SCREEN_WIDTH / 2, 120)

selectButtonRect = selectButtonLabel.get_rect()
selectButtonRect.center = (SCREEN_WIDTH / 2, 650)



# [{image = image, rect = rect}] 
characters = []

def createCharacter(path, xOffset):
    character = pygame.image.load(path).convert_alpha()
    character = pygame.transform.scale(character, (120, 130))
    rect = character.get_rect()
    rect.center = (SCREEN_WIDTH / 2 + xOffset, SCREEN_HEIGHT - 250)
    characters.append({"character" : character, "rect" : rect})
    

createCharacter(r"Asset\Player.png", -300)
createCharacter(r"Asset\Player2.png", 0)
createCharacter(r"Asset\Player3.png", 300)

selectingCharacter = None

def renderCharacters():
    for characterData in characters:
        screen.blit(characterData["character"], characterData["rect"])

    try:
        characterRect = characters[selectingCharacter]["rect"]
        pygame.draw.rect(screen, (255, 0, 0), characterRect, 3)
    except TypeError:
        # show nothing if found no character from selectingCharacter
        pass


def mouseInput():
    mousePos = pygame.mouse.get_pos()

    # Select Character
    for i in range(len(characters)):
        characterData = characters[i]
        rect = characterData["rect"]

        if rect.collidepoint(mousePos):
            global selectingCharacter
            selectingCharacter = i
    
    if (selectingCharacter is not None) and (selectButtonRect.collidepoint(mousePos)):
        print(f"Your Character is {selectingCharacter}")
 

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

    pygame.display.flip()
    clock.tick(60)

pygame.quit()