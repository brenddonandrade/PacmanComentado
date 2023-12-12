#Definições da Tela

TILEWIDTH = 16 #Pixels de comprimento
TILEHEIGHT = 16 #Pixels de altura
NROWS = 36 #Blocos de 16 pixels espalhados na vertical
NCOLS = 28 #Blocos de 16 pixels espalhados na horizontal
SCREENWIDTH = NCOLS*TILEWIDTH #Este é o Comprimento da Tela
SCREENHEIGHT = NROWS*TILEHEIGHT #Este é a Altura da tela
SCREENSIZE = (SCREENWIDTH, SCREENHEIGHT) #Tupla guardando as dimensões da tela

#Cores em RGB

BLACK = (0, 0, 0) 
YELLOW = (255, 255, 0) 
PINK = (255,100,150)
TEAL = (100,255,255)
ORANGE = (230,190,40)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

#Direções do movimento (Valores arbitrários, bastam ser opostos)

STOP = 0
UP = 1
DOWN = -1
LEFT = 2
RIGHT = -2

#Nomes (ID) de alguns objetos

PACMAN = 0 #ID do Pacman
PELLET = 1 #ID das pastilhas
POWERPELLET = 2 #ID das pastilhas power-up
GHOST = 3 #ID dos fantasmas
BLINKY = 4 #ID do Blinky
PINKY = 5 #ID do Pinky
INKY = 6 #ID do Inky
CLYDE = 7 #ID do Clyde
FRUIT = 8 #ID das frutas



PORTAL = 3


SCATTER = 0
CHASE = 1
FREIGHT = 2
SPAWN = 3




SCORETXT = 0
LEVELTXT = 1
READYTXT = 2
PAUSETXT = 3
GAMEOVERTXT = 4
