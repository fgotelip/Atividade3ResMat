from Carregamento import Carregamento
from Apoio import Apoio
import sympy as sp
from Confere import eh_numero,eh_123,eh_funcao,esta_no_intervalo,eh_sim_nao

class MomentoFletor():
    def __init__(self,carregamentos=[],apoios=[]):
        self.__apoios = (0,0)
        self.__carregamentos = []
        self.__vxs = []
        self.__mxs = []
        self.__forcasy = []
        self.__momentos = []
        
        if apoios != []:
            self.__apoios = apoios

        if carregamentos != []:
            self.__carregamentos.append(Carregamento())
            for carregamento in carregamentos:
                self.__aux_set_carregamentos(carregamento)
      

    def __aux_set_carregamentos(self,carregamento):
        dist = carregamento.get_posicao() - self.__apoios[0].get_pos()
        
        self.__carregamentos.append(carregamento)
        self.__forcasy.append(carregamento.get_resultante())
        self.__momentos.append(carregamento.get_resultante()*dist)
        if carregamento.get_resultante2() != 0:
            dist2 = carregamento.get_posicao2() - self.__apoios[0].get_pos()
            self.__forcasy.append(carregamento.get_resultante2())
            self.__momentos.append(carregamento.get_resultante2()*dist2)

    def __define_apoios(self,pos,antes_depois):
        if self.__apoios[0] == 0 or self.__apoios[1] == 0:

            sim_nao = input("Existe um apoio "+antes_depois+" da viga? (s/n): ")
            while not eh_sim_nao(sim_nao):
                sim_nao = input("Existe um apoio"+antes_depois+" da viga? (s/n): ")
            if sim_nao.lower() == 's':
                
                if self.__apoios[0] == 0 and self.__apoios[1] == 0:
                    tipo = input("Escolha o tipo de apoio:\n1-2o Gênero\n2-1o Gênero")
                    while not eh_123(tipo,True):
                        tipo = input("Escolha o tipo de apoio:\n1-2o Gênero\n2-1o Gênero")
                    tipo = int(tipo)
                    if tipo == 1:
                        self.__apoios[0]=(Apoio(pos,tipo))
                    else:
                        self.__apoios[1]=(Apoio(pos,tipo))

                elif self.__apoios[0] == 0:
                    print("Apoio de 2o gênero definido.")
                    self.__apoios[0]=(Apoio(pos,2))

                elif self.__apoios[1] == 0:
                    print("Apoio de 1o gênero definido.")
                    self.__apoios[1]=(Apoio(pos,1))       

    def set_carregamentos(self):
        print("Escolha o tipo de viga:\n1-Biapoiada Simples\n2-Biapoiada com balanço\n3-Engastada Livre")
        tipo = input("Tipo de viga: ")
        while not eh_123(tipo):
            tipo = input("Tipo de viga: ")
        tipo_viga = int(tipo)

        if tipo_viga == 3:
            self.__apoios[0] = (Apoio(0,3))

        num_carregamentos = input("Número de carregamentos= ")
        while not eh_numero(num_carregamentos):
            num_carregamentos = input("Número de carregamentos= ")
        num_carregamentos = int(num_carregamentos)
        
        x2Ant = 0

        self.__carregamentos.append(Carregamento())

        for i in range(num_carregamentos):
            if tipo_viga == 2:
                self.__define_apoios(x2Ant,"antes")
            
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
                    while not esta_no_intervalo(pos,x1,x2):
                        pos = input("Posição da carga =  ")
                else:
                    pos = 0
                self.__aux_set_carregamentos(Carregamento(x1,x2,carga,self.__opcao,0,pos))

            elif self.__opcao == 3:
                funcao = input("Insira a função de distribuição (Ex: 100 + 10*x): ")
                while not eh_funcao(funcao):
                    funcao = input("Insira a função de distribuição (Ex: 100 + 10*x): ")
               
                self.__aux_set_carregamentos(Carregamento(x1,x2,funcao,self.__opcao))

            if tipo_viga == 2:
                self.__define_apoios(x2,"depois")
        
        if tipo_viga == 1:
            self.__apoios[0]=(Apoio(0,2))
            self.__apoios[1]=(Apoio(x2,1))


    def __calcularReacoes(self):
        if self.__apoios[1] != 0:
            dist = self.__apoios[1].get_pos() - self.__apoios[0].get_pos()
            by = -sum(self.__momentos)/dist
            self.__apoios[1].set_reacao(by)
            self.__forcasy.append(self.__apoios[1].get_reacao())
        else:
            self.__apoios[0].set_momento(-sum(self.__momentos))

        ay = 0
        ay -= sum(self.__forcasy)
        self.__apoios[0].set_reacao(ay)

    def __append_esforcos(self,i):
        self.__vxs.append(self.__carregamentos[i].get_v())
        self.__mxs.append(self.__carregamentos[i].get_m())
        self.__idiagramas+=1
        if self.__carregamentos[i].get_tipo() == 2:
            self.__vxs.append(self.__carregamentos[i].get_v2())
            self.__mxs.append(self.__carregamentos[i].get_m2())
            self.__idiagramas+=1


    def __set_esforcos(self):
        self.__idiagramas = 0
        
        self.__vxs.append(0)
        self.__mxs.append(0)
        
        for i in range(1,len(self.__carregamentos)):
            temApoio = False
            for apoio in self.__apoios:
                if apoio != 0:
                    if self.__carregamentos[i].get_x1() == apoio.get_pos():
                        temApoio = True
                        vant = self.__vxs[self.__idiagramas] + apoio.get_reacao()
                        mant = self.__mxs[self.__idiagramas] - apoio.get_momento()

            if not temApoio:
                vant = self.__vxs[self.__idiagramas]
                mant = self.__mxs[self.__idiagramas]

            if self.__carregamentos[i-1].get_tipo() == 2:
                self.__carregamentos[i].geraEsforcos(vant,mant,self.__carregamentos[i-1].get_posicao())
            else:
                self.__carregamentos[i].geraEsforcos(vant,mant,self.__carregamentos[i-1].get_x1())
                

            self.__append_esforcos(i)

    def getMomentoMax(self):
        self.__calcularReacoes()
        self.__set_esforcos()
        MomentoMax = []
        for carregamento in self.__carregamentos:
            carregamento.getMomentoMax(MomentoMax)
        return max(MomentoMax,key=abs)

