#!/usr/bin/env -S python3 -B
from tk_drawer import TkDrawer
from r2point import R2Point
from convex import Figure, Void, Point, Segment, Polygon


def void_draw(self, tk):
    pass


def point_draw(self, tk):
    tk.draw_point(self.p)


def segment_draw(self, tk):
    tk.draw_line(self.p, self.q)


def polygon_draw(self, tk):
    for n in range(self.points.size()):
        tk.draw_line(self.points.last(), self.points.first())
        self.points.push_last(self.points.pop_first())


setattr(Void, 'draw', void_draw)
setattr(Point, 'draw', point_draw)
setattr(Segment, 'draw', segment_draw)
setattr(Polygon, 'draw', polygon_draw)


tk = TkDrawer()
f = Void()
tk.clean()

print("3 точки треугольника")
Figure.Pnt1 = R2Point()
Figure.Pnt2 = R2Point()
Figure.Pnt3 = R2Point()
tk.draw_triangle(Figure.Pnt1, Figure.Pnt2, Figure.Pnt3)
print("Точки в оболочке")

try:
    while True:
        f = f.add(R2Point())
        tk.clean()
        tk.draw_triangle(Figure.Pnt1, Figure.Pnt2, Figure.Pnt3)
        f.draw(tk)
        print(f"S = {f.area()}, P = {f.perimeter()}\n")
except (EOFError, KeyboardInterrupt):
    print("\nStop")
    tk.close()
