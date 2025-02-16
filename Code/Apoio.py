class Apoio():
    def __init__(self,pos=0,tipo=0,forca=0):
        self.__pos = pos
        self.__tipo = tipo
        self.__forca = forca


    def get_pos(self):
        return self.__pos

    def get_tipo(self):
        return self.__tipo

    def get_forca(self):
        return self.__forca
