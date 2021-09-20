# Знакомство с методами класса
class Point:
    x = 0
    y = 0

    def coordinates(self) -> str:
        print(f'coordinates are: {self.x}, {self.y}')


my_point = Point()
my_point.x = 10

my_point.coordinates()


# Конструктор класса
# __init__ - специальный конструктор

class Point:

    def __init__(self, x, y) -> int:
        self.x = x
        self.y = y

    def coordinates(self) -> str:
        print(f'coordinates are: {self.x}, {self.y}')


my_point = Point(5, 16)
my_point.coordinates()


# Метод __repr___
# читабельное представление

class Point:

    def __init__(self, x, y) -> int:
        self.x = x
        self.y = y

    def coordinates(self) -> str:
        print(f'coordinates are: {self.x}, {self.y}')

    def __repr__(self):
        return f'<Point x: {self.x}, y: {self.y}>'


my_point = Point(15, 6)
print(my_point)
