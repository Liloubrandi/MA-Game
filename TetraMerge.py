# Importiere pygame library
import pygame

#importiere random library
import random

# Importiere pygame.locals, um einen einfacheren Zugang zu Tasten zu haben
from pygame.locals import (
    K_UP, #Pfeiltaste nach oben
    K_LEFT, #Pfeiltaste links
    K_RIGHT, #Pfeiltaste rechts
    K_ESCAPE, #Escapetaste
    KEYDOWN, #eine Taste drücken
    QUIT, #Fenster schliessen
)

#initialisiere
pygame.init()
pygame.font.init()

#Parameter für Bildschirm und Block
BLOCKS_VERTICAL = 14
BLOCKS_HORIZONTAL = 10
DISPLAY_WIDTH = 500
DISPLAY_LENGTH = 700
BLOCK_WIDTH = DISPLAY_WIDTH//BLOCKS_HORIZONTAL
BLOCK_HEIGHT = DISPLAY_LENGTH//BLOCKS_VERTICAL

#Erstelle das Spielfenster
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

#Klasse Board: fasst alle Duos (und damit alle Blöcke) zusammen
class Board():
    def __init__(self):
        #erstellt eine Liste für die Duos
        self.duos = []

    def register(self, duo):
        #speichert das Duo in die erstellte Liste
        self.duos.append(duo)
    
    @property #macht, dass die Methode eine Eigenschaft ist, welche ohne Klammern (block_list anstatt block_list()) angesprochen werden kann
    def block_list(self):
        #erstellt eine Liste für alle Blöcke
        block_list = []
        for duo in self.duos: #iteriert durch jedes Duo 
            for block in duo.blocks: #iteriert durch jeden Block des Duos 
                block_list.append(block) #fügt den Block der Liste an
        return block_list
    
    def reset_blocks(self):
        #Setzt das visited Attribut des Blocks wieder auf False 
        #(so kann dieser wieder überprüft werden, bei merge_list)
        for block in self.block_list: #iteriert durch jeden Block
            block.reset() 

    def get_block(self, x, y):
        for block in self.block_list: #iteriert durch jeden Block
            #vergleicht die Position des Blocks mit der übergebenen Position 
            #und gibt den Block zurück, falls einer gefunden wird
            if block.list_x == x and block.list_y == y: 
                return block
    
    @property #macht, dass die Methode eine Eigenschaft ist, welche ohne Klammern angesprochen werden kann
    def falling_duos(self):
        #erstellt eine Liste für die fallenden Duos
        falling_duos = []
        for duo in self.duos: #iteriert durch jedes Duo
            #überprüft, ob das Duo noch fällt und fügt es der Liste hinzu, falls es fällt
            if duo.is_falling(): 
                falling_duos.append(duo) 
        return falling_duos
    
    def merge_list(self, mergelist, block, number):
        #überprüft alle Nachbarsfelder des übergebenen Blocks
        #speichert die Blöcke in die übergebene mergelist, falls diese die gleiche Würfelzahl aufweisen wie der übergebene Block
        if block is not None and block.visited == False: #Ist überhaupt ein Block an dieser Stelle? Wurde dieser bereits überprüft?
        #Rahmenbedingungen (befindet sich der Algorithmus ausserhalb des Spielfeldes?)
            if block.list_x < 0 or block.list_x > BLOCKS_HORIZONTAL - 1:
                return mergelist
            if block.list_y < 0 or block.list_y > BLOCKS_VERTICAL - 1:
                return mergelist
        #Feld überprüfen
            if block.number == number: #Hat der überprüfte Block dieselbe Würfelzahl wie der übegebene?
                mergelist.append(block) #Füge den Block der Liste hinzu
                block.visited = True #Markiere den Block als "besucht"
                self.merge_list(mergelist, block.board.get_block(block.list_x + 1, block.list_y), number) #überprüft Block rechts davon
                self.merge_list(mergelist, block.board.get_block(block.list_x - 1, block.list_y), number) #überprüft Block links davon
                self.merge_list(mergelist, block.board.get_block(block.list_x, block.list_y + 1), number) #überprüft Block unterhalb
                self.merge_list(mergelist, block.board.get_block(block.list_x, block.list_y - 1), number) #überprüft Block oberhalb
        return mergelist #gibt Liste mit allen gleichen Nachbaren zurück

    def lost(self):
        #iteriert durch alle Duos und deren Blöcke und überprüft, ob die am oberen Spielfeldrand ankommen
        for duo in self.duos:
            for block in duo.blocks:
                if block.list_y == 0:
                    return True

