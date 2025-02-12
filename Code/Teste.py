from Carregamento import Carregamento
from MomentoFletor import MomentoFletor


carregamentos = [ Carregamento(0, 1.25, 100, 100),Carregamento(1.25, 3.25, 20, 500), Carregamento(3.25, 4.25, 120, 0),Carregamento(4.25, 7.25, 100, 10) ]

M = MomentoFletor(carregamentos)
print(M.getMax())
    
M2 = MomentoFletor()
M2.set_carregamentos()
print(M2.getMax())    
