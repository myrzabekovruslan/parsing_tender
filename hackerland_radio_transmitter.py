#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'hackerlandRadioTransmitters' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER_ARRAY x
#  2. INTEGER k
#

def hackerlandRadioTransmitters(x, k, n):
    x.sort()
    a = [0, *x, 0]
    ans, i = 0, 1
    while (i <= n):
        maxijabe = a[i] + k
        j = i
        ans = ans + 1
        while (j <= n and a[j] <= maxijabe):
            i = j
            j += 1

        maxijabe = a[i] + k
        j = i
        while (j <= n and a[j] <= maxijabe):
            i = j
            j += 1

        i = i + 1
    print(ans)
    return ans

if __name__ == '__main__':

    first_multiple_input = input().rstrip().split()

    n = int(first_multiple_input[0])

    k = int(first_multiple_input[1])

    x = list(map(int, input().rstrip().split()))

    result = hackerlandRadioTransmitters(x, k, n)
