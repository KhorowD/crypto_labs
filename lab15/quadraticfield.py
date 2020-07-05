import time
from gmpy2 import mpz, mul, gcd, f_mod, invert


class QuadraticField():
    """

    Класс для работы с квадратичными иррациональностями 

    x+y*sqrt(c)

    x is Re
    y is Im

    """

    def __init__(self, x, y, c):
        """Конструктор

        С - передается не как корень, а как целое число
        """

        self.re = x
        self.im = y
        self.c = c

    def __str__(self):
        """Строковое отображение данных при вызове функции print()"""
        if self.im > 0:
            return f"{self.re}+{self.im}*sqrt({self.c})"
        else:
            return f"{self.re}{self.im}*sqrt({self.c})"

    def __add__(self, other):
        """
        Сложение двух чисел при помощи оператора \'+\' 

        Корни С должны быть равны!
        """
        if self.c != other.get_root():
            raise Exception("different roots")
        x = self.re + other.x()
        y = self.im + other.y()
        return QuadraticField(x, y, self.c)

    def __mul__(self, other):
        """
        Умножение двух чисел при помощи оператора \'*\' 

        Корни С должны быть равны!
        """
        if self.c != other.get_root():
            raise Exception("different roots")
        x = self.re * other.x() + self.c * self.im * other.y()
        y = self.re * other.y() + self.im * other.x()
        return QuadraticField(x, y, self.c)

    def __sub__(self, other):
        """
        Вычитание двух чисел при помощи оператора \'-\' 

        Корни С должны быть равны!
        """
        if self.c != other.get_root():
            raise Exception("different roots")
        x = self.re - other.x()
        y = self.im - other.y()
        return QuadraticField(x, y, self.c)

    def divmod_on_conj(self, N):
        # if self.c != other.get_root():
        #     raise Exception("different roots")
        Z = invert(mpz(self.x()**2 - (self.y()**2) * self.get_root()), N)

        X = ((self.x()**2 + (self.y()**2) * self.get_root()) * Z) % N
        Y = (2 * self.x() * self.y() * Z) % N
        return QuadraticField(X, Y, self.get_root())

    def pow(num, power, N):
        """
        Реализация функции возведения в степень не рекурсивным способом
        """
        X, Y = [], []
        X.append(1)
        X.append(num.x())
        Y.append(0)
        Y.append(num.y())

        X1 = num.x()
        Y1 = num.y()

        for i in range(1, power // 2 + 1):
            X.append((2 * (X[-(i)]**2) - 1) % N)
            Y.append((2 * X[-(i + 1)] * Y[-(i)]) % N)

            X.append((2 * X[-(i + 1)] * X[-(i)] - X1) % N)
            Y.append((2 * X[-(i + 2)] * Y[-(i)] - Y1) % N)

        print(X)
        print(len(X))
        print(Y)
        print(len(Y))

        return QuadraticField(X[-1], Y[-1], num.get_root())

    def pow_1(self, num, power, N):
        """
        Реализация функции возведения в степень рекурсивным способом
        """
        if power % 2 == 0:
            X = f_mod((2 * (self.rec_x(num, power // 2, N)**2) - 1), N)
            # print(f"x = {X}")
            Y = f_mod((2 * self.rec_x(num, power // 2, N)
                       * self.rec_y(num, power // 2, N)), N)
            # print(f"y = {Y}")
            return QuadraticField(X, Y, num.get_root())
        else:
            X = f_mod((2 * self.rec_x(num, (power - 1) // 2, N) *
                       self.rec_x(num, (power - 1) // 2 + 1, N) - self.rec_x(num, 1, N)), N)
            # print(f"x = {X}")
            Y = f_mod((2 * self.rec_x(num, (power - 1) // 2, N) *
                       self.rec_y(num, (power - 1) // 2 + 1, N) - self.rec_y(num, 1, N)), N)
            # print(f"y = {Y}")
            return QuadraticField(X, Y, num.get_root())

    def rec_x(self, num, power, N):

        # print(power)
        if power == 0:
            return 1
        elif power == 1:
            return num.x()
        elif power % 2 == 0:
            return f_mod((2 * (self.rec_x(num, power // 2, N)**2) - 1), N)
        else:
            return f_mod((2 * self.rec_x(num, (power - 1) // 2, N) * self.rec_x(num, (power - 1) // 2 + 1, N) - self.rec_x(num, 1, N)), N)

    def rec_y(self, num, power, N):

        # print(power)
        if power == 0:
            return 0
        elif power == 1:
            return num.y()
        elif power % 2 == 0:
            return f_mod((2 * self.rec_x(num, power // 2, N) * self.rec_y(num, power // 2, N)), N)
        else:
            return f_mod((2 * self.rec_x(num, (power - 1) // 2, N) * self.rec_y(num, (power - 1) // 2 + 1, N) - self.rec_y(num, 1, N)), N)



    def get_tuple(self):
        return (self.re, self.im)

    def get_root(self):
        return self.c

    def set_root(self, c):
        self.c = c

    def x(self):
        return self.re

    def y(self):
        return self.im

    def conjugate(self):
        """Функция возвращает сопряженное число к исходному"""
        return QuadraticField(self.re, - self.im, self.c)


def find_Xe_Ye(a, b, e, N):
    X = []
    Y = []
    X.append(1)
    X.append(a)
    Y.append(0)
    Y.append(b)
    for i in range(1, e // 2 + 1):
        X.append(0)
        X.append(0)
        X.append(0)
        Y.append(0)
        Y.append(0)
        Y.append(0)
        X[2 * i] = (2 * X[i]**2 - 1) % N
        Y[2 * i] = (2 * X[i] * Y[i]) % N
        X[2 * i + 1] = (2 * X[i] * X[i + 1] - X[1]) % N
        Y[2 * i + 1] = (2 * X[i] * Y[i + 1] - Y[1]) % N

    print(X)
    print(len(X))
    print(Y)
    print(len(Y))
    return X[e], Y[e]


