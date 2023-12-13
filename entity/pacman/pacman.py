import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity.entity import Entity
from sprites.sprites import PacmanSprites

class Pacman(Entity):
    def __init__(self, node):
        Entity.__init__(self, node) 
        # identificacao do pacman
        self.name = PACMAN
        # defini a cor a ser gerada na tela
        self.color = YELLOW
        self.direction = LEFT #Começa movimentando para a Esquerda
        self.setBetweenNodes(LEFT) 
        self.alive = True
        self.sprites = PacmanSprites(self)

    def update(self, dt):
        self.sprites.update(dt)
        self.position += self.directions[self.direction]*self.speed*dt #Movimento
        direction = self.getValidKey() #Coleta a tecla apertada no teclado
        if self.overshotTarget():
            self.node = self.target #Troca o nódo antigo para o nódo da posição destino
            # implementa o portal no jogo
            if self.node.neighbors[PORTAL] is not None:
                # implementa os participantes dos portais como vizinhos
                self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction) #Atualiza o destino
            if self.target is not self.node: #Se o destino não é a posição originária

                self.direction = direction #Movimenta para o destino
            else:
                self.target = self.getNewTarget(self.direction)

            if self.target is self.node:
                self.direction = STOP
            self.setPosition() #Atualiza o nódo atual
        else: 
            if self.oppositeDirection(direction):
                self.reverseDirection()

    def getValidKey(self): #Este método irá coletar a tecla que foi apertada no teclado
        # metodo do pygame que coleta a tecla apertada
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT
        return STOP #Se não houve entrada, então parar o Pacman

    # verifica se o pacman está comendo (colidindo) pellets
    def eatPellets(self, pelletList):
        for pellet in pelletList:
            if self.collideCheck(pellet):
                return pellet
        return None

    # decta se o Ghost capiturou o pacman
    def collideGhost(self, ghost):
        return self.collideCheck(ghost)

    # checa se há colisão entre as entidades
    def collideCheck(self, other):
        d = self.position - other.position
        dSquared = d.magnitudeSquared()
        rSquared = (self.collideRadius + other.collideRadius)**2
        if dSquared <= rSquared:
            return True
        return False

    # reseta o jogo
    def reset(self):
        Entity.reset(self)
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.image = self.sprites.getStartImage()
        self.sprites.reset()

    # verifica se o pacman morreu
    def die(self):
        self.alive = False
        self.direction = STOP
