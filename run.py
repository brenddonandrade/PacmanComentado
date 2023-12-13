import pygame
from pygame.locals import * #Constantes do Pygame
from constants import *
from entity.pacman.pacman import Pacman
from maze.nodes import NodeGroup
from entity.pellets.pellets import PelletGroup
from entity.ghosts.ghosts import GhostGroup
from entity.fruits.fruit import Fruit
from pauser import Pause
from text.text import TextGroup
from sprites.sprites import LifeSprites
from sprites.sprites import MazeSprites

#Este é nosso arquivo principal, se quiser rodar o jogo, é por aqui

class GameController(object):
    def __init__(self):
        pygame.init() #Inicializar o Pygame
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32) #Definindo a Tela
        self.background = None
        self.background_norm = None
        self.background_flash = None
        self.clock = pygame.time.Clock() #Inicializa a passagem de tempo
        self.fruit = None
        self.pause = Pause(True)
        self.level = 0
        self.lives = 5
        self.score = 0
        self.textgroup = TextGroup()
        self.lifesprites = LifeSprites(self.lives)
        self.flashBG = False
        self.flashTime = 0.2
        self.flashTimer = 0
        self.fruitCaptured = []

    def setBackground(self): #Aqui criamos o fundo (cor BLACK)
        self.background_norm = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_norm.fill(BLACK)
        self.background_flash = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_flash.fill(BLACK)
        self.background_norm = self.mazesprites.constructBackground(self.background_norm, self.level%5)
        self.background_flash = self.mazesprites.constructBackground(self.background_flash, 5)
        self.flashBG = False
        self.background = self.background_norm

    def restartGame(self):
        self.lives = 5
        self.level = 0
        self.pause.paused = True
        self.fruit = None
        self.score = 0
        self.textgroup.updateScore(self.score)
        self.textgroup.updateLevel(self.level)
        self.textgroup.showText(READYTXT)
        self.startGame()
        self.lifesprites.resetLives(self.lives)
        self.fruitCaptured = []

    def resetLevel(self):
        self.pause.paused = True
        self.pacman.reset()
        self.ghosts.reset()
        self.fruit = None
        self.textgroup.showText(READYTXT)

    def nextLevel(self):
        self.showEntities()
        self.level += 1
        self.pause.paused = True
        self.textgroup.showText(READYTXT) #teste
        self.startGame()
        self.textgroup.updateLevel(self.level)
        
    def startGame(self):
        self.mazesprites = MazeSprites("maze/maze1.txt", "maze/maze1_rotation.txt")
        self.setBackground() #Ao iniciar o jogo, constroi o fundo
        self.nodes = NodeGroup("maze/maze1.txt") #Instancia objeto da classe NodeGroup
        self.nodes.setPortalPair((0,17), (27,17))
        homekey = self.nodes.createHomeNodes(11.5, 14) #Colhe a chave do nodo acima da casa
        self.nodes.connectHomeNodes(homekey, (12,14), LEFT) #Coneta o nodo da casa à ESQUERDA
        self.nodes.connectHomeNodes(homekey, (15,14), RIGHT) #Conecta o nodo da casa à DIREITA
        self.pacman = Pacman(self.nodes.getNodeFromTiles(15, 26)) #Instancia objeto Pacman
        self.pellets = PelletGroup("maze/maze1.txt") #Instancia o grupo de pastilhas
        self.ghosts = GhostGroup(self.nodes.getStartTempNode(), self.pacman) #Instancia o grupo de fantasmas
        self.ghosts.blinky.setStartNode(self.nodes.getNodeFromTiles(2+11.5, 0+14)) #Posição inicial do Blinky
        self.ghosts.pinky.setStartNode(self.nodes.getNodeFromTiles(2+11.5, 3+14)) #Posição inicial do Pinky
        self.ghosts.inky.setStartNode(self.nodes.getNodeFromTiles(0+11.5, 3+14)) #Posição inicial do Inky
        self.ghosts.clyde.setStartNode(self.nodes.getNodeFromTiles(4+11.5, 3+14)) #Posição inicial do Clyde
        self.ghosts.setSpawnNode(self.nodes.getNodeFromTiles(2+11.5, 3+14)) #Definir a posição de origem
        self.nodes.denyHomeAccess(self.pacman) #Negar o acesso à casa
        self.nodes.denyHomeAccessList(self.ghosts) #Lista de entidades com acesso negado à casa
        self.nodes.denyAccessList(2+11.5, 3+14, LEFT, self.ghosts) #Acessar o nodo de entrada da casa pela ESQUERDA
        self.nodes.denyAccessList(2+11.5, 3+14, RIGHT, self.ghosts) #Acessar o nodo de entrada da casa pela DIREITA
        self.ghosts.inky.startNode.denyAccess(RIGHT, self.ghosts.inky) #Negar o acesso da saída ao Inky
        self.ghosts.clyde.startNode.denyAccess(LEFT, self.ghosts.clyde) #Negar o acesso da saída ao Clyde
        self.nodes.denyAccessList(12, 14, UP, self.ghosts) 
        self.nodes.denyAccessList(15, 14, UP, self.ghosts)
        self.nodes.denyAccessList(12, 26, UP, self.ghosts)
        self.nodes.denyAccessList(15, 26, UP, self.ghosts)


    def update(self): #Será chamado a cada quadro do jogo (game loop)
        dt = self.clock.tick(30) / 1000.0 #Quanto tempo passou desde a última vez que este método foi chamado
        self.textgroup.update(dt)
        self.pellets.update(dt) #Atualizar as pastilhas
        if not self.pause.paused:
            self.ghosts.update(dt) #Atualiza as disposições do fantasma
            if self.fruit is not None:
                self.fruit.update(dt)
            self.checkPelletEvents() #Checar os eventos de colisões com a pastilha
            self.checkGhostEvents() #Checar os eventos de colisões com os fantasmas
            self.checkFruitEvents() #Checar os eventos de colisões com as frutas

        if self.pacman.alive:
            if not self.pause.paused:
                self.pacman.update(dt) #Atualizar constantemente a posição do Pacman
        else:
            self.pacman.update(dt) 

        if self.flashBG:
            self.flashTimer += dt
            if self.flashTimer >= self.flashTime:
                self.flashTimer = 0
                if self.background == self.background_norm:
                    self.background = self.background_flash
                else:
                    self.background = self.background_norm
            
        afterPauseMethod = self.pause.update(dt)
        if afterPauseMethod is not None:
            afterPauseMethod()
        self.checkEvents() #Checar Eventos de Input
        self.render() #Método para desenhar as imagens na tela

    def updateScore(self, points):
        self.score += points
        self.textgroup.updateScore(self.score)

    def checkFruitEvents(self):
        if self.pellets.numEaten == 50 or self.pellets.numEaten == 140:
            if self.fruit is None:
                self.fruit = Fruit(self.nodes.getNodeFromTiles(9, 20))
        if self.fruit is not None:
            if self.pacman.collideCheck(self.fruit):
                self.updateScore(self.fruit.points)
                self.textgroup.addText(str(self.fruit.points), WHITE, self.fruit.position.x, self.fruit.position.y, 8, time=1)
                fruitCaptured = False
                for fruit in self.fruitCaptured:
                    if fruit.get_offset() == self.fruit.image.get_offset():
                        fruitCaptured = True
                        break
                if not fruitCaptured:
                    self.fruitCaptured.append(self.fruit.image)
                self.fruit = None
            elif self.fruit.destroy:
                self.fruit = None

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT: #Se apertar o 'X' da tela, sair
                exit()
            elif event.type == KEYDOWN: 
                if event.key == K_SPACE: #Checa se o espaço foi apertado
                    if self.flashBG == False: #A pausa só ocorrerá se a tela não estiver piscando
                        if self.pacman.alive: 
                            self.pause.setPause(playerPaused=True) #Pausa ou despausa o jogo!
                            if not self.pause.paused: #Se não está pausado, não mostra textos extras e mostra as entidades
                                self.textgroup.hideText()
                                self.showEntities()
                            else: #se está pausado, mostra PAUSED! e esconde as entidades
                                self.textgroup.showText(PAUSETXT) 
                                self.hideEntities()

    def checkGhostEvents(self):
        for ghost in self.ghosts:
            if self.pacman.collideGhost(ghost): #Checa se o Pacman colidiu com um fantasma
               if ghost.mode.current is FREIGHT: #Se o fantasma estiver no modo Freight, então o Pacman irá comê-lo
                    self.pacman.visible = False #Esconde o sprite do Pacman e do fantasma
                    ghost.visible = False
                    self.updateScore(ghost.points) #Incrementa os pontos dos fantasmas
                    self.textgroup.addText(str(ghost.points), WHITE, ghost.position.x, ghost.position.y, 8, time=1) #Mostra os pontos adquiridos
                    self.ghosts.updatePoints() #Atualiza os pontos
                    self.pause.setPause(pauseTime=1, func=self.showEntities) #Pausa por um segundo o jogo
                    ghost.startSpawn() #Inicia o modo Spawn
                    self.nodes.allowHomeAccess(ghost) #Permite o acesso do fantasma à casa
                    
               elif ghost.mode.current is not SPAWN: #Se estiver no Scatter ou Chase, então Pacman morreu!
                    if self.pacman.alive:
                        self.lives -=  1 #Perde vida
                        self.lifesprites.removeImage() #Remove uma vida
                        self.pacman.die() #Animação da morte do Pacman
                        self.ghosts.hide() #esconde os fantasmas
                        if self.lives <= 0: #Se não houver mais vida
                           self.textgroup.showText(GAMEOVERTXT)
                           self.pause.setPause(pauseTime=3, func=self.restartGame) #Reinicia o jogo!
                        else:
                           self.pause.setPause(pauseTime=3, func=self.resetLevel) #Reseta a posição do Pacman e dos fantasmas

    def showEntities(self):
        self.pacman.visible = True
        self.ghosts.show()

    def hideEntities(self):
        self.pacman.visible = False
        self.ghosts.hide()

    def render(self):
        self.screen.blit(self.background, (0, 0)) #Redesenhar o fundo para excluir a 'fotografia' do movimento anterior
        self.pellets.render(self.screen) #Desenha as pastilhas na tela
        if self.fruit is not None:
            self.fruit.render(self.screen) #Desenha as frutas na tela
        self.pacman.render(self.screen) #Desenha o Pacman na tela
        self.ghosts.render(self.screen) #Desenha os fantasmas na tela
        self.textgroup.render(self.screen) #Escreve os textos na tela
        for i in range(len(self.lifesprites.images)):
            x = self.lifesprites.images[i].get_width() * i
            y = SCREENHEIGHT - self.lifesprites.images[i].get_height()
            self.screen.blit(self.lifesprites.images[i], (x, y))
        for i in range(len(self.fruitCaptured)):
            x = SCREENWIDTH - self.fruitCaptured[i].get_width() * (i+1)
            y = SCREENHEIGHT - self.fruitCaptured[i].get_height()
            self.screen.blit(self.fruitCaptured[i], (x, y))
        pygame.display.update()

    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.pellets.numEaten += 1
            self.updateScore(pellet.points)
            if self.pellets.numEaten == 30:
                self.ghosts.inky.startNode.allowAccess(RIGHT, self.ghosts.inky)
            if self.pellets.numEaten == 70:
                self.ghosts.clyde.startNode.allowAccess(LEFT, self.ghosts.clyde)
            self.pellets.pelletList.remove(pellet)
            if pellet.name == POWERPELLET:
                self.ghosts.startFreight()
            if self.pellets.isEmpty():
                self.flashBG = True
                self.hideEntities()
                self.pause.setPause(pauseTime=3, func=self.nextLevel)


if __name__ == "__main__": #Faz com que o módulo run.py seja executado como um programa
    game = GameController() #Instancia um objeto da classe GameController
    game.startGame() #Inicia o jogo através do objeto
    while True: #Loop infinito (até o X ser pressionado)
        game.update() #Continuamente irá atualizar o jogo
