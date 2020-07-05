import primegen
import re
from random import randint
from sympy.ntheory import legendre_symbol, jacobi_symbol


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


def gen_keys(dimension):
    """
    Функция, которая генерирует ключи абонента 

    """

    p = primegen.prime_gen(dimension)

    while p % 4 != 3:
        p = primegen.prime_gen(dimension)

    q = primegen.prime_gen(dimension)

    while q % 4 != 3:
        q = primegen.prime_gen(dimension)

    N = p * q

    for i in range(2, N - 1):
        s = jacobi_symbol(i, N)
        if s == -1:
            s = i
            break

    k = ((p - 1) * (q - 1) // 4 + 1) // 2

    return (p, q), N, k, s


def williams_encode(msg_to_encode):

    # переводим символы в числа
    numbers_list = convert_chars_to_int(msg_to_encode)

    print(numbers_list)

    int_m = make_number_to_encode(numbers_list)
    print(f"converted message = {int_m}")

    sec_keys, n, K, S = gen_keys(100)

    print(f"sec keys = {sec_keys}")

    print(f"N = {n}")

    print(f"K = {K}")

    print(f"S = {S}")

    print(f"message = {int_m}")
    J = jacobi_symbol(int_m, n)

    C_1 = 1 if J == -1 else 0

    M = (pow(S, C_1, n) * int_m) % n

    C_2 = M % 2

    C = pow(M, 2, n)

    print(f"Закодированное сообщение ({C}, {C_1}, {C_2})")

    return (C, C_1, C_2), n, K, S


def williams_decode(msg_to_decode, N, key, S):

    MM = pow(msg_to_decode[0], key, N)

    print(f"M = {MM}")

    if (msg_to_decode[2] == 1) and (MM % 2 == 0):
        MM = -MM % N
    if (msg_to_decode[2] == 0) and (MM % 2 == 1):
        MM = -MM % N

    M_dec1 = (pow(S, -(msg_to_decode[1]), N) * MM) % N
    # M_dec2 = (pow(S,-(msg_to_decode[1]),N)*(-MM))%N

    print(f"decoded number = {M_dec1}")

    return convert_int_to_chars(div_str_to_numbers(M_dec1))


def main():

    isLatinNumString = False

    while isLatinNumString != True:

        # получаем входную строку
        message = input("Введите сообщение для отправки: ")

        if re.fullmatch("^[A-Za-z0-9]+$", message):
            isLatinNumString = True
        else:
            print("only Latin symbols and numbers")

    encoded_message, N_open, sec_key, S_open = williams_encode(message)

    decoded_message = williams_decode(encoded_message, N_open, sec_key, S_open)

    print("Декодированное сообщение: ", decoded_message)


if __name__ == '__main__':
    main()
