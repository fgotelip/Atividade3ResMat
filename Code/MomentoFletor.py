from Carregamento import Carregamento
import sympy as sp
from Confere import eh_numero_pos

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
                self.aux_set_carregamentos(carregamento)

    def __aux_set_carregamentos(self,carregamento):
        self.__carregamentos.append(carregamento)
        self.__forcasy.append(carregamento.get_resultante())
        self.__momentos.append(carregamento.get_resultante()*carregamento.get_posicao())
        if carregamento.get_resultante2() != 0:
            self.__forcasy.append(carregamento.get_resultante2())
            self.__momentos.append(carregamento.get_resultante2()*carregamento.get_posicao2())

    def set_carregamentos(self):
        num_carregamentos = input("Número de carregamentos= ")
        while not eh_numero_pos(num_carregamentos):
            num_carregamentos = input("Número de carregamentos= ")
        num_carregamentos = int(num_carregamentos)

        px2 = 0

        for i in range(num_carregamentos):
            carregamento = Carregamento()
            px2 = carregamento.parser(i+1,px2)
            self.__aux_set_carregamentos(carregamento)
           

    def __calcular_reacoes(self):
        by = -sum(self.__momentos)/self.__carregamentos[-1].get_x2()
        self.__B = round(by,2)
        self.__forcasy.append(self.__B)

        ay = 0
        ay -= sum(self.__forcasy)
        self.__A = round(ay,2)

    #atividade 2
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
        

    def getMomentoMax(self):
        self.__calcular_reacoes()
        self.__set_esforcos()
        pontos_y = []
        mx_ajustado = []
        for i in range(len(self.__carregamentos)):
            self.__aux_getMax(i,self.__mxs,pontos_y,mx_ajustado)
        return max(pontos_y)
