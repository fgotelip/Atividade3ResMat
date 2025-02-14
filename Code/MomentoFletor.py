from Carregamento import Carregamento
import sympy as sp
from Confere import eh_numero,eh_123,eh_funcao
from scipy.integrate import quad
import numpy as np
import matplotlib.pyplot as plt

class MomentoFletor():
    def __init__(self,carregamentos=[],opcao=0,comprimento=0):
        self.__opcao = opcao
        self.__comprimento = comprimento
        self.__carregamentos = []
        self.__vxs = []
        self.__mxs = []
        self.__forcasy = []
        self.__momentos = []
        self.__A = 0
        self.__B = 0
        if self.__opcao == 1:
            for carregamento in carregamentos:
                self.__aux_set_carregamentos(carregamento)
        elif self.__opcao == 2:
            self.__carregamentos = sp.sympify(carregamentos)
            self.calcularReacoesFuncao()
        elif self.__opcao == 3:
            self.__carregamentos = carregamentos
            self.calcularReacoesPontual()

    def get_opcao(self):
        return self.__opcao

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
            while not eh_numero(num_carregamentos):
                num_carregamentos = input("Número de carregamentos= ")
            num_carregamentos = int(num_carregamentos)

            px2 = 0

            for i in range(num_carregamentos):
                carregamento = Carregamento()
                px2 = carregamento.parser(i+1,px2)
                self.__aux_set_carregamentos(carregamento)

        elif self.__opcao == 2:
            self.__comprimento = input("Digite o comprimento da viga (m): ")
            while not eh_numero(self.__comprimento):
                self.__comprimento = input("Digite o comprimento da viga (m): ")
            self.__comprimento = float(self.__comprimento)

            funcao = input("Insira a função de distribuição (Ex: 100 + 10*x): ")
            while not eh_funcao(funcao):
                funcao = input("Insira a função de distribuição (Ex: 100 + 10*x): ")
            funcaoSimpy = sp.sympify(funcao)

            self.__carregamentos = funcaoSimpy
            self.calcularReacoesFuncao()

        else: ## Carga pontual
            self.__comprimento = input("Digite o comprimento da viga (m): ")
            while not eh_numero(self.__comprimento):
                self.__comprimento = input("Digite o comprimento da viga (m): ")
            self.__comprimento = float(self.__comprimento)

            numForcas = input("Digite o número de forças atuando na viga: ")
            while not eh_numero(numForcas):
                numForcas = input("Digite o número de forças atuando na viga: ")
            numForcas = int(numForcas)

            for i in range(numForcas):
                posicao = input("Digite a posição da carga (m): ")
                while not eh_numero(posicao,True):
                    posicao = input("Digite a posição da carga (m): ")
                posicao = float(posicao)
            
                intensidade = input("Digite a intensidade da carga (N): ")
                while not eh_numero(intensidade):
                    intensidade = input("Digite a intensidade da carga (N): ")
                intensidade = float(intensidade)

                self.__carregamentos.append((posicao,intensidade))
            self.calcularReacoesPontual()
           
    def calcularReacoesFuncao(self): ## Função para calcular as reações de apoio carregamentos dados por funções
        RA, RB = sp.symbols('RA RB')
        x = sp.symbols('x')
        carga = sp.lambdify(x, self.__carregamentos, 'numpy') ## Função de distribuição de carga
        forca, _ = quad(carga, 0, self.__comprimento) ## Calcula a força total aplicada na viga
        momento, _ = quad(lambda x: carga(x) * x, 0, self.__comprimento) ## Calcula o momento total aplicado na viga
        posicao = momento / forca ## Calcula a posição da força resultante
        RB = (forca * posicao) / self.__comprimento ## Calcula a reação em B
        RA = forca - RB ## Calcula a reação em A

        self.__A = RA
        self.__B = RB

    def calcularReacoesPontual(self): ## Função para calcular as reações de apoio para cargas pontuais
        a, b = sp.symbols('RA RB')
        somaForcas = 0
        momentos = 0
        for carregamento in self.__carregamentos: ## Loop para percorrer as forças
            posicao = carregamento[0]
            intensidade = carregamento[1]
            somaForcas += intensidade ## Adiciona as forças
            momentos += intensidade * posicao ## Adiciona os momentos
        momentos -= b * self.__comprimento
        equacoes = [a + b - somaForcas, momentos]
        solucoes = sp.solve(equacoes, [a, b]) ## Resolve as equações para encontrar as reações de apoio

        self.__A = solucoes[a]
        self.__B = solucoes[b]

    def __calcularReacoesCarregamento(self):
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

    def __aux_getMax_carregamento(self,i,funcao,pontos_y,mx_ajustado):
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

    def getMomentoMax_Funcao_Pontual(self): ## Função para plotar o diagrama de momento fletor
        x = sp.symbols('x')
        pontos = np.linspace(0, self.__comprimento, 10000) ## Vetor de pontos para plotagem
        self.__mxs = np.zeros_like(pontos) ## Vetor de momentos

        RA = float(self.__A)
        self.__mxs += RA * pontos

        if self.__opcao == 2: ## Função
            funcMomento = sp.integrate((sp.integrate(self.__carregamentos,x)),x) ## Integra duas vezes a função de distribuição para obter a função do momento
            self.__mxs -= sp.lambdify(x, funcMomento, 'numpy')(pontos)

        elif self.__opcao == 3: ## Carga pontual
            for forca in self.__carregamentos:
                posicao = forca[0]
                intensidade = forca[1]
                for i, xi in enumerate(pontos):
                    if xi >= posicao:
                        self.__mxs[i] -= intensidade * (xi - posicao)
        '''
        ## Configurações gerais do gráfico
        plt.plot(pontos, self.__mxs, label='Momento Fletor')
        plt.xlabel('comprimento da viga (m)')
        plt.ylabel('Momento fletor (N.m)')
        plt.title('Diagrama de Momento Fletor')
        plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
        plt.gca().invert_yaxis()
        plt.grid(True)
        plt.legend()
        plt.show()
        '''
        
        return max(self.__mxs)

    def getMomentoMax_carregamento(self):
        self.__calcularReacoesCarregamento()
        self.__set_esforcos()
        pontos_y = []
        mx_ajustado = []
        for i in range(len(self.__carregamentos)):
            self.__aux_getMax_carregamento(i,self.__mxs,pontos_y,mx_ajustado)
        return max(pontos_y)
    
    def getMomentoMax(self):
        if self.__opcao == 1:
            return self.getMomentoMax_carregamento()
        else:
            return self.getMomentoMax_Funcao_Pontual()

