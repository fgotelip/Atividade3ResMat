from Retangulo import Retangulo
from MomentoDeInercia import MomentoDeInercia
## Chamada das funções e exibição dos resultados

##retangulos, buracos = LeituraDeRetangulos() Comentei apenas para fazer testes automatizados

## teste 1 da proposta do exercicio
retangulos=[Retangulo(0,48,0,6),Retangulo(20,28,6,54),Retangulo(12,36,54,60)]
buracos=[]

mI = MomentoDeInercia(retangulos, buracos)
mI.exibirResultados()
mI.plotarfigura()

## teste 2 da proposta do exercicio
'''
mI2 = MomentoDeInercia()
mI2.setRetangulos_user()
mI2.exibirResultados()
mI2.plotarfigura()
'''