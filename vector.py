import math

class Vector2(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.thresh = 0.000001

    '''
    Aqui iremos fazer o polimorfismo através da sobreposição de alguns métodos mágicos 
    para introduzir as operações  vetoriais
    '''

    def __add__(self, other):
            return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def __div__(self, scalar):
        #if scalar != 0: (como era antes)
        # como está agora com o tratamento de erros
        try:
            V = Vector2(self.x / float(scalar), self.y / float(scalar))
            return V
        except ZeroDivisionError: #Tratamento de Exceção
            return None

    def __truediv__(self, scalar): #Utilizado no Python 3, o __div__ é padrão no Python 2
        return self.__div__(scalar)

    def __eq__(self, other): #Comparar dois vetores
        if abs(self.x - other.x) < self.thresh: #(Se a diferença for menor que thresh, então são iguais)

            if abs(self.y - other.y) < self.thresh:
                return True
        return False

    def magnitudeSquared(self): #Iremos utilizar este para comparar comprimento de vetores
        return self.x**2 + self.y**2

    def magnitude(self): #É bom evitar o uso de raizes quadradas
        return math.sqrt(self.magnitudeSquared())

    def copy(self): #Copiar vetor
        return Vector2(self.x, self.y)

    def asTuple(self): #Transformar coordenadas em tupla
        return self.x, self.y

    def asInt(self): #Transformar coordenadas em inteiro
        return int(self.x), int(self.y)

    def __str__(self): #Imprimir os vetores
        return "<"+str(self.x)+", "+str(self.y)+">"

