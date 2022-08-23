#!/usr/bin/env python3
#
# float_strata_count.py
# Count bit patterns organized into fields.
#
# Author: Sreepathi Pai

# a bit pattern is a string with '10X' where X is dont-care
import unittest

def count_patterns(x):
    dontcare = 0
    length = 0

    for c in x:
        if c == '0' or c == '1':
            length += 1
        elif c == 'X':
            length += 1
            dontcare += 1
        elif c == ' ': # for readability
            pass
        else:
            raise ValueError(f"Illegal character '{c}', must be 10X")

    assert length > 0

    # total patterns = 2^length / 2^(length - dontcare)
    # which after simplification is:

    return 2 ** dontcare

class TestCountPatterns(unittest.TestCase):
    def test_count_patterns(self):
        self.assertEqual(count_patterns('X'), 2)
        self.assertEqual(count_patterns('10'), 1)
        self.assertEqual(count_patterns('XX'), 4)

class float_counts():
    ZEROES = 'X  0000 0000  000 0000 0000 0000 0000 0000'

    # at least 1 in the significand
    SUBNORMALS = 'X  0000 0000  XXX XXXX XXXX XXXX XXXX XXXX'

    INF = 'X 1111 1111 000 0000 0000 0000 0000 0000'
    NAN = 'X 1111 1111 XXX XXXX XXXX XXXX XXXX XXXX'

    NORMALS_1    = 'X  XXXX XXXX  XXX XXXX XXXX XXXX XXXX XXXX'
    #OT_NORMAL_1 = 'X  0000 0000  XXX XXXX XXXX XXXX XXXX XXXX' # zero/subnormals
    #OT_NORMAL_2 = 'X  1111 1111  XXX XXXX XXXX XXXX XXXX XXXX' # inf/nans

    nZEROES = count_patterns(ZEROES)
    nSUBNORMALS = count_patterns(SUBNORMALS) - 2 # for all zeros significand
    nNORMALS_1 = count_patterns(NORMALS_1)
    nINF = count_patterns(INF)
    nNAN = count_patterns(NAN) - 2 # for all zeroes significand
    nNORMALS = nNORMALS_1 - (nZEROES + nSUBNORMALS + nINF + nNAN)

    print(nZEROES)
    print(nINF)
    print(nNAN)
    print(nSUBNORMALS)
    print(nNORMALS)

    print(sum([nZEROES, nINF, nNAN, nNORMALS, nSUBNORMALS]), 2**32)

# generation: https://cs.stackexchange.com/questions/67664/prng-for-generating-numbers-with-n-set-bits-exactly

float_counts()
