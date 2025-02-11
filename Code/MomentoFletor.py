from Carregamento import Carregamento
import matplotlib.pyplot as plt
import sympy as sp
import numpy as np
import Confere as c

class ReacoesDeApoio:
    def __init__(self):
        self.__carregamentos = []
        self.__vxs = []
        self.__mxs = []
        self.__forcasy = []
        self.__momentos = []
        self.__pontos_vx = []
        self.__pontos_wx = []
        self.__pontos_vy = []
        self.__pontos_wy = []
        self.__A = 0
        self.__B = 0

    def set_carregamentos(self):
        num_carregamentos = input("Número de carregamentos= ")
        while not c.eh_inteiro(num_carregamentos):
            num_carregamentos = input("Número de carregamentos= ")
        num_carregamentos = int(num_carregamentos)

        px2 = 0

        for i in range(num_carregamentos):
            carregamento = Carregamento()
            px2 = carregamento.parser(i+1,px2)
            self.__carregamentos.append(carregamento)
            self.__forcasy.append(carregamento.get_resultante())
            self.__momentos.append(carregamento.get_resultante()*carregamento.get_posicao())
            if carregamento.get_resultante2() != 0:
                self.__forcasy.append(carregamento.get_resultante2())
                self.__momentos.append(carregamento.get_resultante2()*carregamento.get_posicao2())

    def calcular_reacoes(self):
        by = -sum(self.__momentos)/self.__carregamentos[-1].get_x2()
        self.__B = round(by,2)
        self.__forcasy.append(self.__B)

        ay = 0
        ay -= sum(self.__forcasy)
        self.__A = round(ay,2)

    
    #para teste
    def set_carregamentos_teste(self,carregamentos):
        for carregamento in carregamentos:
            self.__carregamentos.append(carregamento)
            self.__forcasy.append(carregamento.get_resultante())
            self.__momentos.append(carregamento.get_resultante()*carregamento.get_posicao())
            if carregamento.get_resultante2() != 0:
                self.__forcasy.append(carregamento.get_resultante2())
                self.__momentos.append(carregamento.get_resultante2()*carregamento.get_posicao2())

    #atividade 2
    def set_esforcos(self):
        for i in range(len(self.__carregamentos)):
            if i == 0:
                vant = self.__A.get_fy()
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
        

    def plotar_parte(self,i,ax,funcao,pontos_x,pontos_y):
        x = sp.symbols('x')
        if i == 0:
            p0y = funcao[i].subs(x,0)
            pontos_x.append(0)
            pontos_y.append(float(p0y))
            ajuste = 0
        else:
            ajuste = self.__carregamentos[i-1].get_x2()

        funcao_ajustada = funcao[i].subs(x,x-ajuste)

        px = self.__carregamentos[i].get_x2()
        py = funcao_ajustada.subs(x,px)
        pontos_x.append(px)
        pontos_y.append(float(py))


        funcao_num = sp.lambdify(x,funcao_ajustada,'numpy')
        
        xmax = self.__carregamentos[i].get_x2() - self.__carregamentos[i].get_x1()
        x_vals = np.linspace(0,xmax,100) + ajuste
        f = funcao_num(x_vals)

        ax.plot(x_vals, f, color='blue')

    
    def plotar_esforco(self,funcao,pontos_x,pontos_y,f,nome_funcao):
        fig,ax = plt.subplots(figsize=(8,5))
      
        for i in range(len(self.__carregamentos)):
            self.plotar_parte(i,ax,funcao,pontos_x,pontos_y)

        ax.scatter(pontos_x, pontos_y, color='red', zorder=3)
        for i, txt in enumerate(pontos_y):
            ax.annotate(f'{txt:.2f}', (pontos_x[i], pontos_y[i]), textcoords="offset points", xytext=(0,5), ha='center', color='red')

        ax.set_xlabel('x')
        ax.set_ylabel(f'{f}(x)')
        ax.set_title(f'Diagrama de {nome_funcao}')
        ax.grid()
        if f == 'M':
            ax.invert_yaxis()
        
        plt.show()    

    def plotar_esforcos(self):
        self.plotar_esforco(self.__vxs,self.__pontos_vx,self.__pontos_wx,'V','Esforço Cortante')
        self.plotar_esforco(self.__mxs,self.__pontos_vy,self.__pontos_wy,'M','Momento Fletor')    
