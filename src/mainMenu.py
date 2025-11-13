import pygame
import pygame.mixer
import pygame.mixer_music as music
import playerData

TITLE_COLOR = (207, 228, 255)
BUTTON_TEXT_COLOR = (224, 238, 255)
BUTTON_HOVER_TEXT_COLOR = (124, 129, 135)

def init(screen, clock):
    global backgroundMovement, running, backgrounds, changeToNextScene

    pygame.display.set_mode((playerData.SCREEN_WIDTH, playerData.SCREEN_HEIGHT), playerData.screenMode)
    
    # Variables
    changeToNextScene = False
    running = True

    backgroundMovement = 0
    delta = 0

    # Sounds
    SCREEN_RECT = screen.get_rect()
    HOVER_SOUND = pygame.mixer.Sound(r"Asset\sounds\Minimalist1.mp3")
    CLICK_SOUND = pygame.mixer.Sound(r"Asset\sounds\Minimalist3.mp3")

    # Fonts
    gameTitleFont = pygame.font.Font(r"Asset\fonts\Jacquard12-Regular.ttf", 100) # Get system font with size of 70
    font          = pygame.font.Font(r"Asset\fonts\Jersey10-Regular.ttf", 50) # Get system font with size of 30

    ### Ui elements

    # all ui elements as dictionary that needed to be displayed
    uiElements  = {} # {uiElement : rect }
    uiButtons   = {} # {string :  {rect, interactRect, normal, hover, isHover}}
    backgrounds = {}

    def createBackground(path):
        # Create background
        background = pygame.image.load(path).convert_alpha()
        background = pygame.transform.scale(background, (1280, 853))

        # Create rect
        rect = background.get_rect()
        rect.center = SCREEN_RECT.center

        # save to backgrounds list
        backgrounds[background] = rect

    def createButton(text, offset):
        button = font.render(text, True, BUTTON_TEXT_COLOR)
        buttonRect = button.get_rect()
        buttonRect.center = SCREEN_RECT.center
        buttonRect.centery += offset

        buttonHover = font.render(text, True, BUTTON_HOVER_TEXT_COLOR)

        interactRect = buttonRect.copy()
        interactRect.width  = 200
        interactRect.height = 50
        interactRect.center = SCREEN_RECT.center
        interactRect.centery += offset

        uiButtons[text] = {
            "rect" : buttonRect,
            "interactRect" : interactRect,
            "normal" : button,
            "hover" : buttonHover,
            "isHover" : False
            }

        return button

    # backgrounds
    createBackground(r"Asset\images\1.png")
    createBackground(r"Asset\images\2.png")
    createBackground(r"Asset\images\3.png")
    createBackground(r"Asset\images\4.png")
    createBackground(r"Asset\images\5.png")

    # Game Title
    gameTitle = gameTitleFont.render("Office Syndrome", True, TITLE_COLOR)

    # Game Title Rect
    gameTitleRect = gameTitle.get_rect()
    gameTitleRect.center = SCREEN_RECT.center
    gameTitleRect.centery -= 220

    # Save game title as ui element
    uiElements[gameTitle]  = gameTitleRect

    # Game Buttons
    createButton("Play", 50)
    createButton("Exit", 140)

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

        for button in uiButtons.values():
            rect = button["rect"]
            buttonRect = button["interactRect"]
            if buttonRect.collidepoint(pygame.mouse.get_pos()):
                # If player hover for first time play the sound
                if (not button["isHover"]):
                    HOVER_SOUND.play()
                    button["isHover"] = True

                screen.blit(button["hover"], rect)
            else:
                screen.blit(button["normal"], rect)

                # Player leave the button prepare to play sound next time
                button["isHover"] = False

    def mouseInput():

        for buttonName, button in uiButtons.items():
            buttonRect = button["interactRect"]
            if not buttonRect.collidepoint(pygame.mouse.get_pos()): 
                continue

            CLICK_SOUND.play()

            match buttonName:
                case "Play":
                    global changeToNextScene
                    changeToNextScene = True
                case "Exit":
                    global running
                    running = False

    ### In Game 
    music.load(r"Asset\musics\Eric Skiff - Underclocked (underunderclocked mix).mp3")
    music.play(-1)

    while running:
        
        # player's action on window
        for event in pygame.event.get():
            # user clicked X to close window
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                mouseInput()

        renderUiElements()

        # update the whole screen
        pygame.display.flip()

        if changeToNextScene:
            return "characterSelector"

        # Limit the frame rate to 60
        delta = clock.tick(60)

    # Stop the game
    pygame.quit()
