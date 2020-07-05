from random import randint
from sympy.ntheory import legendre_symbol
from tonelliShanks import sqrt_mod

class Curve():

    """
    Класс для работы с эллиптическими кривыми
    """

    def __init__(self, a, b, field_char):
        """
        Define elliptic curve y^2 = x^3 + ax + b on Field F_q


        Конструктор эллиптической кривой над конечным полем F_q

        """
        if field_char != 3 and field_char != 2 and (4 * a**3 + 27 * b**2) == 0:
            raise Exception(
                "choose field char other than 2 or 3\nand A, B must be like (4*a^3+27*b^2) != 0 !!!")
        self.A = a
        self.B = b
        self.char = field_char

    def is_appertaint(self, point):
        """
        check the point P = (x,y) for equation y^2 = x^2 + ax + b

        Проверка, принадлежит ли точка эллиптической кривой

        Возвращает True если принадлежит и False если нет.

        """
        if point.y == "O" and point.x == "O":
            return True

        if (point.y**2) % self.char == (point.x**3 + self.A * point.x + self.B) % self.char:
            return True
        else:
            return False

    def __str__(self):
        """
        Строковое символьное представление эллиптической кривой 
        отображается при вызове метода print(curve)

        """
        return f"E_p({self.A},{self.B})"

    def all_points(self):
        """
        Be careful!!!


        Displays all points of the curve.

        Отображает все точки эллиптической кривой. Использовать только на небольших значениях 
        характеристики поля.

        """

        def right(x, a, b, N): return (x**3 + a * x + b) % N
        def left(y, N): return y**2 % N

        X = []
        Y = []

        for i in range(self.char):
            X.append((i, right(i, self.A, self.B, self.char)))
            Y.append((i, left(i, self.char)))

        dots = []

        for i in X:
            for j in Y:
                if i[1] == j[1]:
                    z = (i[0], j[0])
                    if z not in dots:
                        dots.append(z)

        return dots

    def random_point(self):
        """
        Generate random point from defined elliptic curve

        Алгоритм генерации случайной точки на эллиптической кривой 

        """
        x_cor = randint(1, self.char)

        f = x_cor**3 + self.A * x_cor + self.B

        while legendre_symbol(f, self.char) != 1:

            x_cor = randint(1, self.char)

            f = x_cor**3 + self.A * x_cor + self.B

        y1, y2 = sqrt_mod(f, self.char)

        return Point(x_cor, y1, self)

    def gen_point_from_coord_x(self, x):
        """ In process"""
        pass


class Point():

    """
    Класс для работы с точками эллиптической кривой
    """

    def __init__(self, x, y, curve):
        """
        Define elliptic curve point like (x,y)
        if you want define big_O point, use parameters ("O", "O")
        """

        self.x = x
        self.y = y
        self.curve = curve

        if self.x == "O" and self.y == "O":
            print("defined big_O point")

    def __str__(self):
        return f"({self.x},{self.y})"

    def x(self):
        """
        return x coordinate
        """
        return self.x

    def y(self):
        """
        return y coordinate
        """
        return self.y

    def __add__(self, other):
        """
        Функция сложения двух точек эллиптической кривой
        """
        if self.curve != other.curve:
            raise Exception("Check curves, maybe they different")

        def L1(x1, x2, y1, y2, N): return ((y2 - y1) * invert(x2 - x1, N)) % N
        def L2(x1, y1, N): return (3 * x1**2 + curve.A) * invert(2 * y1, N) % N

        # Обработка случая, если одна из точек big_O, т.е является
        # нейтральным элементом по сложению

        if (self.x == "O" and self.y == "O"):
            return other
        if (other.x == "O" and other.y == "O"):
            return self

        # Обработка случаев, если точки находятся на одной вертикальной прямой
        if (self.x == other.x and self.y != other.y):
            return Point("O", "O")
        elif(self.y == other.y and self.y == 0):
            return Point("O", "O")

        # Если все частные случаи не подходят, производим расчет
        else:
            lmbd = 0
            if self.x != other.x:
                lmbd = L1(self.x, other.x, self.y, other.y, curve.char)

            elif self.x == other.x and self.y == other.y:
                lmbd = L2(self.x, self.y, curve.char)

            X = (lmbd**2 - self.x - other.x) % curve.char
            Y = (lmbd * (self.x - X) - self.y) % curve.char
            return Point(X, Y, self.curve)

    def mul(self, n):

        if n < 0:
            self.y = -self.y  # Если множитель n отрицательный, то складываем обратные точки

        p = Point(self.x, self.y, self.curve)
        for i in range(-n):
            self = self + p  # Складываем n раз сами с собой

        return self


def ext_gcd(a, b):
    """
    Реализация расширенного алгоритма Евклида
    Returns integer x:
        ax + by = gcd(a, b).
    """
    x, xx, y, yy = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a % b
        x, xx = xx, x - xx * q
        y, yy = yy, y - yy * q
    return (x, y)


def invert(x, n):
    """Функция поиска обратного числа y по модулю  n такого, что x*y == 1 (mod n)"""
    return ext_gcd(x, n)[0] % n


