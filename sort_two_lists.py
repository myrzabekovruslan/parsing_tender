import time

a = [1,4,6,8,9,10] + [10]*100000 + [11] * 100000
b = [1,2,5,6,7,8] + [9] * 100000 + [12] * 100000
c = []
d = []
start = time.time_ns()
i = 0
j = 0
while True:
    try:
        if a[i] < b[j]:
            c.append(a[i])
            i += 1
        else:
            c.append(b[j])
            j += 1
    except:
        if i == len(a):
            c += b[j:]
        else:
            c += a[i:]
        break
stop = time.time_ns()
print(stop - start)

start = time.time_ns()
i = 0
j = 0
len_a = len(a)
len_b = len(b)
while True:
    if a[i] < b[j]:
        d.append(a[i])
        i += 1
        if i == len_a:
            d += b[j:]
            break
    else:
        d.append(b[j])
        j += 1
        if j == len_b:
            d += a[i:]
            break

stop = time.time_ns()
print(stop - start)

# print(c)
# print(d)