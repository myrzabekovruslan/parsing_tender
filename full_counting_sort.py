#!/bin/python3

import math
import os
import random
import re
import sys


#
# Complete the 'countSort' function below.
#
# The function accepts 2D_STRING_ARRAY arr as parameter.
#

def countSort(arr):
    for i in range(len(arr)//2):
        arr[i][1] = '-'
    for i in sorted(arr, key=lambda x: int(x[0])):
        print(i[1], end=' ')


if __name__ == '__main__':
    n = int(input().strip())

    arr = []

    for _ in range(n):
        arr.append(input().rstrip().split())

    countSort(arr)
