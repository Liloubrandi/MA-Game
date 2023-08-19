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

class Duo(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        block = Block(BLOCK_WIDTH, BLOCK_HEIGHT, rectangle_x)
        block_2 = Block(BLOCK_WIDTH, BLOCK_HEIGHT, rectangle2_x)
        self.add(block)
        self.add(block_2)
        self.x = rectangle2_x
        self.y = 0

    def move_down(self):
        pass

    def move_left(self):
        pass

    def move_right(self):
        pass

    def is_falling(self):
        if self.y < DISPLAY_LENGTH - BLOCK_HEIGHT:
            if board[self.y//BLOCK_HEIGHT + 1][self.x//BLOCK_WIDTH] == False:
                return True

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
            board[self.list.y][self.list_x] = False
            self.rect.y = self.rect.y + BLOCK_HEIGHT
        if direction == 'right':
            board[self.list.y][self.list_x] = False
            self.rect.x = self.rect.x + BLOCK_WIDTH
        if direction == 'left':
            board[self.list.y][self.list_x] = False
            self.rect.x = self.rect.x - BLOCK_WIDTH
    
    @property #macht, dass die Methode eine Eigenschaft ist, welche ohne Klammern (list_x anstatt list_x()) angesprochen werden kann
    def list_x(self):
        return self.rect.x // BLOCK_WIDTH
    
    @property
    def list_y(self):
        return self.rect.y // BLOCK_HEIGHT

#Kreiere ein eigenes Event, welches jede Sekunde ausgeführt wird -> um den Block nach unten zu bewegen
BLOCKFALL = pygame.USEREVENT + 1
pygame.time.set_timer(BLOCKFALL, 500)

#block = Block(BLOCK_WIDTH, BLOCK_HEIGHT, rectangle_x)
#block_2 = Block(BLOCK_WIDTH, BLOCK_HEIGHT, rectangle2_x)
duo = Duo()
#block_group = pygame.sprite.Group()
#block_group.add(block)
duo_group = []
duo_group.append(duo)

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
    for block in duo_group:
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    block.move_right()
                if event.key == K_LEFT:
                    block.move_left()
            if event.type == BLOCKFALL:
                block.move_down()

    if block.is_falling():
        has_active_block = True

    if not has_active_block:
        duo = Duo()
        duo_group.append(duo)

    #Hintergrund weiss machen
    screen.fill((255, 255, 255))

    #Zeichne ein Rechteck oben in die Mitte
    #pygame.draw.rect(screen, (255, 0, 0), [rectangle_x, rectangle_y, BLOCK_WIDTH, BLOCK_HEIGHT])

    for duo in duo_group:
        for block in duo:
            screen.blit(block.image, block.rect)
            if not board[block.list_y][block.list_x]:
                board[block.list_y][block.list_x] = block
                '''for row in board:
                    print(row)
                print(' ')'''
    
    #block_group.draw(screen)
    #Flip the display - aktualisieren
    pygame.display.flip()

#ganz am Ende
pygame.quit()
