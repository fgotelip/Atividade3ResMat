from Elemento import Elemento
from Torcao import Torcao

## Execução principal do exercício 3

elementos = [Elemento(0.8,0.06,77e9,2000,True,0.044,0,0.6),Elemento(0.4,0.03,77e9,250)]

torcao = Torcao(elementos)
torcao.exibir_resultados()

'''
torcao = Torcao()
torcao.set_elementos()
torcao.exibir_resultados()
'''