from pathlib import Path
from typing import Dict, List

import matplotlib.pyplot as plt
import random
import numpy as np

import pandas as pd

from module_variant_3 import Fp,PTeor



# def script(file_path: Path, shoots: int, seed: int,radius:int=10):
#     with open(file_path, 'w', encoding='utf-8') as file:
#         file.write('X\t\t\tY\t\t\tResult\n')
#         random.seed(seed)
#         for shoot in range(shoots):
#             x=random.uniform(-radius,radius)
#             y=random.uniform(-radius,radius)
#             file.write(f'{x:.4f}\t\t{y:.4f}\t\t{int(Fp(x, y))}\n')


class ShootingExperiment:
    def __init__(self, r: float = 10, N: int = 1000, T: int = 15, delta_factor: float = 12):
        self.r = r
        self.N = N
        self.T = T
        self.delta_factor = delta_factor
        self.results = {'Pst': [], 'PT': []}

    def Pst(self, X: List[float], Y: List[float]) -> float:
        hits = sum(Fp(x, y) for x, y in zip(X, Y))
        return hits / self.N


    def run_experiment(self, seed: int):
        np.random.seed(seed)
        X = np.random.uniform(-self.r, self.r, self.N)
        Y = np.random.uniform(-self.r, self.r, self.N)

        Pst_value = self.Pst(X, Y)
        PT_value = PTeor()

        self.results['Pst'].append(Pst_value)
        self.results['PT'].append(PT_value)

        return Pst_value, PT_value


    def save_results_to_file(self, file_path: Path):
        with open(file_path, 'a') as file:
            for i in range(self.T):
                file.write(f"{i+1}. Pst: {self.results['Pst'][i]}, PT: {self.results['PT'][i]}\n")

    # Визуализация результатов
    def plot_results(self):
        t = np.arange(1, self.T + 1)
        plt.plot(t, self.results['PT'], label="PT (Теоретическая вероятность)", linestyle='-', color='b')
        plt.scatter(t, self.results['Pst'], label="Pst (Статистическая вероятность)", color='r', marker='*')

        plt.xlabel("Номер эксперимента (t)")
        plt.ylabel("Вероятность")
        plt.legend()
        plt.title("Сравнение теоретической и статистической вероятности попадания")
        plt.show()

    # Основной метод для выполнения всех опытов
    def perform_experiments(self, file_path: Path):
        for i in range(self.T):
            Pst_value, PT_value = self.run_experiment(seed=i)
            print(f"Эксперимент {i+1}: Pst = {Pst_value}, PT = {PT_value}")

        # Записываем результаты в файл только после выполнения всех экспериментов
        self.save_results_to_file(file_path)

        # Строим график после всех опытов
        self.plot_results()

class DataframeData:

    def __init__(self,shoots:int,seed:int,radius:int=10):
        self._shoots=shoots
        self._seed=seed
        self._radius=radius



    def create_df(self)->pd.DataFrame:
        data=self.make_data()
        df=pd.DataFrame(data)
        return  df
    def make_data(self)->Dict:
        delta = self._radius / 12
        xn, xk = -self._radius - delta, self._radius + delta
        yn, yk = -self._radius - delta, self._radius + delta

        np.random.seed(self._seed)
        X = np.random.uniform(xn, xk, self._shoots)
        Y = np.random.uniform(yn, yk, self._shoots)
        P = [int(Fp(x, y, self._radius)) for x, y in zip(X, Y)]
        J = list(range(self._shoots))

        # Словарь
        data_dict: Dict[str, List] = {
            "J": J,
            "X": X.tolist(),
            "Y": Y.tolist(),
            "P": P
        }

        return data_dict



    def save_results(self, txt_path:Path,csv_path: Path, xlsx_path: Path):

        df=self.create_df()
        df.to_csv(csv_path, index=False)
        df.to_csv(txt_path, sep='|', index=False)
        df.to_excel(xlsx_path, index=False)





if __name__=='__main__':
    experiment = ShootingExperiment(r=10, N=1000, T=15)
    experiment.perform_experiments(Path("betaTest.txt"))

    #DataframeData(shoots=300,seed=20).save_results(Path('alphaTest.txt'),Path('res.csv'),Path('res.xlsx'))


