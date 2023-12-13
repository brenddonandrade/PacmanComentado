import pygame
from vector import Vector2
from constants import *

class Text(object):
    def __init__(self, text, color, x, y, size, time=None, id=None, visible=True):
        self.id = id
        self.text = text
        self.color = color
        self.size = size
        self.visible = visible
        self.position = Vector2(x, y)
        self.timer = 0
        self.lifespan = time
        self.label = None
        self.destroy = False
        self.setupFont("text/PressStart2P-Regular.ttf")
        self.createLabel()

    def setupFont(self, fontpath): #Fonte do texto
        self.font = pygame.font.Font(fontpath, self.size)

    def createLabel(self): #Imprime o texto
        self.label = self.font.render(self.text, 1, self.color)

    def setText(self, newtext): #Define o texto
        self.text = str(newtext)
        self.createLabel()

    def update(self, dt):
        if self.lifespan is not None:
            self.timer += dt
            if self.timer >= self.lifespan:
                self.timer = 0
                self.lifespan = None
                self.destroy = True

    def render(self, screen):
        if self.visible:
            x, y = self.position.asTuple()
            screen.blit(self.label, (x, y))

class TextGroup(object): #Organiza todos os textos criados
    def __init__(self):
        self.nextid = 10
        self.alltext = {}
        self.setupText()
        self.showText(READYTXT)

    def addText(self, text, color, x, y, size, time=None, id=None): #Adiciona o texto
        self.nextid += 1
        self.alltext[self.nextid] = Text(text, color, x, y, size, time=time, id=id)
        return self.nextid

    def removeText(self, id): #Remove o texto
        self.alltext.pop(id)
        
    def setupText(self): #Define como os textos irão aparecer
        size = TILEHEIGHT
        self.alltext[SCORETXT] = Text("0".zfill(8), WHITE, 0, TILEHEIGHT, size)
        self.alltext[LEVELTXT] = Text(str(1).zfill(3), WHITE, 23*TILEWIDTH, TILEHEIGHT, size)
        self.alltext[READYTXT] = Text("READY!", YELLOW, 11.25*TILEWIDTH, 20*TILEHEIGHT, size, visible=False)
        self.alltext[PAUSETXT] = Text("PAUSED!", YELLOW, 10.625*TILEWIDTH, 20*TILEHEIGHT, size, visible=False)
        self.alltext[GAMEOVERTXT] = Text("GAMEOVER!", YELLOW, 10*TILEWIDTH, 20*TILEHEIGHT, size, visible=False)
        self.addText("SCORE", WHITE, 0, 0, size)
        self.addText("LEVEL", WHITE, 23*TILEWIDTH, 0, size)

    def update(self, dt):
        for tkey in list(self.alltext.keys()):
            self.alltext[tkey].update(dt)
            if self.alltext[tkey].destroy:
                self.removeText(tkey)

    def showText(self, id): #Mostra o texto
        self.hideText()
        self.alltext[id].visible = True

    def hideText(self): #Esconde o texto
        self.alltext[READYTXT].visible = False
        self.alltext[PAUSETXT].visible = False
        self.alltext[GAMEOVERTXT].visible = False

    def updateScore(self, score): #Texto da pontuação
        self.updateText(SCORETXT, str(score).zfill(8))

    def updateLevel(self, level): #Texto do nível
        self.updateText(LEVELTXT, str(level + 1).zfill(3))

    def updateText(self, id, value): #Atualiza o texto
        if id in self.alltext.keys():
            self.alltext[id].setText(value)

    def render(self, screen): #Desenha na tela
        for tkey in list(self.alltext.keys()):
            self.alltext[tkey].render(screen)
