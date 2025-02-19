## Classe para definir apoios
class Apoio(): 
    def __init__(self,pos=0,tipo=0): ## Construtor da classe
        self.__reacao = 0
        self.__pos = pos
        self.__tipo = tipo
        self.__momento = 0

    def set_reacao(self,reacao): ## Define a reação no apoio
        self.__reacao = reacao

    def set_momento(self,momento): ## Define a reação momento no apoio
        self.__momento = momento

    def get_pos(self): ## Retorna a posição do apoio
        return self.__pos

    def get_tipo(self): ## Retorna o tipo do apoio
        return self.__tipo
    
    def get_reacao(self): ## Retorna a reação de apoio
        return self.__reacao
    
    def get_momento(self): ## Retorna a reação momento no apoio
        return self.__momento
    


