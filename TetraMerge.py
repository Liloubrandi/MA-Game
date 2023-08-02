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
BLOCK_WIDTH = DISPLAY_WIDTH//9
BLOCK_HEIGHT = DISPLAY_LENGTH//13
screen = pygame.display.set_mode([DISPLAY_WIDTH, DISPLAY_LENGTH])

#Variablen:
running = True
rectangle_y = 0
rectangle_x = 0 + 4 * BLOCK_WIDTH
#list_y = rectangle_x // BLOCK_WIDTH
#list_x = rectangle_y // BLOCK_HEIGHT

board = [
    [False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False], 
    [False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False], 
    [False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False], 
    [False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False], 
    [False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False], 
    [False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False],  
    [False, False, False, False, False, False, False, False, False],    
]

'''def check_events(events, block):
    #Hat der Spieler die Escapetaste gedrückt oder das Fenster geschlossen? 
    for event in pygame.event.get():
        global rectangle_x, running, rectangle_y, list_x, list_y
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            #soll der Block nach recht oder links verschoben werden?
            if event.key == K_RIGHT:
                rectangle_x = rectangle_x + BLOCK_WIDTH
                list_y = rectangle_x / BLOCK_WIDTH
            if event.key == K_LEFT:
                rectangle_x = rectangle_x - BLOCK_WIDTH
                list_y = rectangle_x / BLOCK_WIDTH
        #soll der Block nach unten fallen?
        elif event.type == MOVEBLOCK:
            rectangle_y = rectangle_y + BLOCK_HEIGHT
            list_x = rectangle_y / BLOCK_HEIGHT'''

class Block(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = rectangle_x
        self.rect.y = 0

    def check_events(self, events):
        if not self.is_falling():
            return
        for event in events:
            #global list_x, list_y
            if event.type == KEYDOWN:
                #soll der Block nach recht oder links verschoben werden?
                if event.key == K_RIGHT:
                    if self.rect.x + BLOCK_WIDTH <= DISPLAY_WIDTH - BLOCK_WIDTH:
                        if board[self.rect.y//BLOCK_HEIGHT][self.rect.x//BLOCK_WIDTH + 1] != True:
                            board[self.rect.y//BLOCK_HEIGHT][self.rect.x//BLOCK_WIDTH] = False
                            self.rect.x = self.rect.x + BLOCK_WIDTH
                        #list_y = self.rect.x // BLOCK_WIDTH
                if event.key == K_LEFT:
                    if self.rect.x - BLOCK_WIDTH >= 0:
                        if board[self.rect.y//BLOCK_HEIGHT][self.rect.x//BLOCK_WIDTH - 1] != True:
                            board[self.rect.y//BLOCK_HEIGHT][self.rect.x//BLOCK_WIDTH] = False
                            self.rect.x = self.rect.x - BLOCK_WIDTH
                        #list_y = self.rect.x // BLOCK_WIDTH
            #soll der Block nach unten fallen?
            elif event.type == MOVEBLOCK:
                if self.rect.y + BLOCK_HEIGHT <= DISPLAY_LENGTH - BLOCK_HEIGHT:
                    board[self.rect.y//BLOCK_HEIGHT][self.rect.x//BLOCK_WIDTH] = False
                    self.rect.y = self.rect.y + BLOCK_HEIGHT
                    #list_x = self.rect.y // BLOCK_HEIGHT

    def is_falling(self):
        if self.rect.y < DISPLAY_LENGTH - BLOCK_HEIGHT:
            if board[self.rect.y//BLOCK_HEIGHT+ 1][self.rect.x//BLOCK_WIDTH] != True:
                return True
    

#Kreiere ein eigenes Event, welches jede Sekunde ausgeführt wird -> um den Block nach unten zu bewegen
MOVEBLOCK = pygame.USEREVENT + 1
pygame.time.set_timer(MOVEBLOCK, 500)

block = Block(BLOCK_WIDTH, BLOCK_HEIGHT)

block_group = pygame.sprite.Group()
block_group.add(block)

#While-Schlaufe - machen bis running = False
while running:
    events = pygame.event.get()
    # check events
    for event in events:
        #Hat der Spieler die Escapetaste gedrückt oder das Fenster geschlossen? 
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

    has_active_block = False
    for block in block_group:
        block.check_events(events)
        if block.is_falling():
            has_active_block = True

    if not has_active_block:
        block = Block(BLOCK_WIDTH, BLOCK_HEIGHT)
        block_group.add(block)

    #Hintergrund weiss machen
    screen.fill((255, 255, 255))

    # if rectangle_y > DISPLAY_LENGTH - BLOCK_HEIGHT:
    #     fest_x = rectangle_x
    #     rectangle_x = 0 + 4 * BLOCK_WIDTH
    #     rectangle_y = 0
    # #Nach oben braucht es nicht, da es ja nie nach oben geht
    # if rectangle_x > DISPLAY_WIDTH - BLOCK_WIDTH:
    #     rectangle_x = DISPLAY_WIDTH - BLOCK_WIDTH
    # if rectangle_x < 0:
    #     rectangle_x = 0

    #Zeichne ein Rechteck oben in die Mitte
    #pygame.draw.rect(screen, (255, 0, 0), [rectangle_x, rectangle_y, BLOCK_WIDTH, BLOCK_HEIGHT])

    for block in block_group:
        screen.blit(block.image, block.rect)
        list_x = block.rect.x // BLOCK_WIDTH
        list_y = block.rect.y // BLOCK_HEIGHT
        if not board[list_y][list_x]:
            board[list_y][list_x] = True
            '''for row in board:
                print(row)
            print(' ')'''

    
    #block_group.draw(screen)
    # Flip the display - aktualisieren
    pygame.display.flip()

#ganz am Ende
pygame.quit()
