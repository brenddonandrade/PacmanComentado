import pygame
from constants import *
import numpy as np
from animation import Animator

BASETILEWIDTH = 16
BASETILEHEIGHT = 16
DEATH = 5

class Spritesheet(object):
    def __init__(self):
        self.sheet = pygame.image.load("sprites/spritesheet.png").convert() #Pega o Spritesheet
        transcolor = self.sheet.get_at((0,0))
        self.sheet.set_colorkey(transcolor)
        width = int(self.sheet.get_width() / BASETILEWIDTH * TILEWIDTH)
        height = int(self.sheet.get_height() / BASETILEHEIGHT * TILEHEIGHT)
        self.sheet = pygame.transform.scale(self.sheet, (width, height)) #Modela o tamanho
        
        
    def getImage(self, x, y, width, height):
        x *= TILEWIDTH
        y *= TILEHEIGHT
        self.sheet.set_clip(pygame.Rect(x, y, width, height))
        return self.sheet.subsurface(self.sheet.get_clip()) #Retorna o sprite desejado

class PacmanSprites(Spritesheet): #Sprites do Pacman
    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.entity = entity
        self.entity.image = self.getStartImage()
        self.animations = {}
        self.defineAnimations()
        self.stopimage = (8, 0)

    def getStartImage(self):
        return self.getImage(8, 0) #Coordenadas do sprite

    def getImage(self, x, y):
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT) #Pega o Spritesheet

    def defineAnimations(self):
        self.animations[LEFT] = Animator(((8,0), (0, 0), (0, 2), (0, 0))) #Coordenadas para cada sprite
        self.animations[RIGHT] = Animator(((10,0), (2, 0), (2, 2), (2, 0)))
        self.animations[UP] = Animator(((10,2), (6, 0), (6, 2), (6, 0)))
        self.animations[DOWN] = Animator(((8,2), (4, 0), (4, 2), (4, 0)))
        self.animations[DEATH] = Animator(((0, 12), (2, 12), (4, 12), (6, 12), (8, 12), (10, 12), (12, 12), (14, 12), (16, 12), (18, 12), (20, 12)), speed=6, loop=False)

    def update(self, dt): #Atualiza os sprites para cada movimento realizado
        if self.entity.alive == True:
            if self.entity.direction == LEFT:
                self.entity.image = self.getImage(*self.animations[LEFT].update(dt))
                self.stopimage = (8, 0)
            elif self.entity.direction == RIGHT:
                self.entity.image = self.getImage(*self.animations[RIGHT].update(dt))
                self.stopimage = (10, 0)
            elif self.entity.direction == DOWN:
                self.entity.image = self.getImage(*self.animations[DOWN].update(dt))
                self.stopimage = (8, 2)
            elif self.entity.direction == UP:
                self.entity.image = self.getImage(*self.animations[UP].update(dt))
                self.stopimage = (10, 2)
            elif self.entity.direction == STOP:
                self.entity.image = self.getImage(*self.stopimage)
        else:
           self.entity.image = self.getImage(*self.animations[DEATH].update(dt))

    def reset(self):
        for key in list(self.animations.keys()):
            self.animations[key].reset()


class GhostSprites(Spritesheet): #Sprites dos Fantasmas
    def __init__(self, entity):
        Spritesheet.__init__(self)
        self.x = {BLINKY:0, PINKY:2, INKY:4, CLYDE:6}
        self.entity = entity
        self.entity.image = self.getStartImage()
               
    def getStartImage(self): #Pega cada sprite dos fantasmas
        return self.getImage(self.x[self.entity.name], 4)

    def getImage(self, x, y): #Pega o Spritesheet
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)

    def update(self, dt): #Modifica o sprite dependendo da direção de movimento
        x = self.x[self.entity.name]
        if self.entity.mode.current in [SCATTER, CHASE]:
            if self.entity.direction == LEFT:
                self.entity.image = self.getImage(x, 8)
            elif self.entity.direction == RIGHT:
                self.entity.image = self.getImage(x, 10)
            elif self.entity.direction == DOWN:
                self.entity.image = self.getImage(x, 6)
            elif self.entity.direction == UP:
                self.entity.image = self.getImage(x, 4)
                
        elif self.entity.mode.current == FREIGHT:
            self.entity.image = self.getImage(10, 4)
            if self.entity.mode.timer >= 5:
                self.entity.image = self.getImage(10, 6)
                
        elif self.entity.mode.current == SPAWN:
            if self.entity.direction == LEFT:
                self.entity.image = self.getImage(8, 8)
            elif self.entity.direction == RIGHT:
                self.entity.image = self.getImage(8, 10)
            elif self.entity.direction == DOWN:
                self.entity.image = self.getImage(8, 6)
            elif self.entity.direction == UP:
               self.entity.image = self.getImage(8, 4)

class FruitSprites(Spritesheet): #Sprites das frutas
    def __init__(self, entity, level):
        Spritesheet.__init__(self)
        self.entity = entity
        self.fruits = {0:(16,8), 1:(18,8), 2:(20,8), 3:(16,10), 4:(18,10), 5:(20,10)}
        self.entity.image = self.getStartImage(level % len(self.fruits))

    def getStartImage(self, key): #Sprites de cada fruta
        return self.getImage(*self.fruits[key])

    def getImage(self, x, y): #Spritesheet
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)

class LifeSprites(Spritesheet): #Mesmos sprites do Pacman
    def __init__(self, numlives):
        Spritesheet.__init__(self)
        self.resetLives(numlives)

    def removeImage(self):
        if len(self.images) > 0: #Se a imagem existir
            self.images.pop(0)

    def resetLives(self, numlives): #Reseta quantas vidas quiser
        self.images = []
        for i in range(numlives):
            self.images.append(self.getImage(0,0))

    def getImage(self, x, y): #Pega o Spritesheet
        return Spritesheet.getImage(self, x, y, 2*TILEWIDTH, 2*TILEHEIGHT)

class MazeSprites(Spritesheet): #Sprites do labirinto
    def __init__(self, mazefile, rotfile):
        Spritesheet.__init__(self)
        self.data = self.readMazeFile(mazefile)
        self.rotdata = self.readMazeFile(rotfile)

    def getImage(self, x, y): #Pega cada sprite do labirinto
        return Spritesheet.getImage(self, x, y, TILEWIDTH, TILEHEIGHT)

    def readMazeFile(self, mazefile): #Le o arquivo do labirinto
        return np.loadtxt(mazefile, dtype='<U1')

    def constructBackground(self, background, y): #Constroi o BackGround
        for row in list(range(self.data.shape[0])):
            for col in list(range(self.data.shape[1])):
                if self.data[row][col].isdigit():
                    x = int(self.data[row][col]) + 12
                    sprite = self.getImage(x, y)
                    rotval = int(self.rotdata[row][col])
                    sprite = self.rotate(sprite, rotval)
                    background.blit(sprite, (col*TILEWIDTH, row*TILEHEIGHT))
                elif self.data[row][col] == '=':
                    sprite = self.getImage(10, 8)
                    background.blit(sprite, (col*TILEWIDTH, row*TILEHEIGHT))

        return background

    def rotate(self, sprite, value): #Rotaciona os Sprites
        return pygame.transform.rotate(sprite, value*90)
