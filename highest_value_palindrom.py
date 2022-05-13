#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'highestValuePalindrome' function below.
#
# The function is expected to return a STRING.
# The function accepts following parameters:
#  1. STRING s
#  2. INTEGER n
#  3. INTEGER k
#

def highestValuePalindrome(s, n, k):
    # Write your code here
    i = 0
    s_sered = len(s) // 2
    new_s = ''
    num_not_equal = 0
    error = False
    while i < s_sered:
        if s[i] != s[len(s)-1-i]:
            if s[i] == '9':
                new_s += s[i]
                num_not_equal += 1
            elif s[len(s)-1-i] == '9':
                new_s += s[len(s)-1-i]
                num_not_equal += 1
            else:
                num_not_equal += 2
                new_s += '9'

            if k < num_not_equal:
                error = True
                break
        else:
            new_s += s[i]
        i += 1

    print(new_s)
    print(k, num_not_equal)

    if error:
        i = 0
        s_sered = len(s) // 2
        new_s = ''
        num_not_equal = 0
        while i < s_sered:
            if s[i] != s[len(s) - 1 - i]:
                num_not_equal += 1
                if k >= num_not_equal:
                    if int(s[i]) > int(s[len(s) - 1 - i]):
                        new_s += s[i]
                    else:
                        new_s += s[len(s) - 1 - i]
                else:
                    return -1
            else:
                new_s += s[i]
            i += 1

    print(new_s)
    print(k, num_not_equal)
    i = 0
    new_ss = ''
    remain_k = k - num_not_equal
    while i < len(new_s) and remain_k >= 2:
        if new_s[i] != '9':
            new_ss += '9'
            remain_k -= 2
        i += 1

    new_ss += new_s[i:]
    if len(s) % 2 == 1:
        if remain_k >= 1:
            new_ss += '9'
        else:
            new_ss += s[s_sered]

    if len(s) % 2 == 1:
        return new_ss + new_ss[-2::-1]
    else:
        return new_ss + new_ss[::-1]


if __name__ == '__main__':

    first_multiple_input = input().rstrip().split()

    n = int(first_multiple_input[0])

    k = int(first_multiple_input[1])

    s = input()

    result = highestValuePalindrome(s, n, k)

    print(result)