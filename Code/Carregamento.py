from Esforcos import gera_esforcos
from Confere import eh_numero

class Carregamento():
    def __init__(self, x1=0, x2=0, carga1=0, carga2=0):
        self.__instanciar(x1,x2,carga1,carga2)

    def __instanciar(self,x1,x2,carga1,carga2):
        posicao2 = 0
        resultante2 = 0

        if carga1 == carga2:
            posicao = (x1 + x2)/2
            resultante = -(x2 - x1)*carga1
        elif carga1 == 0:
            posicao = x1+((x2-x1)*(2/3))
            resultante = -(x2 - x1)*carga2/2
        elif carga2 == 0:
            posicao = x1+((x2-x1)*(1/3))
            resultante = -(x2 - x1)*carga1/2
        elif carga1 > carga2:
            posicao = (x1 + x2)/2
            resultante = -(x2 - x1)*carga2
            posicao2 = x1+((x2-x1)*(1/3))
            resultante2 = -(x2 - x1)*(carga1-carga2)/2
        elif carga1 < carga2:
            posicao = (x1 + x2)/2
            resultante = -(x2 - x1)*carga1
            posicao2 = x1+((x2-x1)*(2/3))
            resultante2 = -(x2 - x1)*(carga2-carga1)/2

        self.__x1 = x1
        self.__x2 = x2
        self.__carga1 = carga1
        self.__carga2 = carga2
        self.__posicao = round(posicao,2)
        self.__posicao2 = round(posicao2,2)
        self.__resultante = resultante
        self.__resultante2 = resultante2

    def get_posicao(self):
        return self.__posicao

    def get_posicao2(self):
        return self.__posicao2

    def get_resultante(self):
        return self.__resultante

    def get_resultante2(self):
        return self.__resultante2

    def get_x1(self):
        return self.__x1

    def get_x2(self):
        return self.__x2

    def parser(self,num,px2):
        print("Vamos definir o carregamento", num, "(cargas em N/m e tamanho da barra em m):")
        x1 = px2

        tam = input("Tamanho da barra = ")
        while not eh_numero(tam):
            tam = input("Tamanho da barra =  ")
        tam = float(tam)
        x2=x1+tam

        carga1 = input("Carga 1 = ")
        while not eh_numero(carga1,True):
            carga1 = input("Carga 1 =   ")
        carga1 = float(carga1)

        carga2 = input("Carga 2 =  ")
        while not eh_numero(carga2,True):
            carga2 = input("Carga 2 =  ")
        carga2 = float(carga2)

        self.__instanciar(x1,x2,carga1,carga2)

        return x2

    def gerar_esforco(self,vant,mant,xant=0):
        v,m = gera_esforcos(self.__carga1,self.__carga2,self.__x1,self.__x2,vant,mant,xant)
        return v,m


