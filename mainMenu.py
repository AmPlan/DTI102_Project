import pygame
import pygame.mixer_music as music

SCREEN_WIDTH  = 1280
SCREEN_HEIGHT = 720
TITLE_COLOR = (207, 228, 255)
BUTTON_TEXT_COLOR = (224, 238, 255)

backgroundMovement = 0

### Set up
pygame.init()
pygame.mixer.init() # Initial the game sounds

screen  = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
clock   = pygame.time.Clock()
running = True

SCREEN_RECT = screen.get_rect()

gameTitleFont = pygame.font.Font(r"assets\fonts\Jacquard12-Regular.ttf", 100) # Get system font with size of 70
font = pygame.font.Font(r"assets\fonts\Jersey10-Regular.ttf", 50) # Get system font with size of 30

delta = 0

### Ui elements

# all ui elements as dictionary that needed to be displayed
uiElements  = {} # {uiElement : rect }
uiButtons   = {}
backgrounds = {}

def createBackground(path):
    background = pygame.image.load(path).convert_alpha()
    background = pygame.transform.scale(background, (1280, 853))
    rect = background.get_rect()
    rect.center = SCREEN_RECT.center

    backgrounds[background] = rect

def createButton(text, offset):
    button = font.render(text, True, BUTTON_TEXT_COLOR)
    buttonRect = button.get_rect()
    buttonRect.center = SCREEN_RECT.center
    buttonRect.centery += offset

    interactRect = buttonRect.copy()
    interactRect.width  = 200
    interactRect.height = 50
    interactRect.center = SCREEN_RECT.center
    interactRect.centery += offset

    uiElements[button] = buttonRect
    uiButtons[button]  = interactRect

    return button

    
# background
createBackground(r"assets\images\1.png")
createBackground(r"assets\images\2.png")
createBackground(r"assets\images\3.png")
createBackground(r"assets\images\4.png")
createBackground(r"assets\images\5.png")



# gameTitle
gameTitle = gameTitleFont.render("Office Syndrome", True, TITLE_COLOR)
gameTitleRect = gameTitle.get_rect()
gameTitleRect.center = SCREEN_RECT.center
gameTitleRect.centery -= 220

# startButton
startButton   = createButton("Play", 50)
settingButton = createButton("Setting", 140)
exitButton    = createButton("Exit", 230)
uiElements[gameTitle]  = gameTitleRect

### Functions

def renderUiElements():

    # fill the screen with a color to wipe away anything from last frame
    screen.fill((58, 96, 113))

    
    scrollSpeed = 0.25
    global backgroundMovement
    backgroundMovement += 0.1 * delta

    for background, rect in backgrounds.items():
        rect.x = backgroundMovement * -scrollSpeed
        if rect.x < - rect.width:
            rect.x = -(abs(rect.x) % rect.width)
        copiedRect = rect.copy()
        copiedRect.x += rect.width

        screen.blit(background, rect)
        screen.blit(background, copiedRect)
        scrollSpeed += 0.2

    for uiElement, rect in uiElements.items():
        screen.blit(uiElement, rect)

def mouseInput():
    
    for buttonRect in uiButtons.values():
        if not buttonRect.collidepoint(pygame.mouse.get_pos()): 
            continue
        
        if buttonRect == uiButtons[startButton]:
            # Start button
            print("Start")
        elif buttonRect == uiButtons[settingButton]:
            # Setting Button
            print("Setting")
        elif buttonRect == uiButtons[exitButton]:
            # Exit button
            global running
            running = False

### In Game 
music.load("assets\musics\Eric Skiff - Underclocked (underunderclocked mix).mp3")
music.play()

while running:

    # player's action on window
    for event in pygame.event.get():
        # user clicked X to close window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            mouseInput()

    renderUiElements()

    # # Debug Buttons Collisions
    # for button in uiButtons.values():
    #     pygame.draw.rect(screen, "red", button, 1)

    # update the whole screen
    pygame.display.flip()

    # Limit the frame rate to 60
    delta = clock.tick(60)

# Stop the game
pygame.quit()