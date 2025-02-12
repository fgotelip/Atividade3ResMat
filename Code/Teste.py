from Carregamento import Carregamento
from Retangulo import Retangulo
from Tensao import Tensao

'''
carregamentos = [ Carregamento(0,6,5000,5000)]
retangulos=[Retangulo(0,250,0,20),Retangulo(115,135,20,320),Retangulo(0,250,320,340)]
buracos=[]

tensao = Tensao(retangulos,buracos,carregamentos)
tensao.exibe_resultados()
'''

carregamentos = [ Carregamento(0,3,10,5000)]
retangulos=[Retangulo(0,250,0,20),Retangulo(115,135,20,320),Retangulo(0,250,320,340)]
buracos=[]

tensao = Tensao(retangulos,buracos,carregamentos)
tensao.exibe_resultados()

