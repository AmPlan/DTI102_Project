import pygame

SCREEN_WIDTH  = 1280
SCREEN_HEIGHT = 720

# Set up
pygame.init()
screen  = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock   = pygame.time.Clock()
running = True


# Get system font with size of 18
font = pygame.font.SysFont("Arial", 18) 

# Game loop
while running:

    # player's action on window
    for event in pygame.event.get():
        # user clicked X to close window
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    testText = font.render("Hello World!", True, (0, 0, 0))

    screen.blit(testText, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

    # update the whole screen
    pygame.display.flip()

    # Limit the frame rate to 60
    clock.tick(60)

# Stop the game
pygame.quit()