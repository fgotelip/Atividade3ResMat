from MomentoDeInercia import MomentoDeInercia
from MomentoFletor import MomentoFletor

## Classe para executar os calculos previstos para o exercício 2
class Tensao():
    def __init__(self,retangulos=[],buracos=[],carregamentos=[],apoios=[]): ## Construtor da classe
        self.__momentoInercia = 0
        self.__momentoFletor = 0
        self.__TracaoMax = 0
        self.__CompressaoMax = 0
        if retangulos != [] and carregamentos != []: ## Condição para testes automatizados
            self.__momentoInercia = MomentoDeInercia(retangulos,buracos)
            self.__momentoFletor = MomentoFletor(carregamentos,apoios)
            self.calcula_tensoes()
            
    def calcula_tensoes(self): ## Função para calcular as tensões na barra
        self.__momentoInercia.calcula() ## Calcula o momento de inércia da seção
        
        ## coordenada Y máxima e mínima
        y_max = self.__momentoInercia.getYmax()
        y_min = self.__momentoInercia.getYmin()
        
        ## Transformar em metros
        y_max_m = y_max*10**-3 
        y_min_m = y_min*10**-3

        MomentoMax = self.__momentoFletor.getMomentoMax() ## Momento fletor máximo
        print(f"Momento Máximo: {MomentoMax:}N.m")

        Ixx_m4 = self.__momentoInercia.getIxx()*10**-12 ## Momento de inércia x em metros^4
        
        ## Tração e compressão máximas
        TracaoMax_Pa = MomentoMax * y_max_m / Ixx_m4
        CompressaoMax_Pa = MomentoMax * y_min_m / Ixx_m4
        
        ## Transformar em MPa
        self.__TracaoMax = -TracaoMax_Pa*10**-6
        self.__CompressaoMax = CompressaoMax_Pa*10**-6

    def set_figura(self): ## Função para ler o problema
        print("Defina a área de seção transversal.")
        self.__momentoInercia.setRetangulos_user()
        
        print("Defina os carregamentos.")
        self.__momentoFletor.set_carregamentos()

        self.calcula_tensoes()

    def exibe_resultados(self): ## Função para exibir os resultados
        print(f"Tração máxima: {self.__TracaoMax:.4e}MPa")
        print(f"Compressão máxima: {self.__CompressaoMax:.4e}MPa")
