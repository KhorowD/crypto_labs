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


def gen_keys(dimension):
    """
    Функция, которая генерирует ключи абонента 

    """

    p = primegen.prime_gen(dimension)
    q = primegen.prime_gen(dimension)

    N = p * q

    phi = (p - 1) * (q - 1)

    d = primegen.prime_gen(dimension // 2)

    c = ext_gcd(d, phi)

    if c < 0:
        c = c % phi

    print((c * d) % phi)

    return c, d, N


def rsa_encode(msg_to_encode):

    # переводим символы в числа
    numbers_list = convert_chars_to_int(msg_to_encode)

    print(numbers_list)

    C_a, D_a, N_a = gen_keys(50)
    C_b, D_b, N_b = gen_keys(50)

    print(f"A keys c_a = {C_a},  d_a = {D_a}, N_a = {N_a}\n")
    print(f"B keys c_b = {C_b},  d_b = {D_b}, N_b = {N_b}\n")

    A_sig = [pow(num, C_a, N_a) for num in numbers_list]

    print("Sign")

    print(A_sig)

    encoded_list = [pow(num, D_b, N_b) for num in A_sig]
    print("Encoded")
    print(encoded_list)

    return encoded_list, C_b, D_a, N_a, N_b


def rsa_decode(msg_to_decode, key_b, pub_key_a, N_a, N_b):

    A_sig = [pow(num, key_b, N_b) for num in msg_to_decode]
    print("Sign")
    print(A_sig)
    return convert_int_to_chars([pow(num, pub_key_a, N_a) for num in A_sig])


def main():

    isLatinNumString = False

    while isLatinNumString != True:

        # получаем входную строку
        message = input("Введите сообщение для отправки: ")

        if re.fullmatch("^[A-Za-z0-9]+$", message):
            isLatinNumString = True
        else:
            print("only Latin symbols and numbers")

    encoded_message, sec_key_b, open_key_a, N_a, N_b = rsa_encode(message)

    decoded_message = rsa_decode(
        encoded_message, sec_key_b, open_key_a, N_a, N_b)

    print("Декодированное сообщение: " + decoded_message)


if __name__ == '__main__':
    main()
