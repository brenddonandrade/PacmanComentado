import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from random import randint

class Entity(object):
    def __init__(self, node):
        self.name = None
        self.directions = {UP:Vector2(0, -1),DOWN:Vector2(0, 1), 
                          LEFT:Vector2(-1, 0), RIGHT:Vector2(1, 0), STOP:Vector2()}
        #Direções definitas utilizando as constantes do constants.py
        self.direction = STOP #Direção inicial é PARADO
        self.setSpeed(100) #Velocidade da entity
        self.radius = 10 #Raio para desenho PADRÃO do Pygame
        self.collideRadius = 5 #Raio para definir colisões entre as entidades
        self.color = WHITE 
        self.node = node #Instancia o nódo (posição originária)
        self.setPosition() #Copia a posição de um nódo como posição atual da entidade
        self.target = node #Destino que deseja alcançar
        self.visible = True
        self.disablePortal = False
        self.goal = None
        self.directionMethod = self.randomDirection #Variável que guarda o método que será utilizado para definir o movimento
        self.setStartNode(node)
        self.image = None

    def setPosition(self): #Define a posição da entidade baseada em um nódo
        self.position = self.node.position.copy()

    def setStartNode(self, node):
        self.node = node
        self.startNode = node
        self.target = node
        self.setPosition()
          
    def validDirection(self, direction): #Checa para ver se a direção é válida (Se há nódo)
        if direction is not STOP:
            if self.name in self.node.access[direction]:
                if self.node.neighbors[direction] is not None:
                    return True
        return False

    def getNewTarget(self, direction):
        if self.validDirection(direction): #Testa para ver se possui nódo
            return self.node.neighbors[direction] #Retorna a posição do nódo que a entidade deseja chegar
        return self.node

    def overshotTarget(self): #Testa se a entidade ultrapassou o nódo que deseja chegar
        if self.target is not None:
            vec1 = self.target.position - self.node.position #Distância da origem para o destino
            vec2 = self.position - self.node.position #Distância da posição atual com a origem
            node2Target = vec1.magnitudeSquared() #Calcula o quadrado da distância
            node2Self = vec2.magnitudeSquared() 
            return node2Self >= node2Target #Ultrapassa se a distância atual (self) for maior que a do destino (target)
        return False

    def reverseDirection(self): #Reverte a direção do movimento
        self.direction *= -1 #Por isso direções opostas foram escritas com sinal oposto no constants.py
        temp = self.node #Guarda o nodo de origem
        self.node = self.target #Troca o nodo de origem pelo nodo de destino
        self.target = temp #Agora o destino é o antigo nódo de origem
        
    def oppositeDirection(self, direction): #Checa para ver se foi entrada uma direção oposta da atual
        if direction is not STOP:
            if direction == self.direction * -1:
                return True
        return False

    def setSpeed(self, speed):
        self.speed = speed * TILEWIDTH / 16 #Usa o TILEWIDTH para a velocidade ficar proporcional ao tamanho da tela

    def render(self, screen):
        if self.visible:
            if self.image is not None:
                adjust = Vector2(TILEWIDTH, TILEHEIGHT) / 2
                p = self.position - adjust
                screen.blit(self.image, p.asTuple())
            else:
                p = self.position.asInt() #Círculos no Pygame aceita somente Int
                pygame.draw.circle(screen, self.color, p, self.radius) #Desenhando o círculo

    def update(self, dt):
        self.position += self.directions[self.direction]*self.speed*dt
         
        if self.overshotTarget():
            self.node = self.target #Troca o nódo antigo para o nódo da posição destino
            directions = self.validDirections()
            direction = self.directionMethod(directions)
            if not self.disablePortal:
                if self.node.neighbors[PORTAL] is not None:
                    self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction) #Atualiza o destino
            if self.target is not self.node: #Se o destino não é a posição originária
                self.direction = direction #Movimenta para o destino
            else:
                self.target = self.getNewTarget(self.direction)

            self.setPosition() #Atualiza o nódo atual

    def validDirections(self): #Retorna uma lista com as direções válidas da entity
        directions = []
        for key in [UP, DOWN, LEFT, RIGHT]:
            if self.validDirection(key): #Testa para cada direção
                if key != self.direction * -1: #Não pode reverter!
                    directions.append(key)
        if len(directions) == 0:
            directions.append(self.direction * -1) #Se não houver outra direção, reverte
        return directions

    def randomDirection(self, directions):
        return directions[randint(0, len(directions)-1)] #Utiliza a lista directions

    def goalDirection(self, directions):
        distances = []
        for direction in directions:
            vec = self.node.position  + self.directions[direction]*TILEWIDTH - self.goal #Distância entre a posição e o destino
            distances.append(vec.magnitudeSquared()) #Inclui na lista
        index = distances.index(min(distances)) #Escolhe o índice que representa a menor distância
        return directions[index]

    def setBetweenNodes(self, direction):
        if self.node.neighbors[direction] is not None:
            self.target = self.node.neighbors[direction]
            self.position = (self.node.position + self.target.position) / 2.0

    def reset(self):
        self.setStartNode(self.startNode)
        self.direction = STOP
        self.speed = 100
        self.visible = True
