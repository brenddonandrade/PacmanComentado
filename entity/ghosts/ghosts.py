import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity.entity import Entity
from entity.ghosts.modes import ModeController
from sprites.sprites import GhostSprites

class Ghost(Entity):
    def __init__(self, node, pacman=None, blinky=None):
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200
        self.goal = Vector2() #Destino deles é um vetor
        self.directionMethod = self.goalDirection #Os fantasmas terão destinos
        self.pacman = pacman #Instancia objeto Pacman
        self.mode = ModeController(self) #Instancia o modo de controler
        self.blinky = blinky #Instancia o Blinky
        self.homeNode = node #Define o nodo de origem

    def update(self, dt):
        self.sprites.update(dt) #Atualiza os sprites
        self.mode.update(dt) #Atualiza os modos
        if self.mode.current is SCATTER: 
            self.scatter() #Define o destino
        elif self.mode.current is CHASE:
            self.chase() #Define o destino
        Entity.update(self, dt) #Chama o update geral

    def scatter(self):
        self.goal = Vector2() #Define uma posição (x,y) como destino

    def chase(self):
        self.goal = self.pacman.position #Define o Pacman como destino

    def startFreight(self):
        self.mode.setFreightMode() #Inicializa o modo Freight
        if self.mode.current == FREIGHT:
            self.setSpeed(50) #Diminui a velocidade dos fantasmas
            self.directionMethod = self.randomDirection #Agora eles se movimentam de maneira aleatória

    def normalMode(self): #Volta tudo ao normal!
        self.setSpeed(100)
        self.directionMethod = self.goalDirection #Reseta o destino
        self.homeNode.denyAccess(DOWN, self) #Nega o acesso à casa dos fantasmas

    def spawn(self):
        self.goal = self.spawnNode.position #Define o destino para a posição de origem

    def setSpawnNode(self, node):
        self.spawnNode = node #Define a posição de origem

    def startSpawn(self):
        self.mode.setSpawnMode() #Inicializa o modo Spawn
        if self.mode.current == SPAWN:
            self.setSpeed(150) #Velocidade aumenta
            self.directionMethod = self.goalDirection #Direção agora é um destino
            self.spawn() #Define o destino como a origem

    def reset(self): #Reseta o fantasma
        Entity.reset(self)
        self.points = 200
        self.directionMethod = self.goalDirection

class Blinky(Ghost): #Blinky é, praticamente, o fantasma genérico do código
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky) 
        self.name = BLINKY
        self.color = RED
        self.sprites = GhostSprites(self) #Instancia o sprite

class Pinky(Ghost): #Classe do Pinky
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = PINKY
        self.color = PINK
        self.sprites = GhostSprites(self)

    def scatter(self):
        self.goal = Vector2(TILEWIDTH*NCOLS, 0) #Canto superior esquerdo

    def chase(self):
        self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4 #4 posições na frente do Pacman

class Inky(Ghost): #Classe do Inky
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = INKY
        self.color = TEAL
        self.sprites = GhostSprites(self)

    def scatter(self):
        self.goal = Vector2(TILEWIDTH*NCOLS, TILEHEIGHT*NROWS) #Canto superior direito

    def chase(self):
        vec1 = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 2 #Posição de dois blocos na frente do Pacman
        vec2 = (vec1 - self.blinky.position) * 2 #Vetor 1 subtraido pela posição do Blinky e multiplicado por 2
        self.goal = self.blinky.position + vec2 #Destino final

class Clyde(Ghost): #Classe do Clyde
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = CLYDE
        self.color = ORANGE
        self.sprites = GhostSprites(self)

    def scatter(self):
        self.goal = Vector2(0, TILEHEIGHT*NROWS) #Canto inferior esquerdo

    def chase(self):
        d = self.pacman.position - self.position
        ds = d.magnitudeSquared() #Teste de distância
        if ds <= (TILEWIDTH * 8)**2:
            self.scatter()
        else:
            self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4 #Age como o Pinky

class GhostGroup(object): #Junta todos os fantasmas em um só objeto
    def __init__(self, node, pacman):
        self.blinky = Blinky(node, pacman) #Objeto Blinky
        self.pinky = Pinky(node, pacman) #Objeto Pinky
        self.inky = Inky(node, pacman, self.blinky) #Objeto Inky
        self.clyde = Clyde(node, pacman) #Objeto Clyde
        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde] #Lista com os fantasmas

    def __iter__(self): #Iterar sobre a lista de fantasmas
        return iter(self.ghosts) 

    def update(self, dt): #Utilizar o método update na lista
        for ghost in self:
            ghost.update(dt)

    def startFreight(self): #Aplicar o modo Freight na lista
        for ghost in self:
            ghost.startFreight()
        self.resetPoints()

    def setSpawnNode(self, node): #Aplicar o modo Spawn na lista
        for ghost in self:
            ghost.setSpawnNode(node)

    def updatePoints(self): #Incrementar os pontos dos fantasmas
        for ghost in self:
            ghost.points *= 2

    def resetPoints(self): #Resetar os pontos dos fantasmas
        for ghost in self:
            ghost.points = 200

    def reset(self): #Resetar os fantasmas
        for ghost in self:
            ghost.reset()

    def hide(self): #Esconder os fantasmas
        for ghost in self:
            ghost.visible = False

    def show(self): #Mostrar os fantasmas
        for ghost in self:
            ghost.visible = True

    def render(self, screen): #Desenhar os fantasmas
        for ghost in self:
            ghost.render(screen)
