import primegen
import re
from random import randint


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

    return (p, q), N


def rabin_encode(msg_to_encode):

    # переводим символы в числа
    numbers_list = convert_chars_to_int(msg_to_encode)

    print(numbers_list)

    int_m = make_number_to_encode(numbers_list)
    print(int_m)

    sec_a, N_a = gen_keys(100)
    # sec_b, N_b = gen_keys(100)

    print(f"A keys sec_a = {sec_a}, N_a = {N_a}\n")
    # print(f"B keys sec_b = {sec_b}, N_b = {N_b}\n")

    encoded_m = (int_m**2) % N_a

    print(encoded_m)

    return encoded_m, int_m, sec_a, N_a


def rabin_decode(msg_to_decode, key_a, N):

    y_p, y_q = ext_gcd(key_a[0], key_a[1])

    m_p = pow(msg_to_decode, (key_a[0] + 1) // 4, key_a[0])
    m_q = pow(msg_to_decode, (key_a[1] + 1) // 4, key_a[1])

    r_1 = (y_p * key_a[0] * m_q + y_q * key_a[1] * m_p) % N

    r_2 = N - r_1

    r_3 = (y_p * key_a[0] * m_q - y_q * key_a[1] * m_p) % N

    r_4 = N - r_3

    return (r_1, r_2, r_3, r_4)


def main():

    isLatinNumString = False

    while isLatinNumString != True:

        # получаем входную строку
        message = input("Введите сообщение для отправки: ")

        if re.fullmatch("^[A-Za-z0-9]+$", message):
            isLatinNumString = True
        else:
            print("only Latin symbols and numbers")

    encoded_message, number_message, sec_key_a, N_open = rabin_encode(message)

    decoded_message = rabin_decode(encoded_message, sec_key_a, N_open)

    # print("Декодированное сообщение: ", decoded_message)

    print("All calculated roots\n")

    print(f"r1 = {decoded_message[0]}\n")
    print(f"r2 = {decoded_message[1]}\n")
    print(f"r3 = {decoded_message[2]}\n")
    print(f"r4 = {decoded_message[3]}\n")

    for num in decoded_message:
        if num == number_message:
            print(
                f"decoded message: {convert_int_to_chars(div_str_to_numbers(num))}")


if __name__ == '__main__':
    main()
