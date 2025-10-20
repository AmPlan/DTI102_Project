import pygame

# Set up
pygame.init()
screen  = pygame.display.set_mode((1280, 720))
clock   = pygame.time.Clock()
running = True

# Game loop
while running:

    # player's action on window
    for event in pygame.event.get():
        # user clicked X to close window
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # update the whole screen
    pygame.display.flip()

    # Limit the frame rate to 60
    clock.tick(60)

# Stop the game
pygame.quit()

# bag