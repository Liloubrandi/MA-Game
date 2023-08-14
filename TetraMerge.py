# Importiere pygame library
import pygame

#importiere random library
import random

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
DISPLAY_WIDTH = 500
DISPLAY_LENGTH = 700
BLOCK_WIDTH = DISPLAY_WIDTH//10
BLOCK_HEIGHT = DISPLAY_LENGTH//14
screen = pygame.display.set_mode([DISPLAY_WIDTH, DISPLAY_LENGTH])

#Variablen:
running = True
rectangle_y = 0
rectangle_x = 0 + 4 * BLOCK_WIDTH
rectangle2_x = 0 + 5 * BLOCK_WIDTH
#list_y = rectangle_x // BLOCK_WIDTH
#list_x = rectangle_y // BLOCK_HEIGHT

board = [
    [False, False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False, False], 
    [False, False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False, False], 
    [False, False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False, False], 
    [False, False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False, False], 
    [False, False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False, False], 
    [False, False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False, False],  
    [False, False, False, False, False, False, False, False, False, False], 
    [False, False, False, False, False, False, False, False, False, False],    
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
        elif event.type == BLOCKFALL:
            rectangle_y = rectangle_y + BLOCK_HEIGHT
            list_x = rectangle_y / BLOCK_HEIGHT'''

class Duo(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.add(Block(BLOCK_WIDTH, BLOCK_HEIGHT, rectangle_x))
        self.add(Block(BLOCK_WIDTH, BLOCK_HEIGHT, rectangle2_x))

    def check_events(events):
        if not Block.is_falling(block): #wieso reicht hier block? Müsste block_2 nicht auch?
            return
        for event in events:
            if event.type == BLOCKFALL:
                Block.move(block, 'down')
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    if block.rect.x + BLOCK_WIDTH <= DISPLAY_WIDTH - BLOCK_WIDTH:
                        Block.move(block, 'right')
                if event.key == K_LEFT:
                    if block.rect.x - BLOCK_WIDTH >= 0:
                        Block.move(block, 'left')

class Block(pygame.sprite.Sprite):
    def __init__(self, width, height, pos_x):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = 0
        self.number = random.randint(1, 6)

    def move(self, direction):
        if direction == 'down':
            board[self.rect.y//BLOCK_HEIGHT][self.rect.x//BLOCK_WIDTH] = False
            self.rect.y = self.rect.y + BLOCK_HEIGHT
        if direction == 'right':
            board[self.rect.y//BLOCK_HEIGHT][self.rect.x//BLOCK_WIDTH] = False
            self.rect.x = self.rect.x + BLOCK_WIDTH
        if direction == 'left':
            board[self.rect.y//BLOCK_HEIGHT][self.rect.x//BLOCK_WIDTH] = False
            self.rect.x = self.rect.x - BLOCK_WIDTH

    def is_falling(self):
        if self.rect.y < DISPLAY_LENGTH - BLOCK_HEIGHT:
            if board[self.rect.y//BLOCK_HEIGHT+ 1][self.rect.x//BLOCK_WIDTH] == False:
                return True
    
    '''def check_events(self, events):
        if not self.is_falling():
            return
        for event in events:
            #global list_x, list_y
            if event.type == KEYDOWN:
                #soll der Block nach recht oder links verschoben werden?
                if event.key == K_RIGHT:
                    if self.rect.x + BLOCK_WIDTH <= DISPLAY_WIDTH - BLOCK_WIDTH:
                        if board[self.rect.y//BLOCK_HEIGHT][self.rect.x//BLOCK_WIDTH + 1] == False:
                            board[self.rect.y//BLOCK_HEIGHT][self.rect.x//BLOCK_WIDTH] = False
                            self.rect.x = self.rect.x + BLOCK_WIDTH
                        #list_y = self.rect.x // BLOCK_WIDTH
                if event.key == K_LEFT:
                    if self.rect.x - BLOCK_WIDTH >= 0:
                        if board[self.rect.y//BLOCK_HEIGHT][self.rect.x//BLOCK_WIDTH - 1] == False:
                            board[self.rect.y//BLOCK_HEIGHT][self.rect.x//BLOCK_WIDTH] = False
                            self.rect.x = self.rect.x - BLOCK_WIDTH
                        #list_y = self.rect.x // BLOCK_WIDTH
            #soll der Block nach unten fallen?
            elif event.type == BLOCKFALL:
                if self.rect.y + BLOCK_HEIGHT <= DISPLAY_LENGTH - BLOCK_HEIGHT:
                    board[self.rect.y//BLOCK_HEIGHT][self.rect.x//BLOCK_WIDTH] = False
                    self.rect.y = self.rect.y + BLOCK_HEIGHT
                    #list_x = self.rect.y // BLOCK_HEIGHT'''
    

#Kreiere ein eigenes Event, welches jede Sekunde ausgeführt wird -> um den Block nach unten zu bewegen
BLOCKFALL = pygame.USEREVENT + 1
pygame.time.set_timer(BLOCKFALL, 500)

#block = Block(BLOCK_WIDTH, BLOCK_HEIGHT, rectangle_x)
#block_2 = Block(BLOCK_WIDTH, BLOCK_HEIGHT, rectangle2_x)
block = Duo()

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
    #for block in block_group:
        #block.check_events(events)
    for block in block_group:
        Duo.check_events(events)
    if block.is_falling():
        has_active_block = True

    if not has_active_block:
        block = Duo()
        block_group.add(block)

    #Hintergrund weiss machen
    screen.fill((255, 255, 255))

    #Zeichne ein Rechteck oben in die Mitte
    #pygame.draw.rect(screen, (255, 0, 0), [rectangle_x, rectangle_y, BLOCK_WIDTH, BLOCK_HEIGHT])

    for block in block_group:
        screen.blit(block.image, block.rect)
        list_x = block.rect.x // BLOCK_WIDTH
        list_y = block.rect.y // BLOCK_HEIGHT
        if not board[list_y][list_x]:
            board[list_y][list_x] = block
            '''for row in board:
                print(row)
            print(' ')'''
    
    #block_group.draw(screen)
    #Flip the display - aktualisieren
    pygame.display.flip()

#ganz am Ende
pygame.quit()
