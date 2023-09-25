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
pygame.font.init()

YELLOW = (255, 255, 0)
RED = (204, 0, 0)
GREEN = (0, 204, 0)
BLUE = (0, 0, 204)
PURPLE = (102, 0, 204)
PINK = (204, 0, 204)

#Parameter für Bildschirm und Block und Bildschirmerstellung
BLOCKS_VERTICAL = 14
BLOCKS_HORIZONTAL = 10
DISPLAY_WIDTH = 500
DISPLAY_LENGTH = 700
BLOCK_WIDTH = DISPLAY_WIDTH//BLOCKS_HORIZONTAL
BLOCK_HEIGHT = DISPLAY_LENGTH//BLOCKS_VERTICAL
screen = pygame.display.set_mode([DISPLAY_WIDTH, DISPLAY_LENGTH])

#Variablen:
running = True
rectangle_y = 0
rectangle_x = 0 + 4 * BLOCK_WIDTH
rectangle2_x = 0 + 5 * BLOCK_WIDTH
timer = 500
score = 0
score_increasement = 10
font = pygame.font.Font(None, 50)

class Board():
    def __init__(self):
        self.duos = []

    def register(self, duo):
        self.duos.append(duo)
        #raise exception, wenn ausserhalb oder Position schon besetzt
    
    @property
    def block_list(self):
        block_list = []
        for duo in self.duos:
            for block in duo.blocks:
                block_list.append(block)
        return block_list
    
    def reset_blocks(self):
        for block in self.block_list:
            block.reset()

    def get_block(self, x, y):
        for block in self.block_list:
            if block.list_x == x and block.list_y == y:
                return block
    
    @property
    def falling_duos(self):
        falling_duos = []
        for duo in self.duos:
            if duo.is_falling():
                falling_duos.append(duo)
        return falling_duos

    def lost(self):
        for duo in self.duos:
            for block in duo.blocks:
                if block.list_y == 0:
                    return True

class Duo(pygame.sprite.Group):
    def __init__(self, board):
        super().__init__()
        self.board : Board = board
        block = Block(BLOCK_WIDTH, BLOCK_HEIGHT, rectangle_x, board, self)
        block_2 = Block(BLOCK_WIDTH, BLOCK_HEIGHT, rectangle2_x, board, self)
        self.add(block)
        self.add(block_2)
        self.rotation = 'horizontal_right'
        self.board.register(self)
    
    @property
    def blocks(self):
        return self.sprites()
    
    def remove_block(self, block):
        self.remove(block)

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
        if len(self.blocks) == 0:
            return False
        is_falling = True
        for block in self.lowest_block:
            if is_falling and not block.falling():
                is_falling = False
        return is_falling
        
    def is_right_free(self):
        is_right_free = True
        for block in self.right_block:
            if is_right_free and not block.right_free():
                    is_right_free = False
        return is_right_free

    def is_left_free(self):
        is_left_free = True 
        for block in self.left_block:
            if is_left_free and not block.left_free():
                    is_left_free = False
        return is_left_free
                
    def rotate(self):
        if self.rotation == 'horizontal_right':
            for block in self.right_block:
                #board[block.list_y][block.list_x] = False
                block.rect.y += BLOCK_HEIGHT
                block.rect.x -= BLOCK_WIDTH
            self.rotation = 'vertical_down'
        elif self.rotation == 'vertical_down':
            if self.is_left_free():
                for block in self.lowest_block:
                    #board[block.list_y][block.list_x] = False
                    block.rect.y -= BLOCK_HEIGHT
                    block.rect.x -= BLOCK_WIDTH
                self.rotation = 'horizontal_left'
        elif self.rotation == 'horizontal_left':
            for block in self.left_block:
                #board[block.list_y][block.list_x] = False
                block.rect.y -= BLOCK_HEIGHT
                block.rect.x += BLOCK_WIDTH
            self.rotation = 'vertical_up'
        elif self.rotation == 'vertical_up':
            if self.is_right_free():
                for block in self.highest_block:
                    #board[block.list_y][block.list_x] = False
                    block.rect.y += BLOCK_HEIGHT
                    block.rect.x += BLOCK_WIDTH
                self.rotation = 'horizontal_right'

