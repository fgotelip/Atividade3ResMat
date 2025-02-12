from MomentoDeInercia import MomentoDeInercia
from MomentoFletor import MomentoFletor
class Tensao():
    def __init__(self,retangulos=[],buracos=[],carregamentos=[]):
        self.__momentoInercia = MomentoDeInercia(retangulos,buracos)
        self.__momentoFletor = MomentoFletor(carregamentos)
        self.__TensaoMax = 0
        self.__TensaoMin = 0
        if retangulos != [] and carregamentos != []:
            self.calcula_tensoes()
            
    def calcula_tensoes(self):
        self.__momentoInercia.calcula()
        y_max = self.__momentoInercia.getYmax()
        y_min = self.__momentoInercia.getYmin()

        MomentoMax = self.__momentoFletor.getMomentoMax()

        self.__TensaoMax = MomentoMax * y_max / self.__momentoInercia.getIxx()
        self.__TensaoMin = MomentoMax * y_min / self.__momentoInercia.getIxx()

    def set_figura(self):
        print("Defina a área de seção transversal.")
        self.__momentoInercia.setRetangulos_user()
        
        print("Defina os carregamentos.")
        self.__momentoFletor.set_carregamentos()

        self.calcula_tensoes()

    def exibe_resultados(self):
        print(f"Tensão máxima: {self.__TensaoMax}")
        print(f"Tensão mínima: {self.__TensaoMin}")
        