#Klasse Duo: verbindet zwei Blöcke und regelt die Bewegungen des Spielsteins
class Duo(pygame.sprite.Group):
    def __init__(self, board):
        super().__init__()
        #Duo kennt nun das Board
        self.board = board
        #erstellt seine beiden Blöcke
        block = Block(BLOCK_WIDTH, BLOCK_HEIGHT, rectangle_x, 0, board, self)
        block_2 = Block(BLOCK_WIDTH, BLOCK_HEIGHT, rectangle2_x, 0, board, self)
        #fügt die erstellten Blöcke sich selbst hinzu
        self.add(block) 
        self.add(block_2)
        #bestimmt die aktuelle Ausrichtung (Startausrichtung)
        self.rotation = 'horizontal_right'
        #speicher sich in der Liste des Boards
        self.board.register(self)
    
    @property #macht, dass die Methode eine Eigenschaft ist, welche ohne Klammern angesprochen werden kann
    def blocks(self):
        #gibt die im Duo enthaltenen Blöcke zurück
        return self.sprites()
    
    def remove_block(self, block):
        #entfernt den übergebenen Block (beispielsweise nach dem Mergen)
        self.remove(block)

    def move_down(self):
        #iteriert durch jeden seiner Blöcke und verschiebt sie nach unten
        for block in self.blocks:
            block.move('down')

    def move_left(self):
        #iteriert durch jeden seiner Blöcke und verschiebt sie nach links
        for block in self.blocks:
            block.move('left')

    def move_right(self):
        #iteriert durch jeden seiner Blöcke und verschiebt sie nach rechts
        for block in self.blocks:
            block.move('right')

    @property #macht, dass die Methode eine Eigenschaft ist, welche ohne Klammern angesprochen werden kann
    def lowest_block(self):
        #Gibt den tieferstehenden Block des Duos zurück 
        #Voraussetzung: Es hat genau zwei Blöcke
        #Wenn beide die gleichen y-Koordinaten haben -> waagerecht
        #Wenn beide andere y-Koordinaten haben -> senkrecht
        if len(self.blocks) == 2: #Sind zwei Blöcke vorhanden?
            #Vergleich der y-Koordinaten
            if self.blocks[0].rect.y == self.blocks[1].rect.y: 
                return self.blocks
            else:
                if self.blocks[0].rect.y > self.blocks[1].rect.y:
                    return [self.blocks[0]] 
                else:
                    return [self.blocks[1]]
        else:
            return self.blocks
            
    @property #macht, dass die Methode eine Eigenschaft ist, welche ohne Klammern angesprochen werden kann
    def highest_block(self):
        #Gibt den höherstehenden Block des Duos zurück
        #Voraussetzung: Es hat genau zwei Blöcke
        #Wenn beide die gleichen y-Koordinaten haben -> waagerecht
        #Wenn beide andere y-Koordinaten haben -> senkrecht
        if len(self.blocks) == 2: #Sind zwei Blöcke vorhanden?
            #Vergleich der y-Koordinaten
            if self.blocks[0].rect.y == self.blocks[1].rect.y: 
                return self.blocks
            else:
                if self.blocks[0].rect.y > self.blocks[1].rect.y:
                    return [self.blocks[1]]
                else:
                    return [self.blocks[1]]
        else:
            return self.blocks

    @property #macht, dass die Methode eine Eigenschaft ist, welche ohne Klammern angesprochen werden kann
    def right_block(self):
        #Gibt den Block des Duos zurück, der weiter rechts ist
        #Voraussetzung: Es hat genau zwei Blöcke
        #Wenn beide die gleichen x-Koordinaten haben -> senkrecht
        #Wenn beide andere x-Koordinaten haben -> waagerecht
        if len(self.blocks) == 2: #Sind zwei Blöcke vorhanden?
            #Vergleich der x-Koordinaten
            if self.blocks[0].rect.x == self.blocks[1].rect.x:
                return self.blocks
            else:
                if self.blocks[0].rect.x > self.blocks[1].rect.x:
                    return [self.blocks[0]]
                else:
                    return [self.blocks[1]]
        else:
            return self.blocks
    
    @property #macht, dass die Methode eine Eigenschaft ist, welche ohne Klammern angesprochen werden kann
    def left_block(self):
        #Gibt den Block des Duos zurück, der weiter links ist
        #Voraussetzung: Es hat genau zwei Blöcke
        #Wenn beide die gleichen x-Koordinaten haben -> senkrecht
        #Wenn beide andere x-Koordinaten haben -> waagerecht
        if len(self.blocks) == 2: #Sind zwei Blöcke vorhanden?
            #Vergleich der x-Koordinaten
            if self.blocks[0].rect.x == self.blocks[1].rect.x:
                return self.blocks
            else:
                if self.blocks[0].rect.x > self.blocks[1].rect.x:
                    return [self.blocks[1]]
                else:
                    return [self.blocks[0]]
        else:
            return self.blocks

    def is_falling(self):
        #Diese Funktion gibt nur dann True zurück, wenn keiner der Blöcke des Duos and der Bewegung gehindert wird
        if len(self.blocks) == 0: #bricht ab, falls keine Blöcke mehr im Duo sind
            return False
        is_falling = True
        #iteriert durch den/die tiefsten Block/Blöcke
        for block in self.lowest_block:
            #schaut, ob der Block noch fallen kann/darf
            if is_falling and not block.falling():
                is_falling = False
        return is_falling
        
    def is_right_free(self):
        #Diese Funktion gibt nur dann True zurück, wenn keiner der Blöcke des Duos and der Bewegung gehindert wird
        is_right_free = True
        #iteriert durch den/die Block/Blöcke, der/die am weitesten rechts ist
        for block in self.right_block:
            #Schaut, ob der Block nach rechts verschoben werden kann/darf
            if is_right_free and not block.right_free():
                    is_right_free = False
        return is_right_free

    def is_left_free(self):
        #Diese Funktion gibt nur dann True zurück, wenn keiner der Blöcke des Duos and der Bewegung gehindert wird
        is_left_free = True 
        #iteriert durch den/die Block/Blöcke, der/die am weitesten links ist
        for block in self.left_block:
            #Schaut, ob der Block nach links verschoben werden kann/darf
            if is_left_free and not block.left_free():
                    is_left_free = False
        return is_left_free
                
    def rotate(self):
        if self.rotation == 'horizontal_right': #aktuelle Ausrichtung?
            #schaut den Block an, der weiter rechts liegt, und verändert seine Koordinaten
            for block in self.right_block:
                #der rechte Block wird unter den anderen gesetzt
                block.rect.y += BLOCK_HEIGHT
                block.rect.x -= BLOCK_WIDTH
            self.rotation = 'vertical_down' #definiere neue aktuelle Ausichtung
        elif self.rotation == 'vertical_down': #aktuelle Ausrichtung?
            #Kann der Block an die gewünschte Stelle verschoben werden?
            if self.is_left_free():
                #schaut den Block an, der weiter unten liegt, und verändert seine Koordinaten
                for block in self.lowest_block:
                    #der tiefere Block wird links neben den anderen gesetzt
                    block.rect.y -= BLOCK_HEIGHT
                    block.rect.x -= BLOCK_WIDTH
                self.rotation = 'horizontal_left' #definiere neue aktuelle Ausichtung
        elif self.rotation == 'horizontal_left': #aktuelle Ausrichtung?
            #schaut den Block an, der weiter links liegt, und verändert seine Koordinaten
            for block in self.left_block:
                #der linke Block wird über den anderen gesetzt
                block.rect.y -= BLOCK_HEIGHT
                block.rect.x += BLOCK_WIDTH
            self.rotation = 'vertical_up' #definiere neue aktuelle Ausichtung
        elif self.rotation == 'vertical_up': #aktuelle Ausrichtung?
            #Kann der Block an die gewünschte Stelle verschoben werden?
            if self.is_right_free():
                #schaut den Block an, der weiter oben liegt, und verändert seine Koordinaten
                for block in self.highest_block:
                    #der höhere Block wird rechts neben den anderen gesetzt
                    block.rect.y += BLOCK_HEIGHT
                    block.rect.x += BLOCK_WIDTH
                self.rotation = 'horizontal_right' #definiere neue aktuelle Ausichtung

