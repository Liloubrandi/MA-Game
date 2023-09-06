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

YELLOW = (255, 255, 0)
RED = (204, 0, 0)
GREEN = (0, 204, 0)
BLUE = (0, 0, 204)
PURPLE = (102, 0, 204)
PINK = (204, 0, 204)

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
timer = 500
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

class Board(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        duo = Duo()
        self.add(duo)

    def is_right_free(self):
        pass

    def left_is_free(self):
        pass

    def is_falling(self):
        pass

class Duo(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        block = Block(BLOCK_WIDTH, BLOCK_HEIGHT, rectangle_x)
        block_2 = Block(BLOCK_WIDTH, BLOCK_HEIGHT, rectangle2_x)
        self.add(block)
        self.add(block_2)
        self.rotation = 'horizontal_right'
    
    @property
    def blocks(self):
        return self.sprites()

    def move_down(self):
        for block in self.blocks:
            block.move('down')

    def move_left(self):
        for block in self.blocks:
            block.move('left')

    def move_right(self):
        for block in self.blocks:
            block.move('right')

    @property
    def lowest_block(self):
        #Voraussetzung: Es hat genau zwei Blöcke
        #Wenn beide die gleichen y-Koordinaten haben -> waagerecht
        #Wenn beide andere y-Koordinaten haben -> senkrecht
        if self.blocks[0].rect.y == self.blocks[1].rect.y:
            return self.blocks
        else:
            if self.blocks[0].rect.y > self.blocks[1].rect.y:
                return [self.blocks[0]] #Wieso braucht es hier diese Listenklammern?
            else:
                return [self.blocks[1]]
            
    @property
    def highest_block(self):
        if self.blocks[0].rect.y == self.blocks[1].rect.y:
            return self.blocks
        else:
            if self.blocks[0].rect.y > self.blocks[1].rect.y:
                return [self.blocks[1]]
            else:
                return [self.blocks[1]]
            
    @property
    def right_block(self):
        #Voraussetzung: Es hat genau zwei Blöcke
        #Wenn beide die gleichen x-Koordinaten haben -> senkrecht
        #Wenn beide andere x-Koordinaten haben -> waagerecht
        if self.blocks[0].rect.x == self.blocks[1].rect.x:
            return self.blocks
        else:
            if self.blocks[0].rect.x > self.blocks[1].rect.x:
                return [self.blocks[0]]
            else:
                return [self.blocks[1]]
    
    @property
    def left_block(self):
        #Voraussetzung: Es hat genau zwei Blöcke
        #Wenn beide die gleichen x-Koordinaten haben -> senkrecht
        #Wenn beide andere x-Koordinaten haben -> waagerecht
        if self.blocks[0].rect.x == self.blocks[1].rect.x:
            return self.blocks
        else:
            if self.blocks[0].rect.x > self.blocks[1].rect.x:
                return [self.blocks[1]]
            else:
                return [self.blocks[0]]

    def is_falling(self):
        is_falling = True
        for block in self.lowest_block:
            if is_falling and block.rect.y < DISPLAY_LENGTH - BLOCK_HEIGHT: 
                if board[block.list_y + 1][block.list_x] != False:
                    is_falling = False
            else:
                is_falling = False
        return is_falling
            
    def is_right_free(self):
        is_right_free = True
        for block in self.right_block:
            if is_right_free and block.rect.x < DISPLAY_WIDTH - BLOCK_WIDTH:
                if board[block.list_y][block.list_x + 1] != False:
                    is_right_free = False
            else:
                is_right_free = False
        return is_right_free

    def is_left_free(self):
        is_left_free = True 
        for block in self.left_block:
            if is_left_free and block.rect.x > 0:
                if board[block.list_y][block.list_x - 1] != False:
                    is_left_free = False
            else:
                is_left_free = False
        return is_left_free
                
    def rotate(self):
        if self.rotation == 'horizontal_right':
            for block in self.right_block:
                board[block.list_y][block.list_x] = False
                block.rect.y += BLOCK_HEIGHT
                block.rect.x -= BLOCK_WIDTH
            self.rotation = 'vertical_down'
        elif self.rotation == 'vertical_down':
            if self.is_left_free():
                for block in self.lowest_block:
                    board[block.list_y][block.list_x] = False
                    block.rect.y -= BLOCK_HEIGHT
                    block.rect.x -= BLOCK_WIDTH
                self.rotation = 'horizontal_left'
        elif self.rotation == 'horizontal_left':
            for block in self.left_block:
                board[block.list_y][block.list_x] = False
                block.rect.y -= BLOCK_HEIGHT
                block.rect.x += BLOCK_WIDTH
            self.rotation = 'vertical_up'
        elif self.rotation == 'vertical_up':
            if self.is_right_free():
                for block in self.highest_block:
                    board[block.list_y][block.list_x] = False
                    block.rect.y += BLOCK_HEIGHT
                    block.rect.x += BLOCK_WIDTH
                self.rotation = 'horizontal_right'

class Block(pygame.sprite.Sprite):
    def __init__(self, width, height, pos_x):
        super().__init__()
        self.number = random.randint(1, 6)
        self.image = pygame.Surface((width, height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = 0
    
    @property
    def color(self):
        if self.number == 1:
            return YELLOW
        if self.number == 2:
            return RED
        if self.number == 3:
            return PINK
        if self.number == 4:
            return PURPLE
        if self.number == 5:
            return BLUE
        if self.number == 6:
            return GREEN

    def move(self, direction):
        if direction == 'down':
            board[self.list_y][self.list_x] = False
            self.rect.y = self.rect.y + BLOCK_HEIGHT
        if direction == 'right':
            board[self.list_y][self.list_x] = False
            self.rect.x = self.rect.x + BLOCK_WIDTH
        if direction == 'left':
            board[self.list_y][self.list_x] = False
            self.rect.x = self.rect.x - BLOCK_WIDTH
    
    @property #macht, dass die Methode eine Eigenschaft ist, welche ohne Klammern (list_x anstatt list_x()) angesprochen werden kann
    def list_x(self):
        return self.rect.x // BLOCK_WIDTH
    
    @property
    def list_y(self):
        return self.rect.y // BLOCK_HEIGHT     

'''def mergen(x, y, number):
    #Rahmenbedingungen
    if x < 0 or x > DISPLAY_WIDTH - BLOCK_WIDTH:
        return False
    if y < 0 or y > DISPLAY_LENGTH - BLOCK_HEIGHT:
        return False
    #Feld überprüfen
    if board[y // BLOCK_HEIGHT][x // BLOCK_WIDTH].number == number:
        board[y // BLOCK_HEIGHT][x // BLOCK_WIDTH]  = False
        mergen(Block.rect.x, Block.rect.y + BLOCK_HEIGHT, Block.number) #unten
        mergen(Block.rect.x, Block.rect.y - BLOCK_HEIGHT, Block.number) #oben
        mergen(Block.rect.x + BLOCK_WIDTH, Block.rect.y, Block.number) #recht
        mergen(Block.rect.x - BLOCK_WIDTH, Block.rect.y, Block.number) #links
        
def fill(x, y):
    board[x][y].number = board[x][y].number + 1
    if board[x][y].number == 6:
        board[x][y] == False
    for row in range(DISPLAY_LENGTH // BLOCK_HEIGHT, 0, -1):
        for field in range(DISPLAY_LENGTH // BLOCK_HEIGHT, 0, -1):
            if board[row][field] == False:
                row_index = row 
                while row_index > 0 and board[row_index][field] == 0:
                    row_index = row_index - 1
                board[row][field] = board[row_index][field]
                board[row_index][field] = False'''

#Kreiere ein eigenes Event, welches jede Sekunde ausgeführt wird -> um den Block nach unten zu bewegen
BLOCKFALL = pygame.USEREVENT + 1
pygame.time.set_timer(BLOCKFALL, timer)

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
    for duo in duo_group:
        for event in events:
            if duo.is_falling():
                if event.type == KEYDOWN:
                    if event.key == K_RIGHT:
                        if duo.is_right_free():
                            duo.move_right()
                    if event.key == K_LEFT:
                        if duo.is_left_free():
                            duo.move_left()
                    if event.key == K_UP:
                        duo.rotate()
                if event.type == BLOCKFALL:
                        duo.move_down()
        if duo.is_falling():
            has_active_block = True

    #mergen(Block.rect.x, Block.rect.y, Block.number)
    #fill(Block.rect.x, Block.rect.y)

    if not has_active_block:
        for field in board[0]:
            if field == False:
                duo = Duo()
                duo_group.append(duo)
            else:
                running = False
                print('Du hast leider verloren')
    #Hintergrund weiss machen
    screen.fill((255, 255, 255))

    #Zeichne ein Rechteck oben in die Mitte
    #pygame.draw.rect(screen, (255, 0, 0), [rectangle_x, rectangle_y, BLOCK_WIDTH, BLOCK_HEIGHT])

    for duo in duo_group:
        for block in duo:
            screen.blit(block.image, block.rect)
            if board[block.list_y][block.list_x] == False:
                board[block.list_y][block.list_x] = block
                '''for row in board:
                    print(row)
                print(' ')'''

    #block_group.draw(screen)
    #Flip the display - aktualisieren
    pygame.display.flip()

#ganz am Ende
pygame.quit()
