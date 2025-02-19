from Carregamento import Carregamento
from Apoio import Apoio
from Retangulo import Retangulo
from Tensao import Tensao


'''carregamentos1 = [ Carregamento(0,3,"100*x",3),Carregamento(3,5,"200*x",3),Carregamento(5,6,30,2,0,0.75)]
retangulos1=[Retangulo(0,250,0,20),Retangulo(115,135,20,320),Retangulo(0,250,320,340)]
buracos1=[]

tensao1 = Tensao(retangulos1,buracos1,carregamentos1)
tensao1.exibe_resultados()'''



#T3
carregamentos = [ Carregamento(0,1.5,100,1,100),Carregamento(1.5,3,10,2,0,1.5),Carregamento(3,3.75,"133.3333*x",3),Carregamento(3.75,4,30,2,0,0),Carregamento(4,5,100,1,10),Carregamento(5,6,30,2,0,0.75)]
apoios = [Apoio(0,3),0]
retangulos=[Retangulo(0,250,0,20),Retangulo(115,135,20,320),Retangulo(0,250,320,340)]
buracos=[]

tensao = Tensao(retangulos,buracos,carregamentos,apoios)
tensao.exibe_resultados()