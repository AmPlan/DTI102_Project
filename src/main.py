import pygame
import playerData

# Set up
pygame.init()
pygame.mixer.init()
pygame.font.init()

screen = pygame.display.set_mode((playerData.SCREEN_WIDTH, playerData.SCREEN_HEIGHT), playerData.screenMode)
clock  = pygame.time.Clock()

pygame.display.set_caption("Office Syndrome")
icon = pygame.image.load("./Asset/game-controller.png")
pygame.display.set_icon(icon)


def _changeScene(scene, screen, clock):
    match scene:
        case "mainMenu":
            import mainMenu
            return mainMenu.init(screen, clock)
        case "combat":
            import combatTest
            return combatTest.init(screen, clock)
        case "cutscene":
            import cutscene
            return cutscene.init(screen, clock)
        case "characterSelector":
            import characterSelector
            return characterSelector.init(screen, clock)


def changeScene(scene, screen, clock): 
    while True:
        if scene is None:
            break
        
        scene = _changeScene(scene, screen, clock)
    

if __name__ == "__main__":
    changeScene("cutscene", screen, clock)
