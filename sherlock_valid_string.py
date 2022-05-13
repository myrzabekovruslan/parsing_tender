#!/bin/python3

import math
import os
import random
import re
import sys
import collections
import itertools
import string
#
# Complete the 'isValid' function below.
#
# The function is expected to return a STRING.
# The function accepts STRING s as parameter.
#

def isValid(s):
    # Write your code here
    cnt = collections.Counter(s)
    cnt2 = collections.Counter(list(cnt.values()))
    if len(list(cnt2.values())) > 2:
        return 'NO'
    elif len(list(cnt2.values())) == 2:
        key1, key2 = cnt2.keys()
        if cnt2[key1] == 1 and (key1 - 1 == key2 or key1 - 1 == 0):
            return 'YES'
        elif cnt2[key2] == 1 and (key2 - 1 == key1 or key2 - 1 == 0):
            return 'YES'
        else:
            return 'NO'
    else:
        return 'YES'


if __name__ == '__main__':
    s = input()

    result = isValid(s)

    print(result)