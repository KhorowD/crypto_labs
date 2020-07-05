from sympy.ntheory import isprime, jacobi_symbol, legendre_symbol
from math import gcd
import time
import sys
import pyecm

def generate_p_q():
    
    prime_number = 82
    start_prime = 367
    tmp = start_prime
    pq = []
    for i in range(2):
        
        while len(str(tmp)) < prime_number:
            N = 4 * tmp + 2
            U = 0
            candidate = 0
            while True:
                candidate = (N + U) * tmp + 1
                if pow(2, int(candidate - 1), int(candidate)) == 1 and pow(2, int(N + U), int(candidate)) != 1:
                    tmp = candidate
                    break
                else:
                    U = U - 2
        pq.append(tmp)
        start_prime = start_prime + 2
        while len(list(pyecm.factors(start_prime, False, True, 8, 1))) != 1:
            start_prime = start_prime + 2
        tmp = start_prime
    p = pq[0]
    q = pq[1]
    print("\np = {}, длина = {}".format(p, len(str(p))))
    print("\nq = {}, длина = {}".format(q, len(str(q))))
    return p,q

def binarn(x, y, N):
    if y == 0:
        return 1
    if y == -1:
        return 1. / x
    p = binarn(x, y // 2, N)
    p = (p * p)% N
    if y % 2:
        p = (p * x)% N
    return p

def exgcd(a, b):
    x, xx, y, yy = 1, 0, 0, 1
    while b:
        q = a // b
        a, b = b, a % b
        x, xx = xx, x - xx*q
        y, yy = yy, y - yy*q
    return x

def find_c(p, q):
    c = 2
    while ((legendre_symbol(c, p))%4 != (-p)%4) or ((legendre_symbol(c, q))%4 != (-q)%4):
        c += 1
    return c

def find_s(N, c):
    s = 2
    while (jacobi_symbol((s**2 - c), N) != (-1)) or (gcd(s, N) != 1):
        s += 1
    return s

def find_d(w):
    d = 2
    while (gcd(d, w) != 1):
        d += 1
    return d

def find_Xe_Ye(a, b, e):
    X = []
    Y = []
    X.append(1)
    X.append(a)
    Y.append(0)
    Y.append(b)
    for i in range (1, e//2+1):
        X.append(0)
        X.append(0)
        X.append(0)
        Y.append(0)
        Y.append(0)
        Y.append(0)
        X[2*i] = (2*X[i]**2 - 1)%N
        Y[2*i] = (2*X[i]*Y[i])%N
        X[2*i+1] = (2*X[i]*X[i+1] - X[1])%N
        Y[2*i+1] = (2*X[i]*Y[i+1] - Y[1])%N
    return X[e], Y[e]

#def modular_sqrt(a, p):
    """ Find a quadratic residue (mod p) of 'a'. p
        must be an odd prime.

        Solve the congruence of the form:
            x^2 = a (mod p)
        And returns x. Note that p - x is also a root.

        0 is returned is no square root exists for
        these a and p.

        The Tonelli-Shanks algorithm is used (except
        for some simple cases in which the solution
        is known from an identity). This algorithm
        runs in polynomial time (unless the
        generalized Riemann hypothesis is false).
    """
    """# Simple cases
    #
    if legendre_symbol(a, p) != 1:
        return 0
    elif a == 0:
        return 0
    elif p == 2:
        return 0
    elif p % 4 == 3:
        return pow(a, (p + 1) // 4, p)

    # Partition p-1 to s * 2^e for an odd s (i.e.
    # reduce all the powers of 2 from p-1)
    #
    s = p - 1
    e = 0
    while s % 2 == 0:
        s /= 2
        e += 1

    # Find some 'n' with a legendre symbol n|p = -1.
    # Shouldn't take long.
    #
    n = 2
    while legendre_symbol(n, p) != -1:
        n += 1

    # Here be dragons!
    # Read the paper "Square roots from 1; 24, 51,
    # 10 to Dan Shanks" by Ezra Brown for more
    # information
    #

    # x is a guess of the square root that gets better
    # with each iteration.
    # b is the "fudge factor" - by how much we're off
    # with the guess. The invariant x^2 = ab (mod p)
    # is maintained throughout the loop.
    # g is used for successive powers of n to update
    # both a and b
    # r is the exponent - decreases with each update
    #
    x = pow(a, (s + 1) / 2, p)
    b = pow(a, s, p)
    g = pow(n, s, p)
    r = e

    while True:
        t = b
        m = 0
        for m in xrange(r):
            if t == 1:
                break
            t = pow(t, 2, p)

        if m == 0:
            return x

        gs = pow(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m"""

start_time = time.time()

#подготовка ключей

#p, q = generate_p_q()
p = 19
q = 11

N = p * q
print("\nN = ", N)

c = find_c(p, q)
print("\nc = ", c)
#kor_cp = modular_sqrt(c,p)
#kor_cq = modular_sqrt(c,q)
#kor_c = kor_cp*kor_cq%N
kor_c = int(c**(1/2))
print(kor_c)

s = find_s(N, c)
print("\ns = ", s)

leg_p = legendre_symbol(c, p)
leg_q = legendre_symbol(c, q)

w = (p - leg_p)*(q - leg_q)*exgcd(4,N)
w = w % N
print("\nw = ", w)

d = find_d(w)
#d=16
print("\nЗакрытый ключ d = ", d)

e = (((w+1)//2)*exgcd(d, w)) % w
#e=23
print("\ne = ", e)

#шифрование

M = int(input("Введите сообщение для шифрования: "))
M = M % N
print("Сообщение для шифрования: ", M)

b1 = 0
gamma = 0
jac = jacobi_symbol((M**2 - c), N)
if jac == 1:
    b1 = 0
    #gamma = (M + kor_c)
    #gamma_sopr = (M - kor_c)
    a = (M**2 + c)*exgcd((M**2 - c), N) % N
    b = 2*M*exgcd((M**2 - c), N) % N
    b2 = a % 2
if jac == -1:
    b1 = 1
    #gamma = (M*s + c)%N + ((M + s)%N)*kor_c
    #gamma_sopr = (M*s + c)%N - ((M + s)%N)*kor_c
    a = (((M**2 + c)*(s**2 + c) + 4*c*M*s)*exgcd(((M**2 - c)*(s**2 - c)),N)) % N
    b = ((2*s*(M**2 + c)+2*M*(s**2 + c))*exgcd((M**2 - c)*(s**2 - c), N)) % N
    b2 = a % 2
if jac == 0:
    print("Символ Якоби = 0!")
    sys.exit()
print("\na = ", a)
print("\nb = ", b)
print("\nb2 = ", b2)
print("\nb1 = ", b1)

#alfa = gamma*exgcd(gamma_sopr,N)% N
#alfa = gamma//gamma_sopr
alfa = (a + b*kor_c)%N
print("\nalfa = ", alfa)
alfa_minus = (a - b*kor_c)%N
print("\nalfa_minus = ", alfa_minus)

Xe, Ye = find_Xe_Ye(a, b, e)

#Xe = ((binarn(alfa, e, N) + binarn(alfa_minus, e, N))*exgcd(2, N))% N
print("\nXe = ", Xe)
#Ye = ((binarn(alfa, e, N) - binarn(alfa_minus, e, N))%N)*exgcd(2*kor_c, N)
print("\nYe = ", Ye)
E = Xe * exgcd(Ye, N) % N
print("\nE = ", E)

#дешифрование

a_alfa = ((E**2 + c)*exgcd(E**2 - c,N))%N
b_alfa = (2*E*exgcd(E**2 - c,N))%N
alfa_2e = (a_alfa + b_alfa*kor_c)%N
print("\nalfa_2e = ", alfa_2e)
print("\nalfa_2e_a = ", a_alfa)
print("\nalfa_2e_b = ", b_alfa)
alfa_2e_minus = (a_alfa - b_alfa*kor_c)%N
print("\nalfa_2e_minus = ", alfa_2e_minus)

Xd, Yd = find_Xe_Ye(a_alfa, b_alfa, d)

#Xd = ((binarn(alfa_2e, d, N) + binarn(alfa_2e_minus, d, N))*exgcd(2, N))% N
print("\nXd = ", Xd)

#Yd = ((binarn(alfa_2e, d, N) - binarn(alfa_2e_minus, d, N))*exgcd(2*kor_c, N))
#Yd = ((binarn(alfa_2e, d, N) - binarn(alfa_2e_minus, d, N))*exgcd(2, N))%N
print("\nYd = ", Yd)

alfa_2ed = (Xd + Yd*kor_c)%N
#alfa_2ed = Xd + Yd
print("\nalfa_2ed = ", alfa_2ed)

alfa_shtrih_a = Xd
alfa_shtrih_b = Yd
    
if b2 == 1:
    alfa_shtrih_a = N - alfa_shtrih_a
    alfa_shtrih_b = N - alfa_shtrih_b
    
alfa_shtrih = (alfa_shtrih_a + alfa_shtrih_b * kor_c)%N

if b1 == 1:
    alfa_shtrih_a = (alfa_2ed*(s**2 + c))*exgcd(s**2 - c, N)% N
    alfa_shtrih_b = (alfa_2ed*2*s*exgcd(s**2 - c, N))%N
print("\nalfa_shtrih = ", alfa_shtrih)
print("\nalfa_shtrih_a = ", alfa_shtrih_a)
print("\nalfa_shtrih_b = ", alfa_shtrih_b)

u = alfa_shtrih_a+1
v = alfa_shtrih_a-1
x = alfa_shtrih_b

M2 = kor_c*((u*v - x**2*c)*exgcd(v**2-x**2*c, N)%N) + c*x*(v-u)*exgcd(v**2-x**2*c, N)%N
#M2 = (((alfa_shtrih_a+1+alfa_shtrih_b*kor_c)*exgcd(alfa_shtrih_a-1+alfa_shtrih_b*kor_c, N))% N)*kor_c
print("\nM2 = ", M2)   

print('\nЗатраченное время =', time.time()-start_time)
