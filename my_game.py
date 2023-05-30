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

'''
def links_oder_rechts():
    global rectangle_x
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                rectangle_x = rectangle_x + BLOCK_WIDTH
            if event.key == K_LEFT:
                rectangle_x = rectangle_x - BLOCK_WIDTH'''

def check_events():
    #Hat der Spieler die Escapetaste gedrückt oder das Fenster geschlossen? 
    for event in pygame.event.get():
        global rectangle_x, running, rectangle_y
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_RIGHT:
                rectangle_x = rectangle_x + BLOCK_WIDTH
            if event.key == K_LEFT:
                rectangle_x = rectangle_x - BLOCK_WIDTH
        elif event.type == MOVEBLOCK:
            rectangle_y = rectangle_y + BLOCK_HIGHT

#Kreiere ein eigenes Event, welches jede Sekunde ausgeführt wird -> um den Block nach unten zu bewegen
MOVEBLOCK = pygame.USEREVENT + 1
pygame.time.set_timer(MOVEBLOCK, 1000)

#While-Schlaufe - machen bis running = False
running = True
rectangle_y = 0
rectangle_x = 0 + 4 * BLOCK_WIDTH
while running:

    check_events()

    '''#Hat der Spieler die Escapetaste gedrückt oder das Fenster geschlossen? 
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
                rectangle_x = rectangle_x - BLOCK_WIDTH'''

    #rectangle_y = rectangle_y + 0.01

    #Hintergrund weiss machen
    screen.fill((255, 255, 255))

    if rectangle_y > DISPLAY_LENGTH - BLOCK_HIGHT:
        rectangle_y = DISPLAY_LENGTH - BLOCK_HIGHT
    #Nach oben braucht es nicht, da es ja nie nach oben geht
    if rectangle_x > DISPLAY_WIDTH - BLOCK_WIDTH:
        rectangle_x = DISPLAY_WIDTH - BLOCK_WIDTH
    if rectangle_x < 0:
        rectangle_x = 0

    #Zeichne ein Rechteck oben in die Mitte
    pygame.draw.rect(screen, (255, 0, 0), [rectangle_x, rectangle_y, BLOCK_WIDTH, BLOCK_HIGHT])

    # Flip the display - aktualisieren
    pygame.display.flip()

#ganz am Ende
pygame.quit()
