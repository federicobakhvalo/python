from typing import Dict

import pandas as pd
import numpy as np




def __to_csv(df:pd.DataFrame):
    df.to_csv("output.txt", index=False, sep='\t', mode='a', encoding='utf-8')
    df.to_excel("output.xlsx", index=False)


def show_series(df:pd.DataFrame,seria:str):
    print("\nСерия: ",seria)
    print(df[seria])

# Пример выделения серий

def perform_sorts(df: pd.DataFrame):
    print("\n" + "="*50 + "\nПримеры сортировок:\n" + "="*50)

    # 1. Сортировка по возрасту (по возрастанию)
    sort1 = df.sort_values(by='Год рождения', ascending=True)
    print("\n1. Сортировка по возрасту (старшие сначала):")
    print(sort1[['ФИО', 'Год рождения']].head())

    # 2. Сортировка по росту (по убыванию)
    sort2 = df.sort_values(by='Рост (см)', ascending=False)
    print("\n2. Сортировка по росту (высокие сначала):")
    print(sort2[['ФИО', 'Рост (см)']].head())

    # 3. Сортировка по отделу и весу
    sort3 = df.sort_values(by=['Вес (кг)','Отдел'],ascending=[False,False])
    print("\n3. Сортировка по отделу и весу:")
    print(sort3[['ФИО', 'Отдел', 'Вес (кг)']].head())

    # 4. Сортировка по уровню и доходу
    df['Уровень_число'] = df['Уровень'].map({'Низкий': 0, 'Средний': 1, 'Высокий': 2})
    sort4 = df.sort_values(by=[ 'Доход на душу','Уровень_число',])
    print("\n4. Сортировка по уровню и доходу:")
    print(sort4[['ФИО', 'Уровень', 'Доход на душу']].head())
    df.drop(columns='Уровень_число', inplace=True)

    # 5. Сортировка по полу и возрасту
    sort5 = df.sort_values(by=['Пол', 'Год рождения'], ascending=[True, False])
    print("\n5. Сортировка по полу и возрасту:")
    print(sort5[['ФИО', 'Пол', 'Год рождения']].head())



def perform_filters(df:pd.DataFrame):
    print("\nФильтр: только мужчины")
    print(df[df["Пол"] == "м"])

    # По возрасту (допустим, родившиеся после 1990)
    print("\nФильтр: родившиеся после 1990")
    print(df[df["Год рождения"] > 1990])

    # По росту выше 170 см и весу меньше 80 кг
    filtered = df[(df["Рост (см)"] > 170) & (df["Вес (кг)"] < 80)]
    print("\nФильтр: Рост > 170 и Вес < 80")
    print(filtered)
    print("\nФильтр 1: Женщины из 'Web-дизайнеры'")
    print(WorkVar[(WorkVar["Пол"] == "ж") & (WorkVar["Отдел"] == "Web-дизайнеры")])

    print("\nФильтр 2: Мужчины старше 30 лет")
    print(WorkVar[(WorkVar["Пол"] == "м") & (2025 - WorkVar["Год рождения"] > 30)])

    print("\nФильтр 3: Доход > 30000 и уровень Senior")
    print(WorkVar[(WorkVar["Доход на душу"] > 30000) & (WorkVar["Уровень"] == "Senior")])

    print("\nФильтр 4: Рост между 160 и 180")
    print(WorkVar[(WorkVar["Рост (см)"] >= 160) & (WorkVar["Рост (см)"] <= 180)])

    print("\nФильтр 5: Уровень != Middle")
    print(WorkVar[WorkVar["Уровень"] != "Middle"])

    print("\nФильтр 6: Отдел в списке ['Тестировщики', 'Web-дизайнеры']")
    print(WorkVar[WorkVar["Отдел"].isin(["Тестировщики", "Web-дизайнеры"])])

def perform_set(df:pd.DataFrame):
    departments = set(df["Отдел"])
    levels = set(df["Уровень"])
    print("Множество отделов:", departments)
    print("Множество уровней:", levels)
    print("Пересечение:", departments & levels)
    print('Объединение : ',departments | levels)

def create_dictionaries(df):
    print("\n" + "="*50 + "\nСоздание словарей:\n" + "="*50)

    # 1. Словарь по отделу
    dict1 = {
        'Отделы': {k: tuple(v) for k, v in df.groupby('Отдел').groups.items()},
        'Уровни': {k: tuple(v) for k, v in df.groupby('Уровень').groups.items()}
    }

    # print("\n1. Словарь по отделам (первые 2 записи для каждого):")
    # for dept, ids in dict1['Отделы'].items():
    #     print(f"\n{dept}:")
    #     print(df.loc[list(ids)[:2]])

    # 2. Словарь с ключами (Отдел, Уровень)
    dict2 = {}
    for (dept, level), group in df.groupby(['Отдел', 'Уровень']):
        dict2[(dept, level)] = tuple(group.index)

    # print("\n2. Словарь по (Отдел, Уровень) (пример):")
    # for key in list(dict2.keys())[:3]:
    #     print(f"\n{key}:")
    #     print(df.loc[list(dict2[key])[:2]])

    return dict1, dict2

def filter_dictionaries(dict1:Dict, dict2:Dict, df:pd.DataFrame):
    print("\n" + "="*50 + "\nФильтрация словарей:\n" + "="*50)

    # 1. Фильтр по полу (мужчины)
    print("\n1. Фильтр по полу (мужчины):")
    male_ids = set(df[df['Пол'] == 'м'].index)
    filtered = {k: tuple(set(v) & male_ids) for k, v in dict1['Отделы'].items()}
    for k, v in filtered.items():
        if v:
            print(f"{k}: {len(v)} записей")

    # 2. Фильтр по возрасту (18-20 лет)
    ages = 2025 - df['Год рождения']
    age_ids = set(df[ages.between(18, 20)].index)
    filtered = {k: tuple(set(v) & age_ids) for k, v in dict2.items()}
    print("\n2. Фильтр по возрасту 18–20 лет (первые 3 группы):")
    for k in list(filtered.keys())[:3]:
        if filtered[k]:
            print(f"{k}: {len(filtered[k])} записей")

def save_all_results(df:pd.DataFrame):
    with pd.ExcelWriter('results.xlsx') as writer:
        df.to_excel(writer, sheet_name='Исходные данные', index=False)

        # Сохраняем фильтрации
        df[df['Пол'] == 'м'].to_excel(writer, sheet_name='Мужчины', index=False)
        df[df['Отдел'] == 'Тестировщики'].to_excel(writer, sheet_name='Отдел Тестировщики', index=False)
        df[(df['Уровень'] == 'Middle') & (df['Доход на душу'] > 35000)].to_excel(writer,sheet_name='Мидлы с доходом больше 20к',index=False)
        df.groupby('Отдел')['Доход на душу'].mean().reset_index().to_excel(writer,sheet_name='Средние зарплаты по отделам',index=False)

        # Статистика по числовым колонкам
        df.describe().to_excel(writer, sheet_name='Статистики')

    print("\nВсе результаты сохранены в файл 'результаты_данных.xlsx'")


if __name__=='__main__':
    # 1.1 Чтение файла и сохранение копии
    IshodVar = pd.read_csv("ishodVar.csv")
    WorkVar = IshodVar.copy()
    #show_series(WorkVar,'Уровень')
    #perform_sorts(WorkVar)
    #perform_filters(WorkVar)
    #perform_set(WorkVar)
    # dict1,dict2=create_dictionaries(WorkVar)
    # filter_dictionaries(dict1,dict2,WorkVar)
    save_all_results(WorkVar)



