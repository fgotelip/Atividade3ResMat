from Confere import eh_numero_pos,eh_sim_nao
from Elemento import Elemento
class Torcao():
    def __init__(self,elementos=[]):
        self.__elementos = elementos
        self.__resultados = []
        self.__torcaoTotal = 0
        self.__n = len(elementos)

    def set_elementos(self):
        n = input("Digite o número de elementos no eixo: ")
        while not eh_numero_pos(n):
            n = input("Digite o número de elementos no eixo: ")
        self.__n = int(n) 

        for i in range(self.__n):
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
                self.__elementos.append(n,Elemento(L,OD,G,T,oca,ID1,ID2,L1))
                
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
                self.__elementos.append(n,Elemento(L,OD,G,T))

        
    def __calculaTorcao_Tensao(self):
        i=1
        TorcaoAcumulada = 0

        for elemento in self.__elementos[::-1]:
            TorcaoAcumulada += elemento.get_TorcaoAcumulada()
            elemento.set_TAcumulada(TorcaoAcumulada)

            tauMax,tauMax2, anguloTotal = elemento.calculaTorcao_Tensao()
        
            if elemento.get_oca():
                self.__resultados.append({
                    "Elemento": i,
                    "Tensão Máxima Parte 1 (Pa)": tauMax,
                    "Tensão Máxima Parte 2 (Pa)": tauMax2,
                    "Ângulo de Torção Total (rad)": anguloTotal
                })
            else:
                self.__resultados.append({
                    "Elemento": i,
                    "Tensão Máxima (Pa)": tauMax,
                    "Ângulo de Torção Total (rad)": anguloTotal
                })
            self.__torcaoTotal += anguloTotal
            i+=1

    def exibir_resultados(self):  # Exibindo os resultados
        self.__calculaTorcao_Tensao()
        for resultado in self.__resultados:
            print(f"\nElemento {resultado['Elemento']}:")
            if "Tensão Máxima Parte 1 (Pa)" in resultado:
                print(f"  Tensão Máxima na Parte 1: {resultado['Tensão Máxima Parte 1 (Pa)']:.2f} Pa")
                print(f"  Tensão Máxima na Parte 2: {resultado['Tensão Máxima Parte 2 (Pa)']:.2f} Pa")
            else:
                print(f"  Tensão Máxima: {resultado['Tensão Máxima (Pa)']:.2f} Pa")
            print(f"  Ângulo de Torção Total: {resultado['Ângulo de Torção Total (rad)']:.6f} rad")

        print(f"\nÂngulo de Torção Total do Eixo: {self.__torcaoTotal:.6f} rad")




    
 
