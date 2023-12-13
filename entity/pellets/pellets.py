import pygame
from vector import Vector2
from constants import *
import numpy as np

class Pellet(object):
    def __init__(self, row, column):
        self.name = PELLET # identificador da pellet
        self.position = Vector2(column*TILEWIDTH, row*TILEHEIGHT) # posicionando todas pellets
        self.color = WHITE # definindo suas cores
        self.radius = int(2 * TILEWIDTH / 16) # definido o tamanho das pellets cmuns
        self.collideRadius = int(2 * TILEWIDTH / 16) # atribuindo o raio de colisao
        self.points = 10 # valor em pontos de uma pellet comum
        self.visible = True # se é visivel ou nao na tela
        
    # método para renderizar a pellet na tela
    def render(self, screen):
        if self.visible:
            adjust = Vector2(TILEWIDTH, TILEHEIGHT) / 2
            p = self.position + adjust
            pygame.draw.circle(screen, self.color, p.asInt(), self.radius)

# criando a classe super pellet
class PowerPellet(Pellet):
    def __init__(self, row, column):
        # herda da pellet comum
        Pellet.__init__(self, row, column)
        self.name = POWERPELLET # seu identificador
        self.radius = int(8 * TILEWIDTH / 16) # seu raio
        self.points = 50 # quantos pontos se ganha ao comer
        # faz ficar piscando para chamar atencao a cada 0.2 segundo
        self.flashTime = 0.2
        self.timer= 0
        
    # update para fazer a powerpellet piscar
    def update(self, dt):
        self.timer += dt
        if self.timer >= self.flashTime:
            # tira e atribui visibilidade
            self.visible = not self.visible
            self.timer = 0

# classe para listar as pellets no jogo
class PelletGroup(object):
    def __init__(self, pelletfile):
        # cria a lista para atribuir as pellets
        self.pelletList = []
        # a lista de powerpellets
        self.powerpellets = []
        self.createPelletList(pelletfile)
        # número de pellets comida
        self.numEaten = 0

    def update(self, dt):
        for powerpellet in self.powerpellets:
            powerpellet.update(dt)
                
    # cria a lista de pellet através da leitura do arquivo "pelletfile"
    def createPelletList(self, pelletfile):
        data = self.readPelletfile(pelletfile)        
        for row in range(data.shape[0]):
            for col in range(data.shape[1]):
                if data[row][col] in ['.', '+']:
                    self.pelletList.append(Pellet(row, col))
                elif data[row][col] in ['P', 'p']:
                    pp = PowerPellet(row, col)
                    self.pelletList.append(pp)
                    self.powerpellets.append(pp)
    
    # arquivo de texto que gera a lista de pellet e suas localizaceos
    def readPelletfile(self, textfile):
        return np.loadtxt(textfile, dtype='<U1')
    
    # verifica se acabou a pellets
    def isEmpty(self):
        if len(self.pelletList) == 0:
            return True
        return False
    
    # renderiza as pellets na tela
    def render(self, screen):
        for pellet in self.pelletList:
            pellet.render(screen)
