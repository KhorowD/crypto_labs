
from sympy.ntheory import legendre_symbol


def find_powers_two(num):
    """Функция поиска степеней двойки, которые содержатся в числе"""
    if num % 2 == 1:
        return 0, num

    power = 0

    while num % 2 != 1:
        num //= 2
        power += 1

    return power, num


def sqrt_mod(n, p):
    """Алгоритм вычисления квадратного корня по модулю (реализация Алгоритма Тонелли-Шэнкса)"""
    if p <= 3:
        raise Exception("p must be > 3")

    S, Q = find_powers_two(p - 1)

    # print(f"S = {S}, Q = {Q}")

    if S == 0:
        raise Exception("p should be odd prime")

    if S == 1 and p % 4 == 3:
        R = pow(n, (p + 1) // 4, p)

        return R % p, p - R

    if S >= 2:

        # Ищем произвольный квадратичный невычет
        z = 1
        while legendre_symbol(z, p) != -1:
            z += 1

        # print(f"z = {z}")

        c = pow(z, Q, p)

        # print(f"c = {c}")

        R = pow(n, (Q + 1) // 2, p)

        # print(f"R = {R}")

        t = pow(n, Q, p)

        # print(f"t = {t}")

        M = S

        # print(f"M = {M}\n")

        while True:
            # print(f"t= {t}")
            # a = input()
            if t == 1:
                return R, p - R

            if t == 0:
                return 0

            for i in range(1, M):
                tt = pow(t, 2**i, p)
                # print(f"tt = {tt}")
                # a = input()
                if tt == 1:
                    # print(f"itter_____")
                    b = pow(c, 2**(M - i - 1), p)
                    # print(f"b = {b}")
                    R = R * b % p
                    # print(f"R = {R}")
                    t = (t * ((b**2) % p)) % p
                    # print(f"t = {t}")
                    c = b**2 % p
                    # print(f"c = {c}")
                    M = i
                    # print(f"M = {M}")
                    break
