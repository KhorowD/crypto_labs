import primegen
import re
from primroot import primroot


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

def dh_encode(msg_to_encode):

    # переводим символы в числа
    numbers_list = convert_chars_to_int(msg_to_encode)

    print(numbers_list)

    # генерируем простые числа
    a_priv = primegen.prime_gen(40)
    b_priv = primegen.prime_gen(40)

    p = primegen.prime_gen(50)
    q = primroot(p)

    print(f"prime = {p}\n")

    print(f"primitive root = {q}\n")

    A_pub = pow(q, a_priv, p)
    B_pub = pow(q, b_priv, p)

    print(f"A_pub = {A_pub}, A_priv = {a_priv}\n")

    print(f"B_pub = {B_pub}, A_priv = {b_priv}\n")

    K_a = pow(B_pub, a_priv, p)
    K_b = pow(A_pub, b_priv, p)

    print(f"secret key = {K_a}\n")

    print("Use cesar for encoding with sec. key\n")
    encoded_num = [(num + K_a) % 255 for num in numbers_list]
    print(encoded_num)

    return convert_int_to_chars(encoded_num), K_a


def dh_decode(msg_to_decode, key):
    return convert_int_to_chars([(ord(ch) - key) % 255 for ch in msg_to_decode])


def main():

    isLatinNumString = False

    while isLatinNumString != True:

        # получаем входную строку
        message = input("Введите сообщение для отправки: ")

        if re.fullmatch("^[A-Za-z0-9]+$", message):
            isLatinNumString = True
        else:
            print("only Latin symbols and numbers")

    encoded_message, sec_key = dh_encode(message)

    print("Закодированное сообщение: " + encoded_message)

    decoded_message = dh_decode(encoded_message, sec_key)

    print("Декодированное сообщение: " + decoded_message)


if __name__ == '__main__':
    main()