class Block(pygame.sprite.Sprite):
    def __init__(self, width, height, pos_x, board, duo):
        super().__init__()
        self.board = board
        self.visited = False
        self.number = random.randint(1, 6)
        self.image = pygame.Surface((width, height))
        self.image.fill(self.color) 
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = 0
        self.duo = duo
    
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
        
    def remove(self):
        self.duo.remove_block(self)

    def reset(self):
        self.visited = False

    def move(self, direction):
        if direction == 'down':
            #board[self.list_y][self.list_x] = False
            self.rect.y = self.rect.y + BLOCK_HEIGHT
        if direction == 'right':
            #board[self.list_y][self.list_x] = False
            self.rect.x = self.rect.x + BLOCK_WIDTH
        if direction == 'left':
            #board[self.list_y][self.list_x] = False
            self.rect.x = self.rect.x - BLOCK_WIDTH

    def falling(self):
        if self.list_y < BLOCKS_VERTICAL - 1:
            if self.board.get_block(self.list_x, self.list_y + 1) is None:
                return True
        return False
    
    def right_free(self):
        if self.list_x < BLOCKS_HORIZONTAL - 1:
            if self.board.get_block(self.list_x + 1, self.list_y) is None:
                return True
        return False
    
    def left_free(self):
        if self.list_x > 0:
            if self.board.get_block(self.list_x - 1, self.list_y) is None:
                return True
        return False
    
    @property #macht, dass die Methode eine Eigenschaft ist, welche ohne Klammern (list_x anstatt list_x()) angesprochen werden kann
    def list_x(self):
        return self.rect.x // BLOCK_WIDTH
    
    @property
    def list_y(self):
        return self.rect.y // BLOCK_HEIGHT     

def merge_list(mergelist, block, number):
        if block is not None:
        #Rahmenbedingungen
            if block.list_x < 0 or block.list_x > BLOCKS_HORIZONTAL - 1:
                return mergelist
            if block.list_y < 0 or block.list_y > BLOCKS_VERTICAL - 1:
                return mergelist
        #Feld überprüfen
            if block.number == number:
                mergelist.append(block) 
                merge_list(mergelist, block.board.get_block(block.list_x + 1, block.list_y), number) #rechts
                merge_list(mergelist, block.board.get_block(block.list_x - 1, block.list_y ), number) #links
                merge_list(mergelist, block.board.get_block(block.list_x, block.list_y + 1), number) #unten
                merge_list(mergelist, block.board.get_block(block.list_x, block.list_y - 1), number) #oben
        return mergelist

'''def fill(block, board):
    block.number = block.number + 1
    if block.number == 6:
        block.remove()
    for y in range(BLOCKS_VERTICAL - 1, 0, -1):
        for x in range(BLOCKS_HORIZONTAL - 1):
            if board.get_block(x, y) is None:
                row_index = y
                while row_index > 0 and board.get_block(x, row_index) is None:
                    row_index = row_index + 1
                board.get_block(x, row_index).rect.y = y * BLOCK_HEIGHT'''
    
        
'''def fill(x, y):
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

#erzeuge Spielfeld
board = Board()
#block = Block(BLOCK_WIDTH, BLOCK_HEIGHT, rectangle_x)
#block_2 = Block(BLOCK_WIDTH, BLOCK_HEIGHT, rectangle2_x)
duo = Duo(board)

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
    for duo in board.duos:
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
        if board.lost():
            running = False 
            print('Du hast leider verloren')
        else:
            #bei aktuellem Block schauen, ob er gleiche Nachbaren hat
            #liste mit allen betroffenen Blöcken zurückgeben (wenn liste länger als 3, dann mergen)
            for falling_duo in board.falling_duos:
                for block in falling_duo:
                    board.reset_blocks()
                    blocks_to_merge = merge_list([], block, block.number)
                    if len(blocks_to_merge) > 0:
                        current_block = blocks_to_merge.pop(0)
                    if len(blocks_to_merge) > 1:
                        for block in blocks_to_merge:
                            block.remove()
                        current_block.number = current_block.number + 1
            duo = Duo(board)
            score = score + score_increasement
    
        '''for field in board[0]:
            if field == False:
                duo = Duo()
                duo_group.append(duo)
            else:
                running = False
                print('Du hast leider verloren')'''
    #Hintergrund weiss machen
    screen.fill((255, 255, 255))

    #Zeichne ein Rechteck oben in die Mitte
    #pygame.draw.rect(screen, (255, 0, 0), [rectangle_x, rectangle_y, BLOCK_WIDTH, BLOCK_HEIGHT])

    for duo in board.duos:
        for block in duo:
            screen.blit(block.image, block.rect)
            #if board[block.list_y][block.list_x] == False:
            #board[block.list_y][block.list_x] = block 
            '''for row in board:
                    print(row)
                print(' ')'''

    #Blit the score on the screen
    show_score = font.render(f'Score: {score}', True, (0, 0, 0))
    screen.blit(show_score, (10, 10))

    #block_group.draw(screen)
    #Flip the display - aktualisieren
    pygame.display.flip()

#ganz am Ende
pygame.quit()
