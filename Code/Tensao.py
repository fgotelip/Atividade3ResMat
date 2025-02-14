from MomentoDeInercia import MomentoDeInercia
from MomentoFletor import MomentoFletor
class Tensao():
    def __init__(self,retangulos=[],buracos=[],carregamentos=[],opcao=0,comprimento=0):
        self.__momentoInercia = MomentoDeInercia(retangulos,buracos)
        self.__momentoFletor = MomentoFletor(carregamentos,opcao,comprimento)
        self.__TracaoMax = 0
        self.__CompressaoMax = 0
        if retangulos != [] and carregamentos != []:
            self.calcula_tensoes()
            
    def calcula_tensoes(self):
        self.__momentoInercia.calcula()
        y_max = self.__momentoInercia.getYmax()
        y_min = self.__momentoInercia.getYmin()
        y_max_m = y_max*10**-3
        y_min_m = y_min*10**-3

        MomentoMax = self.__momentoFletor.getMomentoMax()
        print(f"Momento Máximo: {MomentoMax:.2f}N.m")

        Ixx_m4 = self.__momentoInercia.getIxx()*10**-12
        
        TracaoMax_Pa = MomentoMax * y_max_m / Ixx_m4
        CompressaoMax_Pa = MomentoMax * y_min_m / Ixx_m4
        self.__TracaoMax = TracaoMax_Pa*10**-6
        self.__CompressaoMax = -CompressaoMax_Pa*10**-6

    def set_figura(self):
        print("Defina a área de seção transversal.")
        self.__momentoInercia.setRetangulos_user()
        
        print("Defina os carregamentos.")
        self.__momentoFletor.set_carregamentos()

        self.calcula_tensoes()

    def exibe_resultados(self):
        print(f"Tração máxima: {self.__TracaoMax:.2f}MPa")
        print(f"Compressão mínima: {self.__CompressaoMax:.2f}MPa")
        