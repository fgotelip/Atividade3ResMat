import matplotlib.pyplot as plt
## Exercício 1
def calculaCentroide(retangulos,buracos): ## função para calcular o centróide da figura
    areaPreenchida=0
    areaVazada=0
    xc=yc=0
    for xi,xf,yi,yf in retangulos: ## Loop para percorrer o vetor de retângulos
        base=xf-xi ## Base de um retângulo
        altura=yf-yi ## Altura de um retângulo
        area=base*altura ## Área de um retângulo
        areaPreenchida+=area ## Soma a área de cada retângulo
        xp=(xi+xf)/2 * area ## Coordenada X do centróide de um retângulo
        yp=(yi+yf)/2 * area ## Coordenada Y do centróide de um retângulo
        xc+=xp ## Adiciona a coordenada X do centróide de um retângulo na contribuição global
        yc+=yp ## Adiciona a coordenada Y do centróide de um retângulo na contribuição global
    if buracos: ## Caso seja uma figura vazada
        for xi,xf,yi,yf in buracos: ## Loop para percorrer o vetor de buracos
            base=xf-xi
            altura=yf-yi
            area=base*altura
            areaVazada+=area
            xp=(xi+xf)/2 * area
            yp=(yi+yf)/2 * area
            xc-=xp ## Retira a coordenada X do centróide do buraco na contribuição global
            yc-=yp ## Retira a coordenada Y do centróide do buraco na contribuição global
    xc/=(areaPreenchida-areaVazada) ## Posição X do centróide da figura
    yc/=(areaPreenchida-areaVazada) ## Posição Y do centróide da figura

    return xc, yc

def calcularMomentoDeInercia(retangulos, buracos): ## Função para calcular o momento de inércia da figura
    Xp, Yp = calculaCentroide(retangulos,buracos) ## Chama a função para calcular o centróuide
    Ixx = 0 ## Inicializa o momento de inércia em relação a X
    Iyy = 0 ## Inicializa o momento de inércia em relação a Y
    Ixy = 0 ## Inicializa o produto de inércia
    dX=0 ## Inicializa a distancia X entre o centróide do retângulo e da figura
    dY=0 ## Inicializa a distancia Y entre o centróide do retângulo e da figura
    for xi, xf, yi, yf in retangulos: ## Loop para percorrer o vetor de retângulos
        base = xf - xi
        altura = yf - yi
        area = base * altura
        x = (xi + xf) / 2 ## Centróide X do retângulo analisado
        y = (yi + yf) / 2 ## Centróide Y do retângulo analisado
        IxxLocal = (base * altura**3) / 12 ## Momento de inercia X de um retângulo
        IyyLocal = (altura * base**3) / 12 ## Momento de inercia Y de um retângulo
        IxyLocal = 0
        dX = x - Xp ## Distância em X entre o centróide do retângulo analisado e o da figura
        dY = y - Yp ## Distância em Y entre o centróide do retângulo analisado e o da figura
        Ixx += IxxLocal + area * dY**2 ## Momento de inércia em X final
        Iyy += IyyLocal + area * dX**2 ## Momento de inércia em Y final
        Ixy += IxyLocal + area * dX * dY ## Produto de inércia final
    if buracos: ## Apenas se existir buracos na figura
        for xi, xf, yi, yf in buracos: ## Loop para percorrer o vetor de buracos
            base = xf - xi
            altura = yf - yi
            area = base * altura
            x = (xi + xf) / 2
            y = (yi + yf) / 2
            IxxLocal = (base * altura**3) / 12
            IyyLocal = (altura * base**3) / 12
            IxyLocal = 0
            dX = x - Xp
            dy = y - Yp
            Ixx -= IxxLocal + area * dY**2 ## Subtrái o momento de inércia em X do buraco
            Iyy -= IyyLocal + area * dX**2 ## Subtrái o momento de inércia em Y do buraco
            Ixy -= IxyLocal + area * dX * dY ## Subtrái o produto de inércia do buraco
    return Ixx, Iyy, Ixy ,Xp ,Yp

def plotarfigura(retangulos, buracos, dx, dy): ## Função para plotar o problema
    fig, ax = plt.subplots()
    for xi, xf, yi, yf in retangulos: ## Plota os retângulos cheios
        base = xf - xi
        altura = yf - yi
        ax.add_patch(plt.Rectangle((xi, yi), base, altura, edgecolor='black', facecolor='black'))

    for xi, xf, yi, yf in buracos: ## Plota os retângulos vazados
        base = xf - xi
        altura = yf - yi
        ax.add_patch(plt.Rectangle((xi, yi), base, altura, edgecolor='black', facecolor='white'))

    ax.scatter(dx, dy, color='red', label='Pontos (dx, dy)') ## Plota o ponto do centróide

    ## Configurações gerais do gráfico
    plt.axis('equal')
    plt.legend()
    plt.xlabel('Eixo X')
    plt.ylabel('Eixo Y')
    plt.title("Figura Analisada")
    plt.grid(True)
    plt.legend("centróide")
    plt.show()

def LeituraDeRetangulos(): ## função para ler as infor,ações do problema
    retangulos = []
    numRetangulos = int(input("Digite o número de retângulos na figura: "))

    for i in range(numRetangulos): ## Loop para inserir coordenadas dos retângulos cheios
        entrada = input(f"Digite as coordenadas do retângulo {i+1} (X-inicial, X-final, Y-inicial, Y-final): ")
        xi, xf, yi, yf = map(float, entrada.split())
        retangulos.append((xi, xf, yi, yf))

    figOca = input("Existe algum buraco na estrutura? (s/n): ")
    if figOca.lower() == 's':
        buracos = []
        numBuracos = int(input("Digite o número de buracos na figura: "))

        for i in range(numBuracos): ## Loop para inserir as coordenadas dos buracos
            entrada = input(f"Digite as coordenadas do buraco {i+1} (X-inicial, X-final, Y-inicial, Y-final): ")
            xi, xf, yi, yf = map(float, entrada.split())
            buracos.append((xi, xf, yi, yf))

    return retangulos, buracos


## Chamada das funções e exibição dos resultados

##retangulos, buracos = LeituraDeRetangulos() Comentei apenas para fazer testes automatizados

## teste 1 da proposta do exercicio
retangulos=[(0,48,0,6),(20,28,6,54),(12,36,54,60)]
buracos=[]

Ixx, Iyy, Ixy, dx, dy = calcularMomentoDeInercia(retangulos, buracos)

print(f"O centroide da figura é: {dx},{dy}")

print(f"Momento de inércia em relação ao eixo X: {Ixx:.2f} cm⁴")
print(f"Momento de inércia em relação ao eixo Y: {Iyy:.2f} cm⁴")
print(f"Produto de inércia Ixy: {Ixy:.2f} cm⁴")

plotarfigura(retangulos, buracos,dx,dy)