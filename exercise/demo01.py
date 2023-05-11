# Simple pygame program
# 1. Example of https://realpython.com/pygame-a-primer/

# Import and initialize the pygame library
import pygame

pygame.init()

DISPLAY_WIDTH = 500
BLOCK_SIZE=DISPLAY_WIDTH/10
# Set up the drawing window
screen = pygame.display.set_mode([DISPLAY_WIDTH, 600])

# Run until the user asks to quit
running = True
circle_y = 250
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    circle_y = circle_y + 0.1
    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draw a solid blue circle in the center
    pygame.draw.circle(screen, (0, 0, 255), (250, circle_y), 75)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()