from Carregamento import Carregamento
from MomentoFletor import MomentoFletor

def main():
    carregamentos = [ Carregamento(0, 1.25, 100, 100),Carregamento(1.25, 3.25, 20, 500), Carregamento(3.25, 4.25, 120, 0),Carregamento(4.25, 7.25, 100, 10) ]

    M = MomentoFletor()
    M.set_carregamentos_teste(carregamentos)
    M.calcular_reacoes()
    M.set_esforcos()
    print(M.getMax())
    M.imprimir_pontos()

    
    

if __name__ == "__main__":
    main()
