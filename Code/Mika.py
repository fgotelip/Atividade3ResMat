## Exercício 1

import numpy as np
from scipy.integrate import quad
import sympy as sp
import matplotlib.pyplot as plt

def calcularReacoesPontual(forcas, comprimento): ## Função para calcular as reações de apoio para cargas pontuais
    a, b = sp.symbols('RA RB')
    somaForcas = 0
    momentos = 0
    for forca in forcas: ## Loop para percorrer as forças
        posicao = forca['posicao']
        intensidade = forca['intensidade']
        somaForcas += intensidade ## Adiciona as forças
        momentos += intensidade * posicao ## Adiciona os momentos
    momentos -= b * comprimento
    equacoes = [a + b - somaForcas, momentos]
    solucoes = sp.solve(equacoes, [a, b]) ## Resolve as equações para encontrar as reações de apoio

    return {a: solucoes[a], b: solucoes[b]}

def calcularReacoesGeometricas(carregamentos, comprimento): ## Função para calcular as reações de apoio para cargas geométricas
    a, b = sp.symbols('RA RB')
    somaForcas = 0
    momentos = 0
    for carga in carregamentos: ## Loop para percorrer as cargas
        tipo = carga['tipo']
        inicio = carga['inicio']
        fim = carga['fim']
        if tipo == 1: ## Triângulo
            intensidade = carga['intensidade']
            fResultante = 0.5 * intensidade * (fim - inicio) ## Calcula a força resultante
            pResultante = inicio + (2 / 3) * (fim - inicio) ## Calcula a posição da força resultante

        elif tipo == 2: ## Retângulo
            intensidade = carga['intensidade']
            fResultante = intensidade * (fim - inicio) ## Calcula a força resultante
            pResultante = (inicio + fim) / 2 ## Calcula a posição da força resultante

        else:
            baseMaior = carga['baseMaior']
            baseMenor = carga['baseMenor']
            altura = fim - inicio
            fResultante = 0.5 * (baseMaior + baseMenor) * altura ## Calcula a força resultante
            pResultante = inicio + ((2 * baseMaior + baseMenor) / (3 * (baseMaior + baseMenor))) * altura ## Calcula a posição da força resultante
        momentos += fResultante * pResultante ## Calcula o momento total
        somaForcas += fResultante ## Calcula a força total
    momentos -= b * comprimento
    equacoes = [a + b - somaForcas, momentos]
    solucoes = sp.solve(equacoes, [a, b]) ## Resolve as equações para encontrar as reações de apoio

    return {a: solucoes[a], b: solucoes[b]}

def calcularReacoesFuncao(comprimento, funcao): ## Função para calcular as reações de apoio carregamentos dados por funções
    RA, RB = sp.symbols('RA RB')
    x = sp.symbols('x')
    carga = sp.lambdify(x, funcao, 'numpy') ## Função de distribuição de carga
    forca, _ = quad(carga, 0, comprimento) ## Calcula a força total aplicada na viga
    momento, _ = quad(lambda x: carga(x) * x, 0, comprimento) ## Calcula o momento total aplicado na viga
    posicao = momento / forca ## Calcula a posição da força resultante
    RB = (forca * posicao) / comprimento ## Calcula a reação em B
    RA = forca - RB ## Calcula a reação em A

    return {sp.symbols('RA'): RA, sp.symbols('RB'): RB}

def integrarFuncoes(funcao): ## Função para integrar funções
    x = sp.symbols('x')
    return sp.integrate(funcao, x)