#Klasse Block: erstellt die kleinste Einheit des Spiels - den Block und verwaltet dessen Position
class Block(pygame.sprite.Sprite):
    def __init__(self, width, height, pos_x, pos_y, board, duo):
        super().__init__()
        #Block kenn nun das Board
        self.board = board
        self.visited = False #sagt aus, ob der Block besucht wurde
        self.number = random.randint(1, 6)
        #Ladet anhand der zufällig gewählten Nummer das korrekte Bild
        self.image = pygame.image.load(self.dice)
        #Passt die Grösse des Bildes der Grösse des Blocks an
        self.smaller_image = pygame.transform.scale(self.image, (width, height))
        #self.image = pygame.Surface((width, height))
        #self.image.fill(self.color) 
        self.rect = self.image.get_rect() #erstellt aus dme Bild ein Rechteck
        self.rect.x = pos_x #x-Koordinate
        self.rect.y = pos_y #y-Koordinate
        #Block kenn nun das Duo
        self.duo = duo
    
    @property #macht, dass die Methode eine Eigenschaft ist, welche ohne Klammern angesprochen werden kann
    def dice(self):
        #Schaut, welche der sechs Zahlen ausgewählt wurde und gibt das entsprechende Würfelbild zurück
        if self.number == 1:
            return "TetraMerge-wuerfel_1.png"
        if self.number == 2:
            return "TetraMerge-wuerfel_2.png"
        if self.number == 3:
            return "TetraMerge-wuerfel_3.png"
        if self.number == 4:
            return "TetraMerge-wuerfel_4.png"
        if self.number == 5:
            return "TetraMerge-wuerfel_5.png"
        if self.number == 6:
            return "TetraMerge-wuerfel_6.png"
        
    def remove(self):
        #entfernt sich selbst von Duo (beispielsweise nach dem Mergen)
        self.duo.remove_block(self)

    def reset(self):
        #nach dem Mergen
        #setzt das Attribut visited auf False -> der Block gilt damit wieder als nicht besucht 
        self.visited = False

    def increase_number(self, ):
        #nach dem Mergen
        #erhöht die eigene Würfelzahl
        self.number = self.number + 1
        #updated das Bild sowie dessen Grösse anhand der neuen Würfelzahl
        self.image = pygame.image.load(self.dice)
        self.smaller_image = pygame.transform.scale(self.image, (BLOCK_WIDTH, BLOCK_HEIGHT))

    def move(self, direction):
        #verändert die Koordinaten des Blocks wie gewünscht
        if direction == 'down':
            self.rect.y = self.rect.y + BLOCK_HEIGHT #erhöht y-Koordinate - Block tiefer unten
        if direction == 'right':
            self.rect.x = self.rect.x + BLOCK_WIDTH #erhöht x-Koordinate - Block weiter rechts
        if direction == 'left':
            self.rect.x = self.rect.x - BLOCK_WIDTH #verringert x-Koordinate - Block weiter links

    def falling(self):
        #überprüft ob der Block fallen kann/darf
        if self.list_y < BLOCKS_VERTICAL - 1: #ist der Block noch nicht am Ende des Spielfelds?
            if self.board.get_block(self.list_x, self.list_y + 1) is None: #Gibt es einen Block, der unterhalb dieses Blocks liegt?
                return True
        return False
    
    def right_free(self):
        #überprüft ob der Block nach rechts verschoben werden kann/darf
        if self.list_x < BLOCKS_HORIZONTAL - 1: #ist der Block noch nicht am rechten Rand des Spielfelds?
            if self.board.get_block(self.list_x + 1, self.list_y) is None: #Gibt es einen Block, der rechts neben diesem Block liegt?
                return True
        return False
    
    def left_free(self):
        #überprüft ob der Block nach links verschoben werden kann/darf
        if self.list_x > 0: #ist der Block noch nicht am linken Rand des Spielfelds?
            if self.board.get_block(self.list_x - 1, self.list_y) is None: #Gibt es einen Block, der links neben diesem Block liegt?
                return True
        return False
    
    @property #macht, dass die Methode eine Eigenschaft ist, welche ohne Klammern angesprochen werden kann
    def list_x(self):
        #rechnet die waagerechte Position des Blocks aus und gibt sie zurück
        return self.rect.x // BLOCK_WIDTH
    
    @property #macht, dass die Methode eine Eigenschaft ist, welche ohne Klammern angesprochen werden kann
    def list_y(self):
        #rechnet die waagerechte Position des Blocks aus und gibt sie zurück
        return self.rect.y // BLOCK_HEIGHT     

