from constants import *

class MainMode(object):
    def __init__(self):
        self.timer = 0
        self.scatter() #Inicia no modo Scatter

    def update(self, dt):
        self.timer += dt 
        if self.timer >= self.time: #Testa o tempo para cada modo
            if self.mode is SCATTER:
                self.chase() #Troca para Chase
            elif self.mode is CHASE:
                self.scatter() #Troca para Scatter

    def scatter(self):
        self.mode = SCATTER
        self.time = 7
        self.timer = 0

    def chase(self):
        self.mode = CHASE
        self.time = 20
        self.timer = 0

class ModeController(object):
    def __init__(self, entity):
        self.timer = 0
        self.time = None
        self.mainmode = MainMode() #Para controlar a alteração dos modos
        self.current = self.mainmode.mode #Guarda o modo atual
        self.entity = entity #Instancia objeto que deseja controlar

    def update(self, dt):
        self.mainmode.update(dt) #Sobreposição do update do MainMode
        if self.current is FREIGHT: 
            self.timer += dt
            if self.timer >= self.time: #Se o Freight terminou:
                self.time = None #Reseta o tempo
                self.entity.normalMode() #Volta para o modo normal
                self.current = self.mainmode.mode #Volta para SCATTER ou CHASE
        elif self.current in [SCATTER, CHASE]:
            self.current = self.mainmode.mode #Atualiza o modo
        if self.current is SPAWN:
            if self.entity.node == self.entity.spawnNode: #Se já chegou à Home:
                self.entity.normalMode() #Volta para o modo normal
                self.current = self.mainmode.mode #SCATTER ou CHASE

    def setFreightMode(self):
        if self.current in [SCATTER, CHASE]:
            self.timer = 0
            self.time = 7
            self.current = FREIGHT
        elif self.current is FREIGHT:
            self.timer = 0

    def setSpawnMode(self):
        if self.current is FREIGHT:
           self.current = SPAWN
