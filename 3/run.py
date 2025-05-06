from TriangleSquareReservuar_variant_3 import TriangleSquareReservuar


r1 = TriangleSquareReservuar("Сталь_ХВГ", 120, 0.25)
r2 = TriangleSquareReservuar("Алюминиевый_Сплав_А231", 100, 0.35)
r3 = TriangleSquareReservuar("Полимерный_Композит_ПК_421", 180, 0.30)

# До оптимизации
for r in [r1, r2, r3]:
    print("До оптимизации:", r)

# Провести оптимизацию
for r in [r1, r2, r3]:
    r.RaschetOptomParametrov()

# После оптимизации
print("\nПосле оптимизации:")
for r in [r1, r2, r3]:
    print(r)

# Сортировка по объёму
print("\nСортировка по объёму:")
for r in sorted([r1, r2, r3], key=lambda x: x.emkost):
    print(r)

# Построение графика
r4 = TriangleSquareReservuar("Титановый_Сплав_Т12", 130, 0.2)
r4.plot_family([0.2, 0.25, 0.3, 0.35])