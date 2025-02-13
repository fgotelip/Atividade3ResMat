import matplotlib.pyplot as plt
class Retangulo():
    def __init__(self,xi,xf,yi,yf):
        self.__xi = xi
        self.__xf = xf
        self.__yi = yi
        self.__yf = yf

        self.__base = self.__xf - self.__xi
        self.__altura = self.__yf - self.__yi
        self.__area = self.__base * self.__altura

        self.__Ixx = (self.__base * self.__altura**3) / 12
        self.__Iyy = (self.__altura * self.__base**3) / 12
        self.__Ixy = 0

        self.__x= (self.__xi + self.__xf) / 2
        self.__y= (self.__yi + self.__yf) / 2

        self.__xp = self.__x * self.__area
        self.__yp = self.__y * self.__area

    def getYi(self):
        return self.__yi

    def getYf(self):
        return self.__yf

    def getCentroide(self):
        return self.__area, self.__xp, self.__yp
    
    def getMomentoDeInercia(self):
        return self.__area, self.__x, self.__y, self.__Ixx, self.__Iyy, self.__Ixy
    
    def getDimensoes(self):
        return self.__base, self.__altura, self.__xi, self.__yi


   