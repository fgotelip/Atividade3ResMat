import numpy as np

def calcularTorcaoETensao(n, elementos):
    resultados = []
    torcaoTotal = 0  # Ângulo de torção total do eixo
    elementos.reverse()
    TTotal=0
    for i in range(n):
        L = elementos[i]["L"]   ## Comprimento do eixo
        OD = elementos[i]["OD"] ## Diâmetro externo
        G = elementos[i]["G"]   ## Módulo de elasticidade
        T = elementos[i]["T"]   ## Torque
        TTotal+=T
        if elementos[i]["oca"]: ## Se o elemento é oco
            ID1 = elementos[i]["ID1"] ## Diâmetro interno da parte inicial
            ID2 = elementos[i]["ID2"] ## Diâmetro interno da parte final
            L1 = elementos[i]["L1"]   ## Comprimento da parte inicial
            L2 = L - L1  ## Comprimento da parte final

            RExt = OD / 2  # Raio externo
            RInt1 = ID1 / 2  # Raio interno da parte inicial
            RInt2 = ID2 / 2  # Raio interno da parte final

            # Cálculo do momento polar de inércia J para cada parte
            J1 = (np.pi / 2) * (RExt**4 - RInt1**4) if ID1 != 0 else (np.pi / 2) * RExt**4
            J2 = (np.pi / 2) * (RExt**4 - RInt2**4) if ID2 != 0 else (np.pi / 2) * RExt**4

            print(f"cas {J1}" )

            print(f"A: {J1,J2}")
            # Cálculo da tensão máxima de cisalhamento para cada parte
            tauMax1 = (TTotal * RExt) / J1
            tauMax2 = (TTotal * RExt) / J2

            # Cálculo do ângulo de torção de cada parte
            angulo1 = (TTotal * L1) / (G * J1)
            angulo2 = (TTotal * L2) / (G * J2)
            
            print("porra")
            print(angulo1, angulo2)

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
            # Elemento cheio
            RExt = OD / 2  # Raio externo

            # Cálculo do momento polar de inércia J
            J = (np.pi / 2) * RExt**4
            print(J)
            # Cálculo da tensão máxima de cisalhamento
            tauMax = (TTotal * RExt) / J

            # Cálculo do ângulo de torção
            anguloTotal = (TTotal * L) / (G * J)

            print(f"vas: {anguloTotal}")

            # Adiciona os resultados individuais
            resultados.append({
                "Elemento": i + 1,
                "Tensão Máxima (Pa)": tauMax,
                "Ângulo de Torção Total (rad)": anguloTotal
            })

        # Acumula o ângulo de torção total do eixo
        torcaoTotal += anguloTotal

    return resultados, torcaoTotal

# Entrada de dados pelo usuário
n = int(input("Digite o número de elementos no eixo: "))
elementos = []

for i in range(n):
    print(f"\nDigite os dados do elemento {i+1}:")
    L = float(input("  Comprimento total (m): "))
    oca = input("  A parte é oca? (s/n): ").lower() == 's'
    
    if oca:
        OD = float(input("  Diâmetro externo (m): "))
        ID1 = float(input("  Diâmetro interno da parte inicial (m) (0 se for cheio): "))
        ID2 = float(input("  Diâmetro interno da parte final (m) (0 se for cheio): "))
        L1 = float(input("  Comprimento da parte inicial (m): "))
        G = float(input("  Módulo de elasticidade transversal (Pa): "))
        T = float(input("  Torque aplicado (N.m): "))
        elementos.append({"L": L, "OD": OD, "ID1": ID1, "ID2": ID2, "L1": L1, "G": G, "T": T, "oca": True})
    else:
        OD = float(input("  Diâmetro (m): "))
        G = float(input("  Módulo de elasticidade transversal (Pa): "))
        T = float(input("  Torque aplicado (N.m): "))
        elementos.append({"L": L, "OD": OD, "G": G, "T": T, "oca": False})
"""n=2
elementos=[]
elementos.append({"L": 0.8, "OD": 0.06, "ID1": 0.044, "ID2": 0, "L1": 0.6, "G": 77e9, "T": 2000, "oca": True})
elementos.append({"L": 0.4, "OD": 0.03, "G": 77e9, "T": 250, "oca": False})"""

# Executando os cálculos
resultados, torcaoTotal = calcularTorcaoETensao(n, elementos)

# Exibindo os resultados
for resultado in resultados:
    print(f"\nElemento {resultado['Elemento']}:")
    if "Tensão Máxima Parte 1 (Pa)" in resultado:
        print(f"  Tensão Máxima na Parte 1: {resultado['Tensão Máxima Parte 1 (Pa)']:.2f} Pa")
        print(f"  Tensão Máxima na Parte 2: {resultado['Tensão Máxima Parte 2 (Pa)']:.2f} Pa")
    else:
        print(f"  Tensão Máxima: {resultado['Tensão Máxima (Pa)']:.2f} Pa")
    print(f"  Ângulo de Torção Total: {resultado['Ângulo de Torção Total (rad)']:.6f} rad")

print(f"\nÂngulo de Torção Total do Eixo: {torcaoTotal:.6f} rad")
