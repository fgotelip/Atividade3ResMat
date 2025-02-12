from Carregamento import Carregamento
from MomentoFletor import MomentoFletor
from Retangulo import Retangulo


carregamentos = [ Carregamento(0, 1.25, 100, 100),Carregamento(1.25, 3.25, 20, 500), Carregamento(3.25, 4.25, 120, 0),Carregamento(4.25, 7.25, 100, 10) ]
retangulos=[Retangulo(0,48,0,6),Retangulo(20,28,6,54),Retangulo(12,36,54,60)]
buracos=[]

M = MomentoFletor(carregamentos)
print(M.getMomentoMax)
    
M2 = MomentoFletor()
M2.set_carregamentos()
print(M2.getMomentoMax)    
