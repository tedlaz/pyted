import math


class Point:
    'this is a point'
    def __init__(self, x=0, y=0):
        self.move(x, y)

    def move(self, x, y):
        self.x = x
        self.y = y

    def reset(self):
        self.move(0, 0)

    def calc_distance(self, other_point):
        return math.sqrt(
            (self.x - other_point.x) ** 2 +
            (self.y - other_point.y) ** 2)

if __name__ == '__main__':
    p1 = Point()
    p2 = Point(3, 4)
    print(p1.calc_distance(p2))
    print(p2.calc_distance(p1))
