
import primegen
import re
from random import randint
from sympy.ntheory import legendre_symbol, jacobi_symbol
from math import gcd
import quadraticfield as qd
from gmpy2 import invert, is_prime
from time import time


def convert_chars_to_int(msg):
    """
    Функция перевода символов в числа
    """
    return [ord(ch) for ch in msg]


def convert_int_to_chars(num_to_decode):
    """
    Функция перевода чисел в символы
    """
    return "".join([chr(num) for num in num_to_decode])


def make_number_to_encode(numbers):
    """
    Функция, которая делает составное число из индексов символов

    Пример:
    Входное сообщение: abc

    1. Находим индексы символов: 

        ord(a) = 97, ord(b)= 98, ord(c)=99

    2. Переводим в строковый тип данных и добавляем 0 пока длина
    каждого числа не будет равняться 3:

        "097", "098", "099"

    3. Добавляем в начало любое число, отличное от 0,
    для однозначного декодирования, и объединяем строки

        "1"+"097"+"098"+"099" = "1097098099"

    Исходное число будем шифровать, как единую последовательность

    """

    return int("1" + "".join([str(num).rjust(3, "0") for num in numbers]))


def div_str_to_numbers(large_number):
    """
    Функция, которая разбивает число на индексы символов в таблице unicode
    """
    str_to_div = str(large_number)[1:]
    return [int(str_to_div[i:i + 3]) for i in range(0, len(str_to_div), 3)]


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
    return x, y

def get_c(prime1, prime2):

    c = 0
    for i in range(2, (prime1 if prime1 > prime2 else prime2) - 1):
        if (legendre_symbol(i, prime1) % 4 == (-prime1) % 4) and (legendre_symbol(i, prime2) % 4 == (-prime2) % 4):
            c = i
            break

    return c


def get_s(c, n):
    s = 2
    for i in range(2, n - 1):
        s = jacobi_symbol(i**2 - c, n)
        if s == -1 and gcd(s, n) == 1:
            s = i
            break
    return s


def get_m(prime1, prime2, c):
    return (prime1 - legendre_symbol(c, prime1)) * (prime2 - legendre_symbol(c, prime2)) // 4

