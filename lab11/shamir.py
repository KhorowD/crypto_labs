import primegen
import re
from sympy import gcd


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
    return x


def gen_key_pair(prime):
    """
    Функция, которая генерирует пару ключей a,b такую, что:

    a*b mod (p-1) = 1

    При этом, сначала находим a: a mod (p-1) = 1
    Затем находим b при помощи расширенного алгоритма Евклида.

    """

    first = primegen.prime_gen(50)
    second = 0

    while gcd(first, prime - 1) != 1:
        first = primegen.prime_gen(50)

    second = ext_gcd(first, prime - 1)

    return first, second % (prime - 1)


def shamir_encode(msg_to_encode):
    """
    Функция кодирования

    """

    # переводим символы в числа
    numbers_list = convert_chars_to_int(msg_to_encode)

    int_m = make_number_to_encode(numbers_list)

    p = primegen.prime_gen(100)

    C_a, D_a = gen_key_pair(p)
    C_b, D_b = gen_key_pair(p)

    print(f"prime = {p}")
    print(f"A pair c_a = {C_a},  d_a = {D_a}\n")
    print(f"B pair c_b = {C_b},  d_b = {D_b}\n")

    print("********************")
    print("Converted message: ", int_m)
    print("********************")

    print(f"1. A->B: ")

    int_m = pow(int_m, C_a, p)
    print(int_m)

    print(f"2. B->A: ")

    int_m = pow(int_m, C_b, p)
    print(int_m)

    print(f"3. A->B (finaly encoded): ")

    int_m = pow(int_m, D_a, p)
    print(int_m)

    # Возвращаем зашифрованное сообщение, ключ для дешифровки и простое число
    return int_m, D_b, p


def shamir_decode(msg_to_decode, key, p):
    """
    Функция декодирования

    """

    return div_str_to_numbers(pow(msg_to_decode, key, p))


def main():

    isLatinNumString = False

    while isLatinNumString != True:

        message = input("Enter message: ")  # получаем входную строку

        if re.fullmatch("^[A-Za-z0-9]+$", message):
            isLatinNumString = True
        else:
            print("only Latin symbols and numbers")

    encoded_message, sec_key, prime = shamir_encode(message)

    decoded_message = shamir_decode(encoded_message, sec_key, prime)

    decoded_message = convert_int_to_chars(decoded_message)

    print("Decoded message: " + decoded_message)


if __name__ == '__main__':
    main()
