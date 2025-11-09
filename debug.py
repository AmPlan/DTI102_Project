import pygame
import playerData

# ถ้า vscode รันไฟล์นี้ก็ set up pygame แล้วก็ทำให้ฟังชั่นหลักของ script ทำงาน
def setup(name, init):

    if name == "__main__":
        print(name)
        pygame.init()
        pygame.mixer.init() # Initial the game sounds
    
        screen = pygame.display.set_mode((playerData.SCREEN_WIDTH, playerData.SCREEN_HEIGHT))
        clock  = pygame.time.Clock()
    
        init(screen, clock)
    