def get_e_d(m):

    e = primegen.prime_gen(3)

    while gcd(e, m) != 1:
        e = primegen.prime_gen(3)

    d = (pow(e, -1, m) * (m + 1) // 2) % m

    return e, d


def gen_keys(dimension):
    """
    Функция, которая генерирует ключи абонента 

    """

    print("Parametrs: \n")

    p = primegen.prime_gen(dimension)

    while is_prime(p) == False:
        p = primegen.prime_gen(dimension)

    q = primegen.prime_gen(dimension)

    while is_prime(q) == False:
        q = primegen.prime_gen(dimension)

    print(f"p = {p}, q = {q}")

    N = p * q

    print(f"N = {N}")

    C = get_c(p, q)

    print(f"c = {C}")

    S = get_s(C, N)

    print(f"s = {S}")

    M = get_m(p, q, C)

    print(f"m = {M}")

    E, D = get_e_d(M)

    print(f"e = {E}, d = {D}\n")

    return (p, q, M, D), (N, E, C, S)


def williams_encode(msg_to_encode):

    # переводим символы в числа
    numbers_list = convert_chars_to_int(msg_to_encode)

    print(numbers_list)

    int_m = make_number_to_encode(numbers_list)
    print(int_m)

    sec_key, open_key = gen_keys(7)

    # int_m = 21

    # sec_key, open_key = (11, 13, 35, 16), (143, 23, 5, 2)

    print("Start encoding...\n")

    if int_m < open_key[0]:
        if jacobi_symbol(int_m**2 - open_key[2], open_key[0]) == 1:
            b1 = 0
            gamma = qd.QuadraticField(int_m, 1, open_key[2])
            print(f"gamma = {gamma}")
        elif jacobi_symbol(int_m**2 - open_key[2], open_key[0]) == -1:
            b1 = 1
            gamma = qd.QuadraticField(
                int_m, 1, open_key[2]) * qd.QuadraticField(open_key[3], 1, open_key[2])
            print(f"gamma = {gamma}")
        else:
            print("Jacobi symbol == 0!")
            exit()
    else:
        print("to long message")
        exit()
    alpha = gamma.divmod_on_conj(open_key[0])
    print(f"alpha = {alpha}")

    b2 = alpha.x() % 2
    print(f"b1 = {b1}, b2 = {b2}")

    alpha = alpha.pow_1(alpha, open_key[1], open_key[0])

    print(f"alpha = {alpha}\n")

    z = invert(alpha.y(), open_key[0])

    E = (alpha.x() * z) % open_key[0]

    print(f"Encoded_message = ({E}, {b1}, {b2})\n")

    return (E, b1, b2), sec_key, open_key


def williams_decode(msg_to_decode, sec_k, open_k):

    alpha_2e = qd.QuadraticField(
        msg_to_decode[0], 1, open_k[2]).divmod_on_conj(open_k[0])

    print(f"alpha_2e = {alpha_2e}\n")

    start_time = time()

    alpha_2ed = alpha_2e.pow_1(alpha_2e, sec_k[3], open_k[0])
    print(f"alpha_2ed = {alpha_2ed}\n")

    print(f"time for pow_mod (sec) = {(time()-start_time) % 60}\n")

    # тут надо учитывать четность, если уже нечетное а, то ничего не делать
    if msg_to_decode[2] == 1 and alpha_2ed.x() % 2 == 0:
        alpha_2ed = qd.QuadraticField(
            open_k[0] - alpha_2ed.x(), open_k[0] - alpha_2ed.y(), open_k[2])
        print(f"alpha_2ed_parity_correct = {alpha_2ed}\n")

    if msg_to_decode[2] == 0 and alpha_2ed.x() % 2 == 1:
        alpha_2ed = qd.QuadraticField(
            open_k[0] - alpha_2ed.x(), open_k[0] - alpha_2ed.y(), open_k[2])
        print(f"alpha_2ed_parity_correct = {alpha_2ed}\n")

    # а тут мы учитываем не просто знак, а должны домножить число на (s - kor_c)/(s + kor_c)
    if msg_to_decode[1] == 1:
        addition = qd.QuadraticField(open_k[3], 1, alpha_2ed.get_root())
        print(f"add = {addition}\n")
        addition = addition.divmod_on_conj(open_k[0])
        print(f"add1 = {addition}\n")
        addition = qd.QuadraticField(
            addition.x(), - addition.y(), addition.get_root())
        print(f"add_conj = {addition}\n")
        alpha_2ed = alpha_2ed * addition
        alpha_2ed = qd.QuadraticField(
            alpha_2ed.x() % open_k[0], alpha_2ed.y() % open_k[0], alpha_2ed.get_root())

    print(f"alpha_2ed_final = {alpha_2ed}\n")

    z = invert((alpha_2ed.x() - 1)**2 -
               open_k[2] * alpha_2ed.y()**2, open_k[0])
    # print(f"invert = {z}\n")
    int_m_1 = (alpha_2ed.x()**2 - 1 -
               open_k[2] * alpha_2ed.y()**2) * z % open_k[0]
    int_m_2 = -2 * alpha_2ed.y() * open_k[2] * z % open_k[0]

    print(f"result number = {int_m_1+int_m_2}")

    return convert_int_to_chars(div_str_to_numbers(int_m_1 + int_m_2))


def main():

    isLatinNumString = False

    while isLatinNumString != True:

        # получаем входную строку
        message = input("Введите сообщение для отправки: ")

        if re.fullmatch("^[A-Za-z0-9]+$", message):
            isLatinNumString = True
        else:
            print("only Latin symbols and numbers")

    encoded_message, sec_key, open_key = williams_encode(message)

    decoded_message = williams_decode(encoded_message, sec_key, open_key)

    print("Декодированное сообщение: ", decoded_message)


if __name__ == '__main__':
    main()