def plotarCortante(comprimento, carregamentos, solucoes, opcao): ## Função para plotar o diagrama de esforço cortante
    x = sp.symbols('x')
    pontos = np.linspace(0, comprimento, 10000) ## Vetor  de pontos para plotagem
    cortante = np.zeros_like(pontos)

    RA = float(solucoes[sp.symbols('RA')]) ## Reação em A
    cortante += RA

    if opcao == 1:  # Função
        for carga in carregamentos: ## Loop para percorrer as cargas
            funcCortante = integrarFuncoes(carga * -1) ## Integra a função de distribuição para obter a função do esforço cortante
            cortante += sp.lambdify(x, funcCortante, 'numpy')(pontos)

    elif opcao == 2: ## Geométrico
        for carga in carregamentos: ## Loop para percorrer as cargas
            inicio = carga['inicio']
            fim = carga['fim']
            if carga['tipo'] == 1: ## Triângulo
                intensidade = carga['intensidade']
                base = fim - inicio
                for i, xi in enumerate(pontos):
                    if inicio <= xi <= fim: ## Ajuste para pontos dentro do intervalo de aplicação da carga
                        cortante[i] -= (intensidade / base) * (xi - inicio) ** 2 / 2 ## Função do triângulo para esforço cortante
                    elif xi > fim: ## Ajuste para pontos fora do intervalo de aplicação da carga
                        cortante[i] -= intensidade * (fim - inicio) / 2

            elif carga['tipo'] == 2: ## Retângulo
                intensidade = carga['intensidade']
                for i, xi in enumerate(pontos):
                    if inicio <= xi <= fim:
                        cortante[i] -= intensidade * (xi - inicio) ## Função do retângulo para esforço cortante
                    elif xi > fim:
                        cortante[i] -= intensidade * (fim - inicio)
            elif carga['tipo'] == 3: ## Trapézio
                baseMaior = carga['baseMaior']
                baseMenor = carga['baseMenor']
                altura = fim - inicio
                for i, xi in enumerate(pontos):
                    if inicio <= xi <= fim:
                        baseAtual = baseMenor + (baseMaior - baseMenor) * (xi - inicio) / altura ## Calcula a base atual do trapézio para o ponto xi
                        cortante[i] -= 0.5 * (baseAtual + baseMenor) * (xi - inicio) ## Função do trapézio para esforço cortante
                    elif xi > fim:
                        cortante[i] -= 0.5 * (baseMaior + baseMenor) * altura

    elif opcao == 3: ## Pontual
        for forca in carregamentos:
            posicao = forca['posicao']
            intensidade = forca['intensidade']
            for i, xi in enumerate(pontos):
                if xi >= posicao:
                    cortante[i] -= intensidade

    ## Configurações gerais do gráfico
    plt.plot(pontos, cortante, label='Esforço Cortante')
    plt.xlabel('Comprimento da viga (m)')
    plt.ylabel('Esforço cortante (N)')
    plt.title('Diagrama de Esforço Cortante')
    plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
    plt.grid(True)
    plt.legend()
    plt.show()

def plotarMomentoFletor(comprimento, carregamentos, solucoes, opcao): ## Função para plotar o diagrama de momento fletor
    x = sp.symbols('x')
    pontos = np.linspace(0, comprimento, 10000) ## Vetor de pontos para plotagem
    momento = np.zeros_like(pontos) ## Vetor de momentos

    RA = float(solucoes[sp.symbols('RA')])
    momento += RA * pontos

    if opcao == 1: ## Função
        for carga in carregamentos:
            funcMomento = integrarFuncoes(integrarFuncoes(carga)) ## Integra duas vezes a função de distribuição para obter a função do momento
            momento -= sp.lambdify(x, funcMomento, 'numpy')(pontos)

    elif opcao == 2: ## Cargas geométricas
        for carga in carregamentos:
            inicio = carga['inicio']
            fim = carga['fim']
            if carga['tipo'] == 1: ## Triângulo
                intensidade = carga['intensidade']
                base = fim - inicio
                for i, xi in enumerate(pontos):
                    if inicio <= xi <= fim:
                        momento[i] -= (intensidade/base) * (xi - inicio)**3 / 6 ## Função do triângulo para momento
                    elif xi > fim: ## Ajuste para pontos fora do intervalo de aplicação da carga
                        momento[i] -= intensidade * (fim - inicio)**2 / 6

            elif carga['tipo'] == 2: ## Retângulo
                intensidade = carga['intensidade']
                for i, xi in enumerate(pontos):
                    if inicio <= xi <= fim:
                        momento[i] -= intensidade * (xi - inicio)**2 / 2 ## Função do retângulo para momento
                    elif xi > fim: ## Ajuste para pontos fora do intervalo de aplicação da carga
                        momento[i] -= intensidade * (fim - inicio) * (xi - (inicio + fim) / 2)

            elif carga['tipo'] == 3: ## Trapézio
                baseMaior = carga['baseMaior']
                baseMenor = carga['baseMenor']
                altura = fim - inicio
                for i, xi in enumerate(pontos):
                    if inicio <= xi <= fim:
                        baseAtual = baseMenor + (baseMaior - baseMenor) * (xi - inicio) / altura ## Calcula a base atual do trapézio para o ponto xi
                        momento[i] -= (baseMenor + 2 * baseAtual) * (xi - inicio)**2 / 6 ## Função do trapezio para momento
                    elif xi > fim: ## Ajuste para pontos fora do intervalo de aplicação da carga
                        momento[i] -= (baseMenor + baseMaior) * altura**2 / 6 + (baseMenor + baseMaior) * altura * (xi - fim) / 2
    elif opcao == 3: ## Carga pontual
        for forca in carregamentos:
            posicao = forca['posicao']
            intensidade = forca['intensidade']
            for i, xi in enumerate(pontos):
                if xi >= posicao:
                    momento[i] -= intensidade * (xi - posicao)

    momento -= momento[-1] * (pontos / comprimento) ## Pequeno ajuste de aproximações numéricas (garante que o momento no final da viga é zero)

    ## Configurações gerais do gráfico
    plt.plot(pontos, momento, label='Momento Fletor')
    plt.xlabel('Comprimento da viga (m)')
    plt.ylabel('Momento fletor (N.m)')
    plt.title('Diagrama de Momento Fletor')
    plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
    plt.gca().invert_yaxis()
    plt.grid(True)
    plt.legend()
    plt.show()

 ## Leitura dos dados e chamadas das funções
