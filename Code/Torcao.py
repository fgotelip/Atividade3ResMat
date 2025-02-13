from Confere import eh_numero_pos
from Elemento import Elemento
class Torcao():
    def __init__(self,elementos=[],n=0):
        self.__elementos = elementos
        self.__resultados = []
        self.__torcaoTotal = 0
        self.__n = n

    def set_elementos(self):
        n = input("Digite o número de elementos no eixo: ")
        while not eh_numero_pos(n):
            n = input("Digite o número de elementos no eixo: ")
        self.__n = int(n)
        for i in range(n):
            elemento = Elemento()
            elemento.set_elemento(i)
            self.__elementos.append(elemento)

    
        
    def calculaTorcao_Tensao(self):
        elementos = self.__elementos.reverse()
        TAcumulada = 0
        for i in range(self.__n):
            elementos[i].

    
 
