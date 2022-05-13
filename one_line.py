pair = list(map(int, input().rstrip().split()))

# for i in range(pair[0]): [print(i*pair[1]+j, end=' ') if j != pair[1] else print(i*pair[1]+j) for j in range(1, pair[1]+1)[::-1]]
for i in range(pair[0]): [print(i*pair[1]+k, end=' ') if k != 1 else print(i*pair[1]+k) for k in range(pair[1], 0, -1)] if i % 2 == 1 else [print(i*pair[1]+j, end=' ') if j != pair[1] else print(i*pair[1]+j) for j in range(1, pair[1]+1)]

# for i in range(10): 2 if 2 > 1 else 1