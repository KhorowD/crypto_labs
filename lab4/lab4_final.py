import gmpy2
import pyecm
from random import randint
import time
from math import pi


def is_square_free(n):
    prime_list = list(pyecm.factors(n, False, True, 8, 1))
    print(prime_list)
    for i in range(len(prime_list) - 1):
        if prime_list[i] == prime_list[i + 1]:
            return False
    return True


N = 10**50

M = 1000


# for avg_time
summ = 0

start_time = time.time()

for i in range(10):
    a = randint(1, N)
    print(a)
    if is_square_free(a):
        summ += 1
    else:
        summ += 0

print()
print("empir_val" + str(summ / M))
# print(list(pyecm.factors(a,False,True, 10, 1)))
print("theor_val " + str(6 / pi**2))
print(time.time() - start_time)
