#!/usr/bin/env -S python3 -B
from r2point import R2Point
from convex import Void, Figure

print("3 точки треугольника")
Figure.Pnt1 = R2Point()
Figure.Pnt2 = R2Point()
Figure.Pnt3 = R2Point()
print("Точки в оболочке")

f = Void()
try:
    while True:
        f = f.add(R2Point())
        print(f"S = {f.area()}, P = {f.perimeter()}, CNT = {f.cnt()}")
        print()
except (EOFError, KeyboardInterrupt):
    print("\nStop")
