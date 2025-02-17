from Carregamento import Carregamento
import sympy as sp
from Confere import eh_numero,eh_123,eh_funcao

class MomentoFletor():
    def __init__(self,carregamentos=[]):
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
        num_carregamentos = input("Número de carregamentos= ")
        while not eh_numero(num_carregamentos):
            num_carregamentos = input("Número de carregamentos= ")
        num_carregamentos = int(num_carregamentos)
        
        x2Ant = 0
        for i in range(num_carregamentos):
            print("Vamos definir o carregamento", i, "(cargas em N/m e tamanho da barra em m):")
            print("tamanho da barra = 0 - define carga pontual entre carregamentos")
            
            x1 = x2Ant

            tam = input("Tamanho da barra = ")
            while not eh_numero(tam,True):
                tam = input("Tamanho da barra =  ")
            tam = float(tam)

            x2=x1+tam
            x2Ant = x2

            opcao = input("Como é dada a distribuição de cargas?\n1-Carga Distribuida\n2-Carga Pontual\n3-Função: ")
            while not eh_123(opcao):
                opcao = input("Como é dada a distribuição de cargas?\n1-Carregamentos\n2-Carga Pontual\n3-Função: ")
            self.__opcao = int(opcao)

            if self.__opcao == 1:
                carga1 = input("Carga 1 = ")
                while not eh_numero(carga1,True):
                    carga1 = input("Carga 1 =   ")
                carga1 = float(carga1)

                carga2 = input("Carga 2 =  ")
                while not eh_numero(carga2,True):
                    carga2 = input("Carga 2 =  ")
                carga2 = float(carga2)
                self.__aux_set_carregamentos(Carregamento(x1,x2,carga1,self.__opcao,carga2))

            elif self.__opcao == 2:
                carga = input("Carga = ")
                while not eh_numero(carga):
                    carga1 = input("Carga =  ")
                carga = float(carga)

                if tam != 0:
                    pos = input("Posição da carga = ")
                    while not eh_numero(pos,True):
                        pos = input("Posição da carga =  ")
                else:
                    pos = 0
                self.__aux_set_carregamentos(Carregamento(x1,x2,carga,self.__opcao,0,pos))

            elif self.__opcao == 3:
                funcao = input("Insira a função de distribuição (Ex: 100 + 10*x): ")
                while not eh_funcao(funcao):
                    funcao = input("Insira a função de distribuição (Ex: 100 + 10*x): ")
                funcaoSimpy = sp.sympify(funcao)
                self.__aux_set_carregamentos(Carregamento(x1,x2,funcaoSimpy,self.__opcao))
            self.__calcularReacoes()

    def __calcularReacoes(self):
        by = -sum(self.__momentos)/self.__carregamentos[-1].get_x2()
        self.__B = round(by,2)
        self.__forcasy.append(self.__B)

        ay = 0
        ay -= sum(self.__forcasy)
        self.__A = round(ay,2)

    def __append_esforcos(self,i):
        self.__vxs.append(self.__carregamentos[i].get_v())
        self.__mxs.append(self.__carregamentos[i].get_m())
        self.__idiagramas+=1
        if self.__carregamentos[i].get_tipo() == 2:
            self.__vxs.append(self.__carregamentos[i].get_v2())
            self.__mxs.append(self.__carregamentos[i].get_m2())
            self.__idiagramas+=1


    def __set_esforcos(self):
        self.__idiagramas = -1
        for i in range(len(self.__carregamentos)):
            if i == 0:
                vant = self.__A
                mant = 0
                self.__carregamentos[i].geraEsforcos(vant,mant)
                self.__append_esforcos(i)
            else:
                vant = self.__vxs[self.__idiagramas]
                mant = self.__mxs[self.__idiagramas]

                if self.__carregamentos[i-1].get_tipo() == 1:
                    self.__carregamentos[i].geraEsforcos(vant,mant,self.__carregamentos[i-1].get_x1())

                elif self.__carregamentos[i-1].get_tipo() == 2:
                    self.__carregamentos[i].geraEsforcos(vant,mant,self.__carregamentos[i-1].get_posicao())
                

                self.__append_esforcos(i)

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

    def getMomentoMax(self):
        self.__calcularReacoes()
        self.__set_esforcos()
        pontos_y = []
        mx_ajustado = []
        for i in range(len(self.__carregamentos)):
            self.__aux_getMax(i,self.__mxs,pontos_y,mx_ajustado)
        return max(pontos_y)

