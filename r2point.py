from math import sqrt


class R2Point:
    """ Точка (Point) на плоскости (R2) """

    # Конструктор
    def __init__(self, x=None, y=None):
        if x is None:
            x = float(input("x -> "))
        if y is None:
            y = float(input("y -> "))
        self.x, self.y = x, y

    # Площадь треугольника
    @staticmethod
    def area(a, b, c):
        return 0.5 * ((a.x - c.x) * (b.y - c.y) - (a.y - c.y) * (b.x - c.x))

    # Лежат ли точки на одной прямой?
    @staticmethod
    def is_triangle(a, b, c):
        return R2Point.area(a, b, c) != 0.0

    # Расстояние до другой точки
    def dist(self, other):
        return sqrt((other.x - self.x)**2 + (other.y - self.y)**2)

    # Лежит ли точка внутри "стандартного" прямоугольника?
    def is_inside(self, a, b):
        return (((a.x <= self.x and self.x <= b.x) or
                 (a.x >= self.x and self.x >= b.x)) and
                ((a.y <= self.y and self.y <= b.y) or
                 (a.y >= self.y and self.y >= b.y)))

    # Освещено ли из данной точки ребро (a,b)?
    def is_light(self, a, b):
        s = R2Point.area(a, b, self)
        return s < 0.0 or (s == 0.0 and not self.is_inside(a, b))

    # Совпадает ли точка с другой?
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.x == other.x and self.y == other.y
        return False

    # Расстояние от точки до отрезка
    def dist_s(self, a, b):
        dot_a = (self.x - a.x) * (b.x - a.x) + (self.y - a.y) * (b.y - a.y)
        dot_b = (self.x - b.x) * (a.x - b.x) + (self.y - b.y) * (a.y - b.y)
        if dot_b < 0:
            d = sqrt((self.x - b.x)**2 + (self.y - b.y)**2)
        elif dot_a < 0:
            d = sqrt((self.x - a.x)**2 + (self.y - a.y)**2)
        else:
            d = abs((a.y - b.y) * self.x - (a.x - b.x) *
                    self.y + a.x * b.y - a.y * b.x)/sqrt((a.y - b.y)**2 +
                                                         (a.x - b.x)**2)
        return d

    # Лежит ли точка внутри треугольника
    def is_in_tr(self, a, b, c):
        if b.is_light(a, c):
            a, c = c, a
        return self.is_light(a, b) and self.is_light(b, c) \
            and self.is_light(c, a)


if __name__ == "__main__":
    x = R2Point(1.0, 1.0)
    print(type(x), x.__dict__)
    print(x.dist(R2Point(1.0, 0.0)))
    a, b, c = R2Point(0.0, 0.0), R2Point(1.0, 0.0), R2Point(1.0, 1.0)
    print(R2Point.area(a, c, b))
    p = R2Point(-50.0, -50.0)
    print(p.is_in_tr(R2Point(1000, 0), R2Point(-1000, 0), R2Point(0, 1000)))
