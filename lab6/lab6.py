from time import time
# from pyecm import factors
from math import log10, ceil
from gmpy2 import is_prime, f_div, mpz, mul, mpfr, is_odd, powmod, next_prime
from random import random


#задаем порядок чисел для поиска
dimension = 500

#Начальное простое число

start_prime = 3571

start_time = time()

current_number = mpz(start_prime)

current_prime = start_prime


list_primes = []

p = mpz(start_prime)

repit_flag = True

U = 0

for i in range(1000):
	# print(p.num_digits())
	print(i)
	while p.num_digits() <= dimension:
		if repit_flag:
			repit_flag = False
			N = f_div(mpz(10**(dimension-1)),mpz(current_prime)) + f_div(mpz(10**(dimension-1)*mpfr(random())),mpz(current_prime))
			N = N + 1 if N.is_odd() else N 
			U = 0
			# print(N)
			# print("suka!")
			# a = input()
		# print("U = "+ str(U))
		p = (N + U)*current_prime + 1
		# print(p)
		# a = input()
		if pow(2,p-1,p) == 1 and pow(2,N+U,p) != 1:
			print(p)
			list_primes.append(p)
			repit_flag = True
			break
		else:
			U += 2
	# print(p)
	current_prime = next_prime(current_prime)

	print()
	print("curr: "+ str(current_prime))

print("Time:")
print(time()-start_time)

summ = 0

for i in list_primes:
	if is_prime(i):
		summ += 1

print()
print(summ)