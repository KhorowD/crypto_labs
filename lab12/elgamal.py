import primegen
import re
from primroot import primroot
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


def gen_open_keys(dimension):
    """
    Функция, которая генерирует пару общих ключей 

    """
    large_prime = primegen.prime_gen(dimension)
    primitive_root = primroot(large_prime)

    while primitive_root == -1:
        large_prime = primegen.prime_gen(dimension)
        primitive_root = primroot(large_prime)

    return large_prime, primitive_root


def gen_key_pair(prime, root):
    """
    Функция, которая генерирует пару ключей для каждого пользователя
    """

    first = randint(1, prime - 1)
    second = pow(root, first, prime)

    return first, second


def elgamal_encode(msg_to_encode):

    # переводим символы в числа
    numbers_list = convert_chars_to_int(msg_to_encode)

    print(numbers_list)

    p, q = gen_open_keys(70)

    C_a, D_a = gen_key_pair(p, q)
    C_b, D_b = gen_key_pair(p, q)

    print(f"prime = {p}, primitive root = {q}")
    print(f"A pair c_a = {C_a},  d_a = {D_a}\n")
    print(f"B pair c_b = {C_b},  d_b = {D_b}\n")

    encoded_pairs_list = []

    for num in numbers_list:
        k = randint(1, p - 2)
        r = pow(q, k, p)
        e = (num * pow(D_b, k, p)) % p
        encoded_pairs_list.append((r, e))

    print("Последовательность пар чисел (r, e)\n")
    for i in encoded_pairs_list:
        print(f"{i[0]}, {i[1]}")

    print()

    return encoded_pairs_list, C_b, p


def elgamal_decode(msg_to_decode, key, p):
    return convert_int_to_chars([((tupl[1] * pow(tupl[0], (p - 1 - key), p)) % p) for tupl in msg_to_decode])


def main():

    isLatinNumString = False

    while isLatinNumString != True:

        # получаем входную строку
        message = input("Введите сообщение для отправки: ")

        if re.fullmatch("^[A-Za-z0-9]+$", message):
            isLatinNumString = True
        else:
            print("only Latin symbols and numbers")

    encoded_message, sec_key, prime = elgamal_encode(message)

    decoded_message = elgamal_decode(encoded_message, sec_key, prime)

    print("Декодированное сообщение: " + decoded_message)


if __name__ == '__main__':
    main()
