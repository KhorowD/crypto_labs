import primegen
import re
from primroot import primroot
from random import randint
import ellipticcurve as ec
from constants import curves


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


def gen_key_pair(prime, pnt):
    """
    Функция которая генерирует закрытый ключ и открытый из случайной точки выбранной на кривой
    """

    sec = randint(1, prime - 1)    # секретный ключ

    pub = pnt.mul(sec)  # Высчитываем открытый ключ из точки и секретного ключа

    return (pub, sec)


def elgamal_encode(msg_to_encode, curve_id):
    """
    Функция шифрования
    """

    numbers_list = convert_chars_to_int(
        msg_to_encode)  # Переводим символы в числа
    print(f"unicode table numbers: {numbers_list}\n")

    int_message = make_number_to_encode(
        numbers_list)   # Собираем число для кодирования
    print(f"converted values: {int_message}\n")

    curve_id_const = curves.get(curve_id)

    p = curve_id_const[0]
    a = curve_id_const[1]
    b = curve_id_const[2]
    q = curve_id_const[3]

    # p = primegen.prime_gen(50)  # Генерируем простое число

    # Создаем элиптическую кривую с заданными параметрами
    curve = ec.Curve(a, b, p)

    point = curve.random_point()    # и берем случайную точку с этой кривой

    print(f"Random point = {point}\n")

    # Генерируем ключи для пользователей А и В

    A_keys = gen_key_pair(q, point)

    B_keys = gen_key_pair(q, point)

    if int_message < p:     # Проверяем, не превосходит ли наше сообщение простое число

        K = randint(1, q - 1)  # Генерируем случайное число K

        # R = [k]*G  - Умножаем нашу случайную точку на K - 1-я часть шифротекста
        R = point.mul(K)

        # P = [K]*B_open_key  - Умножаем открытый ключ адресата В на число К
        P = B_keys[0].mul(K)

        e = int_message * P.x % p     # e = mx mod p - получаем 2-ую часть шифротекста

    else:
        raise Exception("message should be < than prime")

    return (R, e), B_keys, curve


def elgamal_decode(msg_to_decode, key, curve):

    Q = msg_to_decode[0].mul(key[1])  # Q = [B_sec_key]*R - вычисляем точку Q

    # m' = e/x mod p = e*x^(-1) mod p
    int_message_decoded = msg_to_decode[1] * \
        ec.invert(Q.x, curve.char) % curve.char

    return convert_int_to_chars(div_str_to_numbers(int_message_decoded))


def gen_curve():
    pass

def main():

    isLatinNumString = False

    while isLatinNumString != True:

        # получаем входную строку
        message = input("Введите сообщение для отправки: ")
        print()
        if re.fullmatch("^[A-Za-z0-9]+$", message):
            isLatinNumString = True
        else:
            print("only Latin symbols and numbers")

    isNotRightAnswer = True
    curve_number = 0

    while isNotRightAnswer:
        print("Какую кривую использовать?")
        print("[1], [2], [3]\n")

        answer = int(input("Введите число: "))

        if answer == 1 or answer == 2 or answer == 3:
            isNotRightAnswer = False
            curve_number = answer
        else:
            print("write a number 1, 2 or 3\n")

    encoded_message, sec_key, el_curve = elgamal_encode(message, curve_number)

    decoded_message = elgamal_decode(encoded_message, sec_key, el_curve)

    print("Декодированное сообщение: " + decoded_message)


if __name__ == '__main__':
    main()
