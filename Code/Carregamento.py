import sympy as sp

## Classe para definir carregamentos e calcular suas informações
class Carregamento():
    def __init__(self, x1=0, x2=0,carga=0,tipo=0,carga2=0,pos=0): ## Construtor da classe
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
        self.__momento = 0
        self.__w = 0
        self.__v = 0
        self.__v2 = 0
        self.__m = 0
        self.__m2 = 0
        
        if self.__tipo == 1: ## Carregamento distribuído
            if self.__carga == self.__carga2: ## Retângulo
                self.__posicao = (self.__x1 + self.__x2)/2 ## Posição da força resultante
                self.__resultante = -self.__tam*self.__carga ## Valor da força resultante

                self.__w = self.__carga ## Valor da carga

            elif self.__carga == 0: ## Triângulo Retângulo crescente
                self.__posicao = self.__x1+(self.__tam*2/3) ## Posição da força resultante
                self.__resultante = -self.__tam*self.__carga2/2 ## Valor da força resultante

                self.__w = (self.__carga2/self.__tam)*self.__x ## Valor da carga

            elif self.__carga2 == 0: ## Triângulo Retângulo decrescente
                self.__posicao = self.__x1+(self.__tam*1/3) ## Posição da força resultante
                self.__resultante = -self.__tam*self.__carga/2 ## Valor da força resultante

                self.__w = self.__carga - (self.__carga/self.__tam)*self.__x

            elif self.__carga > self.__carga2: ## Trapézio decrescente
                self.__posicao = (self.__x1 + self.__x2)/2 ## Posição resultante retângulo
                self.__resultante = -self.__tam*self.__carga2 ## Valor resultante retângulo
                self.__posicao2 = self.__x1+(self.__tam*1/3) ## Posição resultante triângulo
                self.__resultante2 = -self.__tam*(self.__carga-self.__carga2)/2 ## Valor resultante triângulo

                self.__w = -((self.__carga-self.__carga2)/self.__tam)*self.__x + self.__carga ## Valor da carga

            elif self.__carga < self.__carga2: ## Trapézio crescente
                self.__posicao = (self.__x1 + self.__x2)/2 ## Posição resultante retângulo
                self.__resultante = -self.__tam*self.__carga ## valor resultante retângulo
                self.__posicao2 = self.__x1+(self.__tam*2/3) ## Posição resultante triângulo 
                self.__resultante2 = -self.__tam*(self.__carga2-self.__carga)/2 ## Valor resultante triângulo

                self.__w = ((self.__carga2-self.__carga)/self.__tam)*self.__x + self.__carga ## Valor da carga

        elif self.__tipo == 2: ## Carga pontual
            self.__posicao = self.__x1+pos ## Posição da força resultante
            self.__resultante = -self.__carga ## Valor da força resultante

        elif self.__tipo == 3: ## Carregamento por f(X)
            self.__w = sp.sympify(self.__carga)
            forca = sp.integrate(self.__w,(self.__x,0,self.__tam)) ## Valor força resultante
            self.__resultante = -float(forca)
            momento = sp.integrate(self.__w * self.__x,(self.__x, 0, self.__tam)) ## Momento resultante
            posicao = float(momento / forca) ## Posição força resultante
            self.__posicao = self.__x1 + posicao ## Posição resultante em relação a viga toda
        
        elif self.__tipo == 4: ## Carga momento
            self.__posicao = self.__x1+pos ## Posição do momento
            self.__momento = -self.__carga ## Valor do momento

    def geraEsforcos(self,vant,mant,xant=0): ## Função para gerar os esforços na barra
        tamAnt = self.__x1 - xant 
        self.__gera_vx(vant,tamAnt) ## Chama para o calculo do cortante 
        self.__gera_mx(mant,tamAnt) ## Chama para o calculo do fletor
        print(f"m1 ={self.__m}")
        if self.__tipo == 2 or self.__tipo == 4:
            print(f"m2 ={self.__m2}")
    
    def __gera_vx(self,vant,tamAnt): ## Função para calcular o cortante
        
        if isinstance(vant,sp.Basic): ## Confere se é função
            vant = vant.subs(self.__x,tamAnt) ## Cortante anterior

        if self.__tipo == 2 or self.__tipo == 4: ## Carregamento pontual
            self.__v = vant
            if self.__tipo == 2:
                self.__v2 = vant + self.__resultante  

        else: ## Carregamento distribuído e f(X)
            self.__v = sp.integrate(-self.__w,self.__x) + vant

    def __gera_mx(self,mant,tamAnt): ## Função para calcular o fletor
        if isinstance(mant,sp.Basic): ## Confere se é função
            mant = mant.subs(self.__x,tamAnt)
        
        self.__m = sp.integrate(self.__v,self.__x) + mant
        if self.__tipo == 2: ## Carregamento pontual
            mant2 = self.__m.subs(self.__x,self.__pos)
            self.__m2 = sp.integrate(self.__v2,self.__x) + mant2

        elif self.__tipo == 4: ## Carga Momento
            mant2 = self.__m.subs(self.__x,self.__pos)
            termo_independente = self.__m.subs(self.__x,0) ## Termo independente da função
            self.__m2 = self.__m.subs(termo_independente,mant2+self.__momento) ## Calcula o segundo fletor subtraindo o termo independente

    def getMomentoMax(self,MomentoMax): ## Funçãp para calcular o momento máximo
        if isinstance(self.__m,sp.Basic): ## Confere se é função 
            if self.__tipo == 2 or self.__tipo == 4: ## Carga pontual e Carga Momento
                MomentoMax.append(float(self.__m.subs(self.__x,0)))
                self.setPontoMaxMomento(self.__m,MomentoMax,self.__pos)
                MomentoMax.append(float(self.__m.subs(self.__x,self.__pos)))
                self.setPontoMaxMomento(self.__m2,MomentoMax,self.__tam - self.__pos)
                MomentoMax.append(float(self.__m2.subs(self.__x,self.__tam - self.__pos)))
            else: ## Carregamento distribuído e f(X)
                MomentoMax.append(float(self.__m.subs(self.__x,0)))
                self.setPontoMaxMomento(self.__m,MomentoMax,self.__tam)
                MomentoMax.append(float(self.__m.subs(self.__x,self.__tam)))
        else: ## Função constante
            MomentoMax.append(self.__m)
            if self.__tipo == 2 or self.__tipo == 4:
                MomentoMax.append(self.__m2)        

    def setPontoMaxMomento(self,funcao,MomentoMax,tam): ## Função para definir a seção mais solicitada da viga
        df = sp.diff(funcao,self.__x)
        df2 = sp.diff(df,self.__x)

        pontos_criticos = sp.solveset(df,self.__x,domain=sp.Interval(0,tam)) ## Pontos onde a derivada é 0

        if not isinstance(pontos_criticos,sp.Interval): ## Confere se não é função
            for ponto in pontos_criticos: ## Percorre o vetor de pontos críticos
                concavidade = df2.subs(self.__x,ponto)
                if concavidade < 0 or concavidade > 0: ## Ponto de máximo ou mínimo
                    print(f"X momento máximo = {ponto}")
                    MomentoMax.append(float(self.__m.subs(self.__x,ponto)))    

    def get_tipo(self): ## Retornar o tipo de carregamento
        return self.__tipo

    def get_posicao(self): ## Retornar posição da resultante
        return self.__posicao
    
    def get_posicao2(self): ## Retornar posição da segunda resultante(Trapézios)
        return self.__posicao2
 
    def get_resultante(self): ## Retornar a resultante
        return self.__resultante

    def get_resultante2(self): ## Retornar a segunda resultante (Trapézios)
        return self.__resultante2
    
    def get_momento(self):
        return -self.__momento

    def get_x1(self): ## Retorna o início do carregamento
        return self.__x1

    def get_x2(self): ## Retorna o fim do carregamento
        return self.__x2
    
    def get_v(self): ## Retorna o cortante
        return self.__v
    
    def get_v2(self): ## Retorna o segundo cortante
        return self.__v2
    
    def get_m(self): ## Retorna o fletor 
        return self.__m
    
    def get_m2(self): ## Retorna o segundo fletor
        return self.__m2













