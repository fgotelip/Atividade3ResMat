from Carregamento import Carregamento
from Retangulo import Retangulo
from Tensao import Tensao


'''
carregamentos = [ Carregamento(0,6,5000,1,5000)]
retangulos=[Retangulo(0,250,0,20),Retangulo(115,135,20,320),Retangulo(0,250,320,340)]
buracos=[]

tensao = Tensao(retangulos,buracos,carregamentos)
tensao.exibe_resultados()


carregamentos2 = "5000"
retangulos2=[Retangulo(0,250,0,20),Retangulo(90,110,20,320),Retangulo(0,250,320,340)]
buracos2=[]

tensao2 = Tensao(retangulos2,buracos2,carregamentos2,2,6)
tensao2.exibe_resultados()
'''

#T1
carregamentos = [ Carregamento(0,3,100,1,100),Carregamento(3,3,10,2,0,0),Carregamento(3,3.75,0,1,100),Carregamento(3.75,4,30,2,0,0),Carregamento(4,5,100,1,10),Carregamento(5,6,30,2,0,0.75)]
retangulos=[Retangulo(0,250,0,20),Retangulo(115,135,20,320),Retangulo(0,250,320,340)]
buracos=[]

tensao = Tensao(retangulos,buracos,carregamentos)
tensao.exibe_resultados()