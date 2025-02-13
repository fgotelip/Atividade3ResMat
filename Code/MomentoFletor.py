from Carregamento import Carregamento
import sympy as sp
from Confere import eh_numero_pos,eh_123,eh_funcao
from scipy.integrate import quad
import numpy as np
import matplotlib.pyplot as plt

class MomentoFletor():
    def __init__(self,carregamentos=[]):
        self.__opcao = 0
        self.__carregamentos = []
        self.__vxs = []
        self.__mxs = []
        self.__forcasy = []
        self.__momentos = []
        self.__A = 0
        self.__B = 0
        if carregamentos != []:
            for carregamento in carregamentos:
                self.__aux_set_carregamentos(carregamento)

    def __aux_set_carregamentos(self,carregamento):
        self.__carregamentos.append(carregamento)
        self.__forcasy.append(carregamento.get_resultante())
        self.__momentos.append(carregamento.get_resultante()*carregamento.get_posicao())
        if carregamento.get_resultante2() != 0:
            self.__forcasy.append(carregamento.get_resultante2())
            self.__momentos.append(carregamento.get_resultante2()*carregamento.get_posicao2())

    def set_carregamentos(self):
        opcao = input("Como é dada a distribuição de cargas?\n1-Função\n2-Formas Geométricas\n3-Carga pontual: ")
        while not eh_123(opcao):
            opcao = input("Como é dada a distribuição de cargas?\n1-Carregamentos\n2-Função\n3-Carga pontual: ")
        self.__opcao = int(opcao)

        if self.__opcao == 1:
            num_carregamentos = input("Número de carregamentos= ")
            while not eh_numero_pos(num_carregamentos):
                num_carregamentos = input("Número de carregamentos= ")
            num_carregamentos = int(num_carregamentos)

            px2 = 0

            for i in range(num_carregamentos):
                carregamento = Carregamento()
                px2 = carregamento.parser(i+1,px2)
                self.__aux_set_carregamentos(carregamento)

        elif self.__opcao == 2:
            comprimento = input("Digite o comprimento da viga (m): ")
            while not eh_numero_pos(comprimento):
                comprimento = input("Digite o comprimento da viga (m): ")
            comprimento = float(comprimento)

            funcao = input("Insira a função de distribuição (Ex: 100 + 10*x): ")
            while not eh_funcao(funcao):
                funcao = input("Insira a função de distribuição (Ex: 100 + 10*x): ")
            funcaoSimpy = sp.sympify(funcao)

            self.__carregamentos.append(funcaoSimpy)
            self.calcularReacoesFuncao(comprimento, funcaoSimpy)

        else: ## Carga pontual
            comprimento = input("Digite o comprimento da viga (m): ")
            while not eh_numero_pos(comprimento):
                comprimento = input("Digite o comprimento da viga (m): ")
            comprimento = float(comprimento)

            numForcas = input("Digite o número de forças atuando na viga: ")
            while not eh_numero_pos(numForcas):
                numForcas = input("Digite o número de forças atuando na viga: ")
            numForcas = int(numForcas)

            for i in range(numForcas):
                posicao = input("Digite a posição da carga (m): ")
                while not eh_numero_pos(posicao,True):
                    posicao = input("Digite a posição da carga (m): ")
                posicao = float(posicao)
            
                intensidade = input("Digite a intensidade da carga (N): ")
                while not eh_numero_pos(intensidade):
                    intensidade = input("Digite a intensidade da carga (N): ")
                intensidade = float(intensidade)

                self.__carregamentos.append({'posicao': posicao, 'intensidade': intensidade})
            self.calcularReacoesPontual(comprimento)
           
    def calcularReacoesFuncao(self,comprimento, funcao): ## Função para calcular as reações de apoio carregamentos dados por funções
        RA, RB = sp.symbols('RA RB')
        x = sp.symbols('x')
        carga = sp.lambdify(x, funcao, 'numpy') ## Função de distribuição de carga
        forca, _ = quad(carga, 0, comprimento) ## Calcula a força total aplicada na viga
        momento, _ = quad(lambda x: carga(x) * x, 0, comprimento) ## Calcula o momento total aplicado na viga
        posicao = momento / forca ## Calcula a posição da força resultante
        RB = (forca * posicao) / comprimento ## Calcula a reação em B
        RA = forca - RB ## Calcula a reação em A

        self.__A = RA
        self.__B = RB

    def calcularReacoesPontual(self,comprimento): ## Função para calcular as reações de apoio para cargas pontuais
        a, b = sp.symbols('RA RB')
        somaForcas = 0
        momentos = 0
        for carregamento in self.__carregamentos: ## Loop para percorrer as forças
            posicao = carregamento['posicao']
            intensidade = carregamento['intensidade']
            somaForcas += intensidade ## Adiciona as forças
            momentos += intensidade * posicao ## Adiciona os momentos
        momentos -= b * comprimento
        equacoes = [a + b - somaForcas, momentos]
        solucoes = sp.solve(equacoes, [a, b]) ## Resolve as equações para encontrar as reações de apoio

        self.__A = solucoes[a]
        self.__B = solucoes[b]

    def __calcular_reacoes_carregamento(self):
        by = -sum(self.__momentos)/self.__carregamentos[-1].get_x2()
        self.__B = round(by,2)
        self.__forcasy.append(self.__B)

        ay = 0
        ay -= sum(self.__forcasy)
        self.__A = round(ay,2)


    def __set_esforcos(self):
        for i in range(len(self.__carregamentos)):
            if i == 0:
                vant = self.__A
                mant = 0
                v,m = self.__carregamentos[i].gerar_esforco(vant,mant)
                self.__vxs.append(v)
                self.__mxs.append(m)
            else:
                vant = self.__vxs[i-1]
                mant = self.__mxs[i-1]
                
                v,m = self.__carregamentos[i].gerar_esforco(vant,mant,self.__carregamentos[i-1].get_x1())
                self.__vxs.append(v)
                self.__mxs.append(m)

    def __aux_getMax(self,i,funcao,pontos_y,mx_ajustado):
        x = sp.symbols('x')
        if i == 0:
            p0y = funcao[i].subs(x,0)
            pontos_y.append(float(p0y))
            ajuste = 0
        else:
            ajuste = self.__carregamentos[i-1].get_x2()

        funcao_ajustada = funcao[i].subs(x,x-ajuste)
        mx_ajustado.append(funcao_ajustada)

        px = self.__carregamentos[i].get_x2()
        py = funcao_ajustada.subs(x,px)
        pontos_y.append(float(py))

        df = sp.diff(funcao_ajustada,x)
        df2 = sp.diff(df,x)

        xmax = self.__carregamentos[i].get_x2() - self.__carregamentos[i].get_x1()
        pontos_criticos = sp.solveset(df,x,domain=sp.Interval(ajuste,xmax+ajuste))

        for ponto in pontos_criticos:
            concavidade = df2.subs(x,ponto)
            if concavidade < 0:
                pontos_y.append(float(funcao_ajustada.subs(x,ponto)))

    def plotarMomentoFletor(self,comprimento): ## Função para plotar o diagrama de momento fletor
        x = sp.symbols('x')
        pontos = np.linspace(0, comprimento, 10000) ## Vetor de pontos para plotagem
        self.__mxs = np.zeros_like(pontos) ## Vetor de momentos

        RA = float(self.__A)
        self.__mxs += RA * pontos

        if self.__opcao == 2: ## Função
            for carga in self.__carregamentos:
                funcMomento = sp.integrate(x,sp.integrate(x,carga)) ## Integra duas vezes a função de distribuição para obter a função do momento
                self.__mxs -= sp.lambdify(x, funcMomento, 'numpy')(pontos)

        elif self.__opcao == 3: ## Carga pontual
            for forca in self.__carregamentos:
                posicao = forca['posicao']
                intensidade = forca['intensidade']
                for i, xi in enumerate(pontos):
                    if xi >= posicao:
                        self.__mxs[i] -= intensidade * (xi - posicao)

        self.__mxs -= self.__mxs[-1] * (pontos / comprimento) ## Pequeno ajuste de aproximações numéricas (garante que o momento no final da viga é zero)

        ## Configurações gerais do gráfico
        plt.plot(pontos, self.__mxs, label='Momento Fletor')
        plt.xlabel('Comprimento da viga (m)')
        plt.ylabel('Momento fletor (N.m)')
        plt.title('Diagrama de Momento Fletor')
        plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
        plt.gca().invert_yaxis()
        plt.grid(True)
        plt.legend()
        plt.show()

    def getMomentoMax(self):
        self.__calcular_reacoes_carregamento()
        self.__set_esforcos()
        pontos_y = []
        mx_ajustado = []
        for i in range(len(self.__carregamentos)):
            self.__aux_getMax(i,self.__mxs,pontos_y,mx_ajustado)
        return max(pontos_y)
