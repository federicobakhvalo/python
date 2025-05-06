import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize_scalar
from base import ReservuarClass

class TriangleSquareReservuar(ReservuarClass):
    def __init__(self, material, emkost, koeffC):
        super().__init__(material, emkost, koeffC)

    def Fpoverchnosti(self, R, H):
        r = self.koeffC * R
        S_triangle = (3 * R ** 2 * math.sqrt(3)) / 4
        S_square = r ** 2
        S_lateral = (3 * R) * H  # периметр треугольника * H
        return S_triangle + S_square + S_lateral

    def Rfi(self, H):
        r = math.sqrt(self.koeffC)
        V = self.emkost
        # Площадь основания (разность между треугольником и квадратом)
        base_area = lambda R: ((3 * R ** 2 * math.sqrt(3)) / 4) - ((self.koeffC * R) ** 2)
        # def volume_eq(R):
        #     return base_area(R) * H - V
        # Обратная задача — найти R, зная H и V
        R_guess = (self.emkost / H) ** (1/2)
        return R_guess

    def generator_tab(self, n=50):
        h0 = self.emkost ** (1/3)
        hn, hk = h0 / 3, 2 * h0
        hs = np.linspace(hn, hk, n)
        for h in hs:
            R = self.Rfi(h)
            ff = self.Fpoverchnosti(R, h)
            yield (h, ff)

    def RaschetOptomParametrov(self):
        h0 = self.emkost ** (1/3)

        def objective(H):
            R = self.Rfi(H)
            return self.Fpoverchnosti(R, H)

        result = minimize_scalar(objective, bounds=(h0 / 3, 2 * h0), method='bounded')
        Hopt = result.x
        Ropt = self.Rfi(Hopt)
        FFmin = self.Fpoverchnosti(Ropt, Hopt)

        # self._ReservuarClass__HH = Hopt
        # self._ReservuarClass__RR = Ropt
        # self._ReservuarClass__FF = FFmin
        self.HH=Hopt
        self.RR=Ropt
        self.FF=FFmin

    def plot_family(self, c_values):
        plt.figure(figsize=(10, 5))
        for c in c_values:
            # self._ReservuarClass__koeffC=c
            self.koeffC=c

            hs, ffs = zip(*list(self.generator_tab()))
            plt.plot(hs, ffs, label=f'c = {c:.2f}')
        plt.title("FF(H) для разных c")
        plt.xlabel("H")
        plt.ylabel("FF")
        plt.legend()
        plt.grid()
        plt.show()