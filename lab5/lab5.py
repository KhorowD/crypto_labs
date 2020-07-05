import time

N = 2019
a = 2019
z = 10**2019
start_time = time.time()
for i in range(N):
    print(i)
    time_begin = time.time()
    a = a ** N
    a = a % z
    print(time.time() - time_begin)


print(a)
print('Затраченное время = ', time.time() - start_time)
