import time
import math

t = time.monotonic()
n = 10000

# simple = True
#
# for i in range(2, n+1):
#     for j in range(2, int(math.sqrt(i))+1):
#         if i % j == 0:
#             simple = False
#             break
#     if simple:
#         print(i)
#
#     simple = True
# end = time.monotonic()
# print(end-t)


# # n = 10
# prime = [1] * n
# # for i in range(0,n+1):
# #    prime[i] = 1
#
# prime[1] = 0
# prime[0] = 0
# for i in range(2, n):
#     if (i * i <= n and prime[i]):
#         for j in range(i * i, n, i):
#             prime[j] = 0
#
# for i in range(0, n):
#     if prime[i]:
#         print(i)

# for n in range(2, 10000):
#     for x in range(2, n):
#         if n % x == 0:
#             # print(n, 'equals', x, '*', n//x)
#             break
#     else:
#         # loop fell through without finding a factor
#         print(n)



def is_prime(nb: int) -> bool:
    if nb >= 2:
        if nb % 2 == 0 and nb != 2:
            return False
        i = 3
        while(i*i <= nb):
            if nb % i == 0:
                return False
            i = i+2
        return True
    return False


# start = time.monotonic()
for i in range(2, n):
    if is_prime(i):
        print(i)
# end = time.monotonic()
# print(end-start)

end = time.monotonic()
print(end - t)
