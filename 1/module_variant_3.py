import math


def Fp(x: float, y: float, r=10) -> bool:
    first_quarter = (0 <= x <= r) and (0 <= y <= r)
    second_quarter = (-r<=x<=0 and 0<=y<=r) and ((x + r)**2 + (y - r)**2 >= r**2)
    third_quarter = (-r <= x <= 0) and (-r <= y <= 0)
    fourth_quarter = (r>=x>=0 and 0>=y>=-r) and ((x - r)**2 + (y + r)**2 >= r**2)
    return first_quarter or second_quarter or third_quarter or fourth_quarter


def PTeor(r: float = 10) -> float:
    shaded = 4 * r**2 - (math.pi * r**2) / 2
    delta = r / 12
    rect_area = (2 * r + 2 * delta) ** 2
    return shaded / rect_area




if __name__=='__main__':
    x=float(input('Введите x : '))
    y=float(input(('Введите y : ')))
    print(f'Область попадания ({x},{y}) равна {Fp(x,y)}')


