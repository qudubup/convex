from deq import Deq
from r2point import R2Point


class Figure:
    """ Абстрактная фигура """

    Pnt1 = R2Point(-1.0, 0.0)
    Pnt2 = R2Point(1.0, 0.0)
    Pnt3 = R2Point(0.0, 1.0)

    def perimeter(self):
        return 0.0

    def area(self):
        return 0.0

    def cnt(self):
        return 0


class Void(Figure):
    """ "Hульугольник" """

    def add(self, p):
        return Point(p)


class Point(Figure):
    """ "Одноугольник" """
    Pnt1: R2Point
    Pnt2: R2Point
    Pnt3: R2Point

    def __init__(self, p):
        self.p = p

    def add(self, q):
        return self if self.p == q else Segment(self.p, q)

    def cnt(self):
        if all(x >= 1 for x in [
            self.p.dist_s(self.Pnt1,
                          self.Pnt2),
            self.p.dist_s(self.Pnt1,
                          self.Pnt3),
            self.p.dist_s(self.Pnt3,
                          self.Pnt2)
        ]) and not self.p.is_in_tr(self.Pnt1, self.Pnt2, self.Pnt3):
            return 1
        else:
            return 0


class Segment(Figure):
    """ "Двуугольник" """

    def __init__(self, p, q):
        self.p, self.q = p, q

    def perimeter(self):
        return 2.0 * self.p.dist(self.q)

    def add(self, r):
        if R2Point.is_triangle(self.p, self.q, r):
            return Polygon(self.p, self.q, r)
        elif self.q.is_inside(self.p, r):
            return Segment(self.p, r)
        elif self.p.is_inside(r, self.q):
            return Segment(r, self.q)
        else:
            return self

    def cnt(self):
        c = 0
        if all(x >= 1 for x in [
            self.p.dist_s(self.Pnt1,
                          self.Pnt2),
            self.p.dist_s(self.Pnt1,
                          self.Pnt3),
            self.p.dist_s(self.Pnt3,
                          self.Pnt2)
                ]) and not self.p.is_in_tr(self.Pnt1, self.Pnt2, self.Pnt3):
            c += 1
        if all(x >= 1 for x in [
            self.q.dist_s(self.Pnt1,
                          self.Pnt2),
            self.q.dist_s(self.Pnt1,
                          self.Pnt3),
            self.q.dist_s(self.Pnt3,
                          self.Pnt2)
                ]) and not self.q.is_in_tr(self.Pnt1, self.Pnt2, self.Pnt3):
            c += 1
        return c


class Polygon(Figure):
    """ Многоугольник """

    def __init__(self, a, b, c):
        self.points = Deq()
        self.points.push_first(b)
        if b.is_light(a, c):
            self.points.push_first(a)
            self.points.push_last(c)
        else:
            self.points.push_last(a)
            self.points.push_first(c)
        self._perimeter = a.dist(b) + b.dist(c) + c.dist(a)
        self._area = abs(R2Point.area(a, b, c))
        self._cnt = 0
        if all(x >= 1 for x in [
            a.dist_s(self.Pnt1, self.Pnt2),
            a.dist_s(self.Pnt1, self.Pnt3),
            a.dist_s(self.Pnt3, self.Pnt2)]) \
                and not a.is_in_tr(self.Pnt1, self.Pnt2, self.Pnt3):
            self._cnt += 1
        if all(x >= 1 for x in [
            b.dist_s(self.Pnt1, self.Pnt2),
            b.dist_s(self.Pnt1, self.Pnt3),
            b.dist_s(self.Pnt3, self.Pnt2)]) \
                and not b.is_in_tr(self.Pnt1, self.Pnt2, self.Pnt3):
            self._cnt += 1
        if all(x >= 1 for x in [
            c.dist_s(self.Pnt1, self.Pnt2),
            c.dist_s(self.Pnt1, self.Pnt3),
            c.dist_s(self.Pnt3, self.Pnt2)]) \
                and not c.is_in_tr(self.Pnt1, self.Pnt2, self.Pnt3):
            self._cnt += 1

    def perimeter(self):
        return self._perimeter

    def area(self):
        return self._area

    def cnt(self):
        return self._cnt

    # добавление новой точки
    def add(self, t):

        # поиск освещённого ребра
        for n in range(self.points.size()):
            if t.is_light(self.points.last(), self.points.first()):
                break
            self.points.push_last(self.points.pop_first())

        # хотя бы одно освещённое ребро есть
        if t.is_light(self.points.last(), self.points.first()):

            # учёт удаления ребра, соединяющего конец и начало дека
            self._perimeter -= self.points.first().dist(self.points.last())
            self._area += abs(R2Point.area(t,
                                           self.points.last(),
                                           self.points.first()))

            # удаление освещённых рёбер из начала дека
            p = self.points.pop_first()
            while t.is_light(p, self.points.first()):
                self._perimeter -= p.dist(self.points.first())
                self._area += abs(R2Point.area(t, p, self.points.first()))
                if all(x >= 1 for x in [
                    p.dist_s(self.Pnt1, self.Pnt2),
                    p.dist_s(self.Pnt1, self.Pnt3),
                    p.dist_s(self.Pnt3, self.Pnt2)]) \
                        and not p.is_in_tr(self.Pnt1, self.Pnt2, self.Pnt3):
                    self._cnt -= 1
                p = self.points.pop_first()
            self.points.push_first(p)

            # удаление освещённых рёбер из конца дека
            p = self.points.pop_last()
            while t.is_light(self.points.last(), p):
                self._perimeter -= p.dist(self.points.last())
                self._area += abs(R2Point.area(t, p, self.points.last()))
                if all(x >= 1 for x in [
                    p.dist_s(self.Pnt1, self.Pnt2),
                    p.dist_s(self.Pnt1, self.Pnt3),
                    p.dist_s(self.Pnt3, self.Pnt2)]) \
                        and not p.is_in_tr(self.Pnt1, self.Pnt2, self.Pnt3):
                    self._cnt -= 1
                p = self.points.pop_last()
            self.points.push_last(p)

            # добавление двух новых рёбер
            self._perimeter += t.dist(self.points.first()) + \
                t.dist(self.points.last())
            if all(x >= 1 for x in [
                t.dist_s(self.Pnt1, self.Pnt2),
                t.dist_s(self.Pnt1, self.Pnt3),
                t.dist_s(self.Pnt3, self.Pnt2)]) \
                    and not t.is_in_tr(self.Pnt1, self.Pnt2, self.Pnt3):
                self._cnt += 1
            self.points.push_first(t)

        return self


if __name__ == "__main__":
    f = Void()
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(1.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 1.0))
    print(type(f), f.__dict__)