opcao = int(input("Como é dada a distribuição de cargas?\n1-Função\n2-Formas Geométricas\n3-Carga pontual: "))
while opcao not in [1, 2, 3]:
    opcao = int(input("Opção inválida, digite novamente\n1-Função\n2-Formas Geométricas\n3-Carga pontual: "))

carregamentos = []
if opcao == 1: ## Função
    comprimento = float(input("Digite o comprimento da viga (m): "))
    funcao = input("Insira a função de distribuição (Ex: 100 + 10*x): ")
    funcaoSimpy = sp.sympify(funcao)
    carregamentos.append(funcaoSimpy)
    solucoes = calcularReacoesFuncao(comprimento, funcaoSimpy)

elif opcao == 2: ## Formas geométricas
    comprimento = float(input("Digite o comprimento da viga (m): "))
    numCarregamentos = int(input("Digite o número de carregamentos na viga: "))
    for i in range(numCarregamentos): ## Loop para ler os tipos de carregamentos
        tipo = int(input("Digite o tipo de carregamento\n1-Triângulo\n2-Retângulo\n3-Trapézio: "))
        while tipo not in [1, 2, 3]:
            tipo = int(input("Opção inválida, digite novamente\n1-Triângulo\n2-Retângulo\n3-Trapézio: "))
        inicio = float(input("Posição inicial do carregamento (m): "))
        fim = float(input("Posição final do carregamento (m): "))
        if tipo != 3: ## Não é lida a intensidade do trapézio
            intensidade = float(input("Digite a intensidade (N/m): "))

        if tipo == 1:
            base = 1

        if tipo == 3: ## Trapézio
            baseMaior = float(input("Digite a base maior do trapézio (m): "))
            baseMenor = float(input("Digite a base menor do trapézio (m): "))
            base = (baseMaior, baseMenor)
            carregamentos.append({'tipo': tipo, 'inicio': inicio, 'fim': fim, 'baseMaior': baseMaior, 'baseMenor': baseMenor})
        else: ## Triângulo ou retângulo
            carregamentos.append({'tipo': tipo, 'inicio': inicio, 'fim': fim, 'intensidade': intensidade, 'base': base})
    solucoes = calcularReacoesGeometricas(carregamentos, comprimento)

else: ## Carga pontual
    comprimento = float(input("Digite o comprimento da viga (m): "))
    numForcas = int(input("Digite o número de forças atuando na viga: "))
    for i in range(numForcas):
        posicao = float(input("Digite a posição da carga (m): "))
        intensidade = float(input("Digite a intensidade da carga (N): "))
        carregamentos.append({'posicao': posicao, 'intensidade': intensidade})
    solucoes = calcularReacoesPontual(carregamentos, comprimento)

## Imprime as reações de apoio
print("\nAs reações de apoio são:")
print(f"A = {float(solucoes[sp.symbols('RA')]):.2f} N")
print(f"B = {float(solucoes[sp.symbols('RB')]):.2f} N")

plotarCortante(comprimento, carregamentos, solucoes, opcao) ## Plota o diagrama de esforço cortante

plotarMomentoFletor(comprimento, carregamentos, solucoes, opcao) ## Plota o diagrama de momento fletor

