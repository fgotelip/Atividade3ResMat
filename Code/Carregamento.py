import sympy as sp

class Carregamento():
    def __init__(self, x1=0, x2=0,carga=0,tipo=0,carga2=0,pos=0):
        self.__x1 = x1
        self.__x2 = x2
        self.__carga = carga
        self.__tipo = tipo
        self.__carga2 = carga2
        self.__pos = pos
        self.__tam = x2-x1
        self.__x = sp.symbols('x')
        self.__posicao = 0
        self.__posicao2 = 0
        self.__resultante = 0
        self.__resultante2 = 0
        self.__w = 0
        self.__v = 0
        self.__v2 = 0
        self.__m = 0
        self.__m2 = 0
        

        if self.__tipo == 1:
            if self.__carga == self.__carga2:
                self.__posicao = (self.__x1 + self.__x2)/2
                self.__resultante = -self.__tam*self.__carga

                self.__w = self.__carga

            elif self.__carga == 0:
                self.__posicao = self.__x1+(self.__tam*2/3)
                self.__resultante = -self.__tam*self.__carga2/2

                self.__w = (self.__carga2/self.__tam)*self.__x

            elif self.__carga2 == 0:
                self.__posicao = self.__x1+(self.__tam*1/3)
                self.__resultante = -self.__tam*self.__carga/2

                self.__w = self.__carga - (self.__carga/self.__tam)*self.__x

            elif self.__carga > self.__carga2:
                self.__posicao = (self.__x1 + self.__x2)/2
                self.__resultante = -self.__tam*self.__carga2
                self.__posicao2 = self.__x1+(self.__tam*1/3)
                self.__resultante2 = -self.__tam*(self.__carga-self.__carga2)/2

                self.__w = -((self.__carga-self.__carga2)/self.__tam)*self.__x + self.__carga

            elif self.__carga < self.__carga2:
                self.__posicao = (self.__x1 + self.__x2)/2
                self.__resultante = -self.__tam*self.__carga
                self.__posicao2 = self.__x1+(self.__tam*2/3)
                self.__resultante2 = -self.__tam*(self.__carga2-self.__carga)/2

                self.__w = ((self.__carga2-self.__carga)/self.__tam)*self.__x + self.__carga

        elif self.__tipo == 2:
            self.__posicao = self.__x1+pos
            self.__resultante = -self.__carga

        elif self.__tipo == 3:
            self.__w = sp.sympify(self.__carga)
            
            forca = sp.integrate(self.__w,(self.__x,0,self.__tam)) ## Calcula a força total aplicada na viga
            self.__resultante = -float(forca)
            momento = sp.integrate(self.__w * self.__x,(self.__x, 0, self.__tam))
            posicao = float(momento / forca) ## Calcula a posição da força resultante
            self.__posicao = self.__x1 + posicao

    def geraEsforcos(self,vant,mant,xant=0):
        tamAnt = self.__x1 - xant
        self.__gera_vx(vant,tamAnt)
        self.__gera_mx(mant,tamAnt)
        print(f"m1 ={self.__m}")
        if self.__tipo == 2:
            print(f"m2 ={self.__m2}")
    
    def __gera_vx(self,vant,tamAnt):
        if isinstance(vant,sp.Basic):
            vant = vant.subs(self.__x,tamAnt)
   
        if self.__tipo == 2: 
            self.__v = vant
            self.__v2 = vant + self.__resultante  
        else:
            self.__v = sp.integrate(-self.__w,self.__x) + vant

    def __gera_mx(self,mant,tamAnt):
        if isinstance(mant,sp.Basic):
            mant = mant.subs(self.__x,tamAnt)
        
        self.__m = sp.integrate(self.__v,self.__x) + mant
        if self.__tipo == 2:
            mant2 = self.__m.subs(self.__x,self.__pos)
            self.__m2 = sp.integrate(self.__v2,self.__x) + mant2

    def getMomentoMax(self,MomentoMax):
        if isinstance(self.__m,sp.Basic):
            if self.__tipo == 2:
                MomentoMax.append(float(self.__m.subs(self.__x,0)))
                self.setPontoMaxMomento(self.__m,MomentoMax,self.__pos)
                MomentoMax.append(float(self.__m.subs(self.__x,self.__pos)))
                self.setPontoMaxMomento(self.__m2,MomentoMax,self.__tam - self.__pos)
                MomentoMax.append(float(self.__m2.subs(self.__x,self.__tam - self.__pos)))
            else:
                MomentoMax.append(float(self.__m.subs(self.__x,0)))
                self.setPontoMaxMomento(self.__m,MomentoMax,self.__tam)
                MomentoMax.append(float(self.__m.subs(self.__x,self.__tam)))

        
          

    def setPontoMaxMomento(self,funcao,MomentoMax,tam):
        df = sp.diff(funcao,self.__x)
        df2 = sp.diff(df,self.__x)

        pontos_criticos = sp.solveset(df,self.__x,domain=sp.Interval(0,tam))

        if not isinstance(pontos_criticos,sp.Interval):
            for ponto in pontos_criticos:
                concavidade = df2.subs(self.__x,ponto)
                if concavidade < 0 or concavidade > 0:
                    print(f"X momento máximo = {ponto}")
                    MomentoMax.append(float(self.__m.subs(self.__x,ponto)))    

    def get_tipo(self):
        return self.__tipo

    def get_posicao(self):
        return self.__posicao

    def get_posicao2(self):
        return self.__posicao2

    def get_resultante(self):
        return self.__resultante

    def get_resultante2(self):
        return self.__resultante2

    def get_x1(self):
        return self.__x1

    def get_x2(self):
        return self.__x2
    
    def get_v(self):
        return self.__v
    
    def get_v2(self):
        return self.__v2
    
    def get_m(self):
        return self.__m
    
    def get_m2(self):
        return self.__m2













