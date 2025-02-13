from Confere import eh_numero_pos, eh_sim_nao
import numpy as np

class Elemento():
    def __init__(self,L,OD,G,T,oca=False,ID1=0,ID2=0,L1=0):
        self.__L = L
        self.__OD = OD
        self.__G = G
        self.__T = T
        self.__TAcumulada = self.__T
        self.__oca = oca
        if oca:
            self.__ID1 = ID1
            self.__ID2 = ID2
            self.__L1 = L1

    def get_oca(self):
        return self.__oca
    
    def get_TorcaoAcumulada(self):
        return self.__TAcumulada
    
    def set_TAcumulada(self,TAcumulada):
        self.__TAcumulada = TAcumulada

    def calculaTorcao_Tensao(self):
        tauMax2 = 0
        RExt = self.__OD / 2

        if self.__oca:
            L2 = self.__L - self.__L1

            RInt1 = self.__ID1 / 2
            RInt2 = self.__ID2 / 2

            # Cálculo do momento polar de inércia J para cada parte
            J1 = (np.pi / 2) * (RExt**4 - RInt1**4) if self.__ID1 != 0 else (np.pi / 2) * RExt**4
            J2 = (np.pi / 2) * (RExt**4 - RInt2**4) if self.__ID2 != 0 else (np.pi / 2) * RExt**4

            # Cálculo da tensão máxima de cisalhamento para cada parte
            tauMax = (self.__TAcumulada * RExt) / J1
            tauMax2 = (self.__TAcumulada * RExt) / J2

            # Cálculo do ângulo de torção de cada parte
            angulo1 = (self.__TAcumulada * self.__L1) / (self.__G * J1)
            angulo2 = (self.__TAcumulada * L2) / (self.__G * J2)

            # Ângulo de torção total do elemento
            anguloTotal = angulo1 + angulo2
        else:
            J = (np.pi / 2) * RExt**4

            # Cálculo da tensão máxima de cisalhamento
            tauMax = (self.__TAcumulada * RExt) / J

            # Cálculo do ângulo de torção
            anguloTotal = (self.__TAcumulada * self.__L) / (self.__G * J)

        return tauMax,tauMax2, anguloTotal



        