#Kreiere ein eigenes Event, welches jede halbe Sekunde ausgeführt wird -> um den Block nach unten zu bewegen
BLOCKFALL = pygame.USEREVENT + 1
pygame.time.set_timer(BLOCKFALL, timer)

#erzeuge Spielfeld
board = Board()
#erzeuge Duo
duo = Duo(board)

#While-Schlaufe - machen bis running = False
while running:
    #fragt alle Events ab und speichert sie in events
    events = pygame.event.get()
    #iteriere durch jedes Event
    for event in events:
        #Hat der Spieler die Escapetaste gedrückt oder das Fenster geschlossen? 
        if event.type == QUIT: #wurde das Fenster geschlossen?
            running = False
        if event.type == KEYDOWN: #wurde eine Taste gedrückt?
            if event.key == K_ESCAPE:
                running = False

    has_active_block = False
    falling_duos = board.falling_duos #speichert alle fallenden Duos in falling _duos
    for duo in board.duos:
        #iteriere für jedes Duo durch jedes Event
        for event in events:
            if duo.is_falling(): #folgende Zeilen dürfen nur für fallende Blöcke ausgeführt werden -> deshalb hier die Überprüfung
                if event.type == KEYDOWN: #Wurde eine Taste gedrückt?
                    if event.key == K_RIGHT:
                        #überprüfe, ob rechts noch Platz wäre -> Falls ja, verschiebe das Duo nach rechts
                        if duo.is_right_free():
                            duo.move_right()
                    if event.key == K_LEFT:
                        #überprüfe, ob links noch Platz wäre -> Falls ja, verschiebe das Duo nach links
                        if duo.is_left_free():
                            duo.move_left()
                    if event.key == K_UP:
                        duo.rotate() #rotiert den Block
                if event.type == BLOCKFALL: #wurde das Userevent BLOCKFALL aufgerufen? -> Falls ja, verschiebe das Duo nach unten
                    duo.move_down()
        #überprüfe, ob dieses Duo fällt, dann wäre has_active_block neu auf True
        if duo.is_falling():
            has_active_block = True

    #Diesen Codeblock führt es nur aus, wenn kein Block mehr fällt
    if not has_active_block:
        #überprüft, ob das Spiel zu ende ist
        if board.lost(): 
            running = False 
            print('Du hast leider verloren')
        else:
            #Setze alle Blöcke aus nicht besucht
            board.reset_blocks()
            #iteriere durch jedes fallende Duo
            for falling_duo in falling_duos: 
                if falling_duo is not None:
                    #iteriere durch jeden Block des fallenden Duos
                    for block in falling_duo:
                        if block is not None:
                            #bei aktuellem Block schauen, ob er gleiche Nachbaren hat
                            #liste mit allen betroffenen Blöcken zurückgeben (wenn Liste länger als 3, dann mergen)
                            blocks_to_merge = board.merge_list([], block, block.number)
                            #überprüfe, ob die Liste mehr als ein Objekt besitzt
                            if len(blocks_to_merge) > 0:
                                current_block = blocks_to_merge.pop(0) #nimmt das erste Element aus der Liste und speichert es als aktuellen Block
                                #überprüft, ob danach noch mindestens zwei Bläcke in der Liste vorhanden sind
                                if len(blocks_to_merge) > 1:
                                    #Löscht jeden Block, der in der Liste noch vorhanden ist und erhöht dabei den Score
                                    for block in blocks_to_merge:
                                        block.remove()
                                        score = score + score_increasement
                                    #Wenn der aktuelle Block eine 6 ist, wird dieser ebenfalls gelöscht
                                    if current_block.number == 6:
                                        current_block.remove()
                                    else: #ansonsten wird die Würfelzahl des aktuellen Blocks erhöht
                                        current_block.increase_number()
                                    has_active_block = True
    if not has_active_block:
        #erstellt ein neues Duo
        duo = Duo(board)
        score = score + score_increasement

    #Hintergrund weiss füllen
    screen.fill((255, 255, 255))

    #iteriert durch jedes Duo
    for duo in board.duos:
        #zeichnet jedes Duo auf das Spielfeld
        duo.draw(screen)

    #Ebenfalls möglich wäre:
    #for duo in board.duos:
        #for block in duo:
            #screen.blit(block.smaller_image, block.rect)

    #erstellt ein Bild des Scores, welches mit blit() auf den Bildschirm gedruckt werden kann
    show_score = font.render(f'Score: {score}', True, (0, 0, 0)) #(Text, abgerundete Ecken?, Farbe)
    #Mit Blit() den Score auf das Spielfeld schreiben
    screen.blit(show_score, (10, 10))

    #Flippe das Display - aktualisieren
    pygame.display.flip()


#ganz am Ende
pygame.quit()
