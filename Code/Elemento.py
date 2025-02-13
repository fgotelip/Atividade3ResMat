from Confere import eh_numero_pos, eh_sim_nao
import numpy as np

## Classe para instanciar elementos e calcular suas informações
class Elemento():
    def __init__(self,L,OD,G,T,oca=False,ID1=0,ID2=0,L1=0): ## Construtor da classe
        self.__L = L ## Comprimento total do elemento
        self.__OD = OD ## Diâmetro externo do elemento
        self.__G = G ## Módulo de elasticidade transversal
        self.__T = T ## Torque aplicado no elemento
        self.__TAcumulada = self.__T ## Torque acumulado no elemento
        self.__oca = oca ## Indica se o elemento é oco ou não
        if oca: ## Caso seja oco
            self.__ID1 = ID1 ## Diâmetro interno da parte incial
            self.__ID2 = ID2 ## Diâmetro interno da parte final
            self.__L1 = L1 ## Comprimento da parte oca

    def get_oca(self): ## Retorna se o elemento é oco ou não
        return self.__oca 
    
    def get_TorcaoAcumulada(self): ## Retorna o torque acumulado
        return self.__TAcumulada
    
    def set_TAcumulada(self,TAcumulada): ## Define o torque acumulado
        self.__TAcumulada = TAcumulada

    def calculaTorcao_Tensao(self): ## Função para calcular o torque e a tensão máxima do elemento
        tauMax=0 ## Variável para armazenar a tensão máxima
        tauMax2 = 0 ## Variável para armazenar a tensão máxima da parte 2
        RExt = self.__OD / 2 ## Variável para armazenar o raio externo
        anguloTotal=0 ## Variável para armazenar o ângulo de torção total

        if self.__oca: ## Caso seja oco
            L2 = self.__L - self.__L1

            RInt1 = self.__ID1 / 2
            RInt2 = self.__ID2 / 2

            ## Cálculo do momento polar de inércia J para cada parte
            J1 = (np.pi / 2) * (RExt**4 - RInt1**4) if self.__ID1 != 0 else (np.pi / 2) * RExt**4
            J2 = (np.pi / 2) * (RExt**4 - RInt2**4) if self.__ID2 != 0 else (np.pi / 2) * RExt**4

            ## Cálculo da tensão máxima de cisalhamento para cada parte
            tauMax = (self.__TAcumulada * RExt) / J1
            tauMax2 = (self.__TAcumulada * RExt) / J2

            ## Cálculo do ângulo de torção de cada parte
            angulo1 = (self.__TAcumulada * self.__L1) / (self.__G * J1)
            angulo2 = (self.__TAcumulada * L2) / (self.__G * J2)

            anguloTotal = angulo1 + angulo2 ## Ângulo de torção total do elemento
        else:
            J = (np.pi / 2) * RExt**4

            tauMax = (self.__TAcumulada * RExt) / J ## Cálculo da tensão máxima de cisalhamento

            anguloTotal = (self.__TAcumulada * self.__L) / (self.__G * J) ## Cálculo do ângulo de torção

        return tauMax,tauMax2, anguloTotal



        


