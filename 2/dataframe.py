import pandas as pd
import numpy as np




class DataframeDevelopersPO:
    def __init__(self,seed:int,N:int):
        self.random = np.random.RandomState(seed)
        self.N=N
        self.__df=pd.DataFrame()

    def get_levels(self):
        levels = ["Junior", "Middle", "Senior"]
        level_probs = [0.5, 0.45, 0.05]
        chosen_levels = self.random.choice(levels, size=self.N, p=level_probs)
        return chosen_levels
    def get_departments(self):

        departments = [
            "Web-разработчики",
            "Web-дизайнеры",
            "Разработчики ядра",
            "Системные администраторы",
            "Тестировщики"
        ]
        department_probs = [0.3, 0.15, 0.05, 0.3, 0.2]
        chosen_departments = self.random.choice(departments, size=self.N, p=department_probs)
        return chosen_departments

    def get_birth_years(self):
        birth_years = self.random.normal(loc=1995, scale=5, size=self.N).astype(int)
        birth_years = np.clip(birth_years, 1980, 2010)
        return birth_years

    def get_incomes(self):
        incomes = self.random.normal(loc=25000, scale=12000, size=self.N)
        incomes = np.round(np.clip(incomes, 5000, None), 2)
        return incomes

    # def get_genders(self):
    #     np.random.seed(self.seed)
    #     return np.random.choice(['м', 'ж'], size=self.N, p=[0.7, 0.3])

    def get_surname_and_name(self,gender):
        male_first_names = ['Иван', 'Алексей', 'Дмитрий', 'Сергей', 'Никита']
        female_first_names = ['Анна', 'Мария', 'Елена', 'Ольга', 'Светлана']
        last_names = ['Иванов', 'Петров', 'Сидоров', 'Кузнецов', 'Смирнов','Фамусов','Копейкин','Галкин']
        surname=self.random.choice(last_names)
        if gender == 'м':
            name=self.random.choice(male_first_names)
        else:
            surname+='а'
            name=self.random.choice(female_first_names)
        return f'{surname} {name}'

    def get_weights_and_heights(self):
        genders=self.random.choice(['м', 'ж'], size=self.N, p=[0.7, 0.3])

        weights=[]
        heights=[]
        for gender in genders:
            if gender == 'м':
                w = self.random.normal(loc=78, scale=10)
                h = self.random.normal(loc=178, scale=8)
            else:
                w = self.random.normal(loc=65, scale=8)
                h = self.random.normal(loc=165, scale=7)
            weights.append(round(max(45, w), 1))  # минимум 45 кг
            heights.append(round(h, 1))
        return genders,weights,heights





    def generate_df(self):
        numbers=list(range(1,self.N+1))
        #surnames=[f'Разработчик_{x}' for x in range(self.N)]
        genders,weights,heights=self.get_weights_and_heights()
        surnames=[self.get_surname_and_name(x) for x in genders]
        self.__df = pd.DataFrame({
            "Номер": numbers,
            "ФИО": surnames,
            "Год рождения": self.get_birth_years(),
            "Пол": genders,
            "Вес (кг)": weights,
            "Рост (см)": heights,
            "Отдел": self.get_departments(),
            "Уровень": self.get_levels(),
            "Доход на душу": self.get_incomes()
        })


    def get_df(self):
        return self.__df




if __name__=='__main__':
    dev1 = DataframeDevelopersPO(seed=156, N=35)
    dev1.generate_df()
    df1 = dev1.get_df()
    print(df1.head())
    df1.to_csv("ishodVar.csv", index=False)
    df1.to_excel("ishodVar.xlsx", index=False)

