"""Реализация алгоритма Диемитко."""
from sympy import prime
from random import randint, random
from gmpy2 import is_prime, f_div, mpz, mpfr, is_odd


def prime_gen(dimension):
    """
    Используем алгоритм Диемитко для генерации чисел нужного порядка
    """
    start_prime = chose_start_prime(dimension)

    current_prime = mpz(start_prime)

    p = mpz(start_prime)

    repit_flag = True

    U = 0

    while p.num_digits() <= dimension:
        if repit_flag:
            repit_flag = False
            N = f_div(mpz(10**(dimension - 1)), mpz(current_prime)) + \
                f_div(mpz(10**(dimension - 1) * mpfr(random())),
                      mpz(current_prime))
            N = N + 1 if N.is_odd() else N
            U = 0
        p = (N + U) * current_prime + 1
        if pow(2, p - 1, p) == 1 and pow(2, N + U, p) != 1:
            repit_flag = True
            break
        else:
            U += 2

    return p


"""
Функция для генерирования простого числа небольшого порядка, для алгоритма Диемитко
"""


def chose_start_prime(position):
    return prime(position + randint(10, 100))
