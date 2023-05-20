# Importiere pygame library
import pygame

# Importiere pygame.locals, um einen einfacheren Zugang zu Tasten zu haben
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

#initialize
pygame.init()

#Parameter für Bildschirm und Block und Bildschirmerstellung
DISPLAY_WIDTH = 450
DISPLAY_LENGTH = 650
BLOCK_WIDTH = DISPLAY_WIDTH/9
BLOCK_HIGHT = DISPLAY_LENGTH/13
screen = pygame.display.set_mode([DISPLAY_WIDTH, DISPLAY_LENGTH])

def links_oder_rechts():
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                rectangle_x = rectangle_x + BLOCK_WIDTH
            if event.key == K_LEFT:
                rectangle_x = rectangle_x - BLOCK_WIDTH 
    return rectangle_x

#While-Schlaufe - machen bis running = False
running = True
rectangle_y = 250
rectangle_x = 0 + 4 * BLOCK_WIDTH
while running:

    #Hat der Spieler die Escapetaste gedrückt oder das Fenster geschlossen? 
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            #hat der Spieler den Block nach rechts oder links verschoben?
            if event.key == K_RIGHT:
                rectangle_x = rectangle_x + BLOCK_WIDTH
            if event.key == K_LEFT:
                rectangle_x = rectangle_x - BLOCK_WIDTH

    rectangle_y = rectangle_y + 0.01

    #Hintergrund weiss machen
    screen.fill((255, 255, 255))

    #Überprüfe, ob sich der Block verschieben soll
    #links_oder_rechts()

    # Draw a solid blue circle in the center
    pygame.draw.rect(screen, (255, 0, 0), [rectangle_x, rectangle_y, BLOCK_WIDTH, BLOCK_HIGHT])

    # Flip the display - aktualisieren
    pygame.display.flip()
#ganz am Ende
pygame.quit()
