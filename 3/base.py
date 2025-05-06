from abc import ABC,abstractmethod


class Subscriptable(type):
    def __getitem__(cls, k):
        return cls.items[k]



class ReservuarClass(metaclass=Subscriptable):
    items=[]
    def __init__(self,material:str,emkost:float,koefCC:float):
        self.material=material
        self.__emkost=emkost
        self.__koefCC=koefCC
        self.__HH=0
        self.__RR=0
        self.__FF = 0.
        ReservuarClass.items.append(self)

    def __str__(self):
        return f"Материал: {self.material}, V={self.emkost}, c={self.koeffC}, R={self.RR:.3f}, H={self.HH:.3f}, FF={self.FF:.3f}"

    @property
    def emkost(self):
        return self.__emkost

    @property
    def koeffC(self):
        return self.__koefCC

    @koeffC.setter
    def koeffC(self, value):
        self.__koefCC = value

    @property
    def RR(self):
        return self.__RR

    @RR.setter
    def RR(self, value):
        self.__RR = value

    @property
    def HH(self):
        return self.__HH

    @HH.setter
    def HH(self,value):
        self.__HH=value

    @property
    def FF(self):
        return self.__FF

    @FF.setter
    def FF(self, value):
        self.__FF = value

    @abstractmethod
    def Fpoverchnosti(self, R, H):
        pass

    @abstractmethod
    def Rfi(self, H):
        pass

    @abstractmethod
    def RaschetOptomParametrov(self):
        pass


