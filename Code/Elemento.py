from Confere import eh_numero_pos, eh_sim_nao
import numpy as np

class Elemento():
    def __init__(self,L=0,OD=0,ID1=0,ID2=0,L1=0,G=0,T=0,oca=False):
        self.__instanciar(L,OD,ID1,ID2,L1,G,T,oca)

    def __instanciar(self,L,OD,ID1,ID2,L1,G,T,oca):
        self.__L = L
        self.__OD = OD
        self.__G = G
        self.__T = T
        self.__oca = oca
        if oca:
            self.__ID1 = ID1
            self.__ID2 = ID2
            self.__L1 = L1

    def set_dados(self,i):
        print(f"\nDigite os dados do elemento {i+1}:")
        L = input("  Comprimento total (m): ")
        while not eh_numero_pos(L):
            L = input("  Comprimento total (m): ")
        L = float(L)

        oca = input("  A parte é oca? (s/n): ")
        while not eh_sim_nao(oca):
            oca = input("  A parte é oca? (s/n): ")
        oca = oca.lower() == 's'
        
        if oca:
            OD = input("  Diâmetro externo (m): ")
            while not eh_numero_pos(OD):
                OD = input("  Diâmetro externo (m): ")
            OD = float(OD)

            ID1 = input("  Diâmetro interno da parte inicial (m) (0 se for cheio): ")
            while not eh_numero_pos(ID1,True):
                ID1 = input("  Diâmetro interno da parte inicial (m) (0 se for cheio): ")
            ID1 = float(ID1)

            ID2 = input("  Diâmetro interno da parte final (m) (0 se for cheio): ")
            while not eh_numero_pos(ID2,True):
                ID2 = input("  Diâmetro interno da parte final (m) (0 se for cheio): ")
            ID2 = float(ID2)

            L1 = input("  Comprimento da parte oca (m): ")
            while not eh_numero_pos(L1):
                L1 = input("  Comprimento da parte oca (m): ")
            L1 = float(L1)

            G = input("  Módulo de elasticidade transversal (Pa): ")
            while not eh_numero_pos(G):
                G = input("  Módulo de elasticidade transversal (Pa): ")
            G = float(G)

            T = input("  Torque aplicado (N.m): ")
            while not eh_numero_pos(T):
                T = input("  Torque aplicado (N.m): ")
            T = float(T)
            
        else:
            OD = input("  Diâmetro (m): ")
            while not eh_numero_pos(OD):
                OD = input("  Diâmetro (m): ")
            OD = float(OD)

            G = input("  Módulo de elasticidade transversal (Pa): ")
            while not eh_numero_pos(G):
                G = input("  Módulo de elasticidade transversal (Pa): ")
            G = float(G)

            T = input("  Torque aplicado (N.m): ")
            while not eh_numero_pos(T):
                T = input("  Torque aplicado (N.m): ")
            T = float(T)

        self.__instanciar(L,OD,ID1,ID2,L1,G,T,oca)

    def calculaTorcao_Tensao(self,TTotal,resultados,i):
        TTotal += self.__T

        RExt = self.__OD / 2

        if self.__oca:
            L2 = self.__L - self.__L1

            RInt1 = self.__ID1 / 2
            RInt2 = self.__ID2 / 2

            # Cálculo do momento polar de inércia J para cada parte
            J1 = (np.pi / 2) * (RExt**4 - RInt1**4) if self.__ID1 != 0 else (np.pi / 2) * RExt**4
            J2 = (np.pi / 2) * (RExt**4 - RInt2**4) if self.__ID2 != 0 else (np.pi / 2) * RExt**4

            # Cálculo da tensão máxima de cisalhamento para cada parte
            tauMax1 = (TTotal * RExt) / J1
            tauMax2 = (TTotal * RExt) / J2

            # Cálculo do ângulo de torção de cada parte
            angulo1 = (TTotal * self.__L1) / (self.__G * J1)
            angulo2 = (TTotal * L2) / (self.__G * J2)

            # Ângulo de torção total do elemento
            anguloTotal = angulo1 + angulo2

            # Adiciona os resultados individuais
            resultados.append({
                "Elemento": i + 1,
                "Tensão Máxima Parte 1 (Pa)": tauMax1,
                "Tensão Máxima Parte 2 (Pa)": tauMax2,
                "Ângulo de Torção Total (rad)": anguloTotal
            })

        else:
            J = (np.pi / 2) * RExt**4

            # Cálculo da tensão máxima de cisalhamento
            tauMax = (TTotal * RExt) / J

            # Cálculo do ângulo de torção
            anguloTotal = (TTotal * self.__L) / (self.__G * J)

            # Adiciona os resultados individuais
            resultados.append({
                "Elemento": i + 1,
                "Tensão Máxima (Pa)": tauMax,
                "Ângulo de Torção Total (rad)": anguloTotal
            })

        return TTotal,anguloTotal

        


