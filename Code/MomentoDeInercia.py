import matplotlib.pyplot as plt
import Confere as c
from Confere import eh_numero, eh_sim_nao, confere_coordenadas
import re
from Retangulo import Retangulo

class MomentoDeInercia:
    def __init__(self, retangulos=[], buracos=[]): ## Construtor da classe
        self.__retangulos = retangulos
        self.__buracos = buracos
        self.__Xp = 0
        self.__Yp = 0
        self.__Ixx = 0
        self.__Iyy = 0
        self.__Ixy = 0

    def getYmin(self):
        return self.__Yp - min([ret.getYi() for ret in self.__retangulos])
    
    def getYmax(self):
        return max([ret.getYf() for ret in self.__retangulos]) - self.__Yp
    
    def getIxx(self):
        return self.__Ixx

    def setRetangulos_user(self): ## função para ler as informações do problema
        numRetangulos = input("Digite o número de retângulos na figura: ")
        while not eh_numero(numRetangulos):
            numRetangulos = input("Digite o número de retângulos na figura: ")
        numRetangulos = int(numRetangulos)

        for i in range(numRetangulos):  ## Loop para inserir coordenadas dos retângulos cheios
            entrada = input(f"Digite as coordenadas do retângulo {i+1} (X-inicial, X-final, Y-inicial, Y-final): ")
            while not confere_coordenadas(entrada):
                entrada = input(f"Digite as coordenadas do retângulo {i+1} (X-inicial, X-final, Y-inicial, Y-final): ")
            numeros = re.findall(r"-?\d+(?:\.\d+)?", entrada)
            xi, xf, yi, yf = map(float, numeros)
            retangulo = Retangulo(xi, xf, yi, yf)
            self.__retangulos.append(retangulo)

        figOca = input("Existe algum buraco na estrutura? (s/n): ")
        while not eh_sim_nao(figOca):
            figOca = input("Existe algum buraco na estrutura?")
        if figOca.lower() == 's':
            print("oca")
            numBuracos = input("Digite o número de buracos na figura: ")
            while not eh_numero(numBuracos):
                numBuracos = input("Digite o número de buracos na figura: ")
            numBuracos = int(numBuracos)

            for i in range(numBuracos): ## Loop para inserir as coordenadas dos buracos
                entrada = input(f"Digite as coordenadas do buraco {i+1} (X-inicial, X-final, Y-inicial, Y-final): ")
                xi, xf, yi, yf = map(float, entrada.split())
                buraco = Retangulo(xi, xf, yi, yf)
                self.__buracos.append(buraco)


    def __calculaCentroide(self): ## função para calcular o centróide da figura
            areaPreenchida=0
            areaVazada=0

            for retangulo in self.__retangulos: ## Loop para percorrer o vetor de retângulos
                area , xp, yp = retangulo.getCentroide() ## Chama a função para retornar a área e o centróide do retângulo
                areaPreenchida+=area ## Adiciona a área do retângulo na contribuição global
                self.__Xp+=xp ## Adiciona a coordenada X do centróide do retângulo na contribuição global
                self.__Yp+=yp ## Adiciona a coordenada Y do centróide do retângulo na contribuição global
            if self.__buracos: ## Caso seja uma figura vazada
                for buraco in self.__buracos: ## Loop para percorrer o vetor de buracos
                    area , xp, yp = buraco.getCentroide() ## Chama a função para retornar a área e o centróide do buraco
                    areaVazada+=area ## Adiciona a área do buraco na contribuição global
                    self.__Xp-=xp ## Retira a coordenada X do centróide do buraco na contribuição global
                    self.__Yp-=yp ## Retira a coordenada Y do centróide do buraco na contribuição global
            self.__Xp/=(areaPreenchida-areaVazada) ## Posição X do centróide da figura
            self.__Yp/=(areaPreenchida-areaVazada) ## Posição Y do centróide da figura


    def __calcularMomentoDeInercia(self): ## Função para calcular o momento de inércia da figura
        dX=0 ## Inicializa a distancia X entre o centróide do retângulo e da figura
        dY=0 ## Inicializa a distancia Y entre o centróide do retângulo e da figura
        for retangulo in self.__retangulos: ## Loop para percorrer o vetor de retângulos
            area, x, y, IxxLocal, IyyLocal, IxyLocal = retangulo.getMomentoDeInercia() ## Chama a função para retornar o momento de inércia do retângulo
            dX = x - self.__Xp ## Distância em X entre o centróide do retângulo analisado e o da figura
            dY = y - self.__Yp ## Distância em Y entre o centróide do retângulo analisado e o da figura
            self.__Ixx += IxxLocal + area * dY**2 ## Momento de inércia em X final
            self.__Iyy += IyyLocal + area * dX**2 ## Momento de inércia em Y final
            self.__Ixy += IxyLocal + area * dX * dY ## Produto de inércia final
        if self.__buracos: ## Apenas se existir buracos na figura
            for buraco in self.__buracos: ## Loop para percorrer o vetor de buracos
                x, y, IxxLocal, IyyLocal, IxyLocal = buraco.getMomentoDeInercia() ## Chama a função para retornar o momento de inércia do buraco
                dX = x - self.__Xp 
                dY = y - self.__Yp 
                self.__Ixx -= IxxLocal + area * dY**2 ## Subtrái o momento de inércia em X do buraco
                self.__Iyy -= IyyLocal + area * dX**2 ## Subtrái o momento de inércia em Y do buraco
                self.__Ixy -= IxyLocal + area * dX * dY ## Subtrái o produto de inércia do buraco

    def calcula(self):
        self.__calculaCentroide()
        self.__calcularMomentoDeInercia()

    def exibirResultados(self): ## Função para exibir os resultados
        self.calcula()
        print(f"O centroide da figura é: ({self.__Xp:.2f},{self.__Yp:.2f})mm")
        print(f"Momento de inércia em relação ao eixo X: {self.__Ixx:.2f} mm⁴")
        print(f"Momento de inércia em relação ao eixo Y: {self.__Iyy:.2f} mm⁴")
        print(f"Produto de inércia Ixy: {self.__Ixy:.2f} mm⁴\n")

    def plotarfigura(self): ## Função para plotar o problema
        fig, ax = plt.subplots()
        for retangulo in self.__retangulos: ## Plota os retângulos cheios
            base, altura, xi, yi = retangulo.getDimensoes()
            ax.add_patch(plt.Rectangle((xi, yi), base, altura, edgecolor='black', facecolor='black'))

        for buraco in self.__buracos: ## Plota os retângulos vazados
            base,altura,xi,yi = buraco.getDimensoes()
            ax.add_patch(plt.Rectangle((xi, yi), base, altura, edgecolor='black', facecolor='white'))

        ax.scatter(self.__Xp, self.__Yp, color='red', label='Pontos (dx, dy)') ## Plota o ponto do centróide

        ## Configurações gerais do gráfico
        plt.axis('equal')
        plt.legend()
        plt.xlabel('Eixo X')
        plt.ylabel('Eixo Y')
        plt.title("Figura Analisada")
        plt.grid(True)
        plt.legend("centróide")
        plt.show()

    


