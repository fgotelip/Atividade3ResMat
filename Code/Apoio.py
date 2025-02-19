class Apoio():
    def __init__(self,pos=0,tipo=0):
        self.__reacao = 0
        self.__pos = pos
        self.__tipo = tipo
        self.__momento = 0

    
    def set_reacao(self,reacao):
        self.__reacao = reacao

    def set_momento(self,momento):
        self.__momento = momento

    def get_pos(self):
        return self.__pos

    def get_tipo(self):
        return self.__tipo
    
    def get_reacao(self):
        return self.__reacao
    
    def get_momento(self):
        return self.__momento
    


