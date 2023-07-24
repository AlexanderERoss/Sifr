# #############################################################################
# Test script to run through terminal: python testscript.py
# Tests various versions of the standard Western decimal Arabic numbering
# system comparing the sifr string with the number converted to string in the
# standard python
# #############################################################################

import logging

from systems import SifrSystem
from systems import SifrScopeException
from sifr import Sifr

# DEBUG, INFO, WARNING, ERROR, CRITICAL are the values for logging values
log_level = logging.WARNING
PRECISION = 12

logging.getLogger().setLevel(log_level)

s = SifrSystem(xcimal_places=PRECISION)

# Sub one positive rational number
a = Sifr('0.96123724', s)
# Large positive rational number
b = Sifr('2192.8459', s)
# Negative rational number
c = Sifr('-31.261234', s)
# Odd positive integer
d = Sifr('3', s)
# Even positive integer
e = Sifr('4', s)
# Negative integer
f = Sifr('-5', s)

ad = 0.96123724
bd = 2192.8459
cd = -31.261234
dd = 3.0  # Declare as float to ensure only one type of function for all
ed = 4.0  # Declare as float to ensure only one type of function for all
fd = -5.0  # Declare as float to ensure only one type of function for all

number_link = {ad: a,
               bd: b,
               cd: c,
               dd: d,
               ed: e,
               fd: f}

unary_link = {'abs': (float.__abs__, Sifr.__abs__),
              'neg': (float.__neg__, Sifr.__neg__),
              'pos': (float.__pos__, Sifr.__pos__)
              }

arith_link = {'add': (float.__add__, Sifr.__add__),
              'sub': (float.__sub__, Sifr.__sub__),
              'mul': (float.__mul__, Sifr.__mul__),
              'floordiv': (float.__floordiv__, Sifr.__floordiv__),
              'mod': (float.__mod__, Sifr.__mod__),
              'truediv': (float.__truediv__, Sifr.__truediv__),
              'pow': (float.__pow__, Sifr.__pow__)
              }

compare_link = {'eq': (float.__eq__, Sifr.__eq__),
                'gt': (float.__gt__, Sifr.__gt__),
                'lt': (float.__lt__, Sifr.__lt__),
                'ge': (float.__ge__, Sifr.__ge__),
                'le': (float.__le__, Sifr.__le__)
                }


# Test functions
def unary_tester(sifr, sifr_op, num, num_op):
    try:
        sifr_result = sifr_op(sifr)
        float_result = num_op(num)
        try:
            assert sifr_result.sifr == str(round(float_result, PRECISION)), \
                "Sifr result: " + sifr_result.sifr + \
                " is not equal to float result: " + \
                str(round(float_result, PRECISION))
            print("    PASS")
            print("    Result: " + sifr_result.sifr)
        except AssertionError as aser:
            print("    FAIL")
            print("    " + str(aser))
    except SifrScopeException as sse:
        print("    OUT OF SCOPE")
        print("    " + sse.message)


def binary_tester(sifr1, sifr2, sifr_op, num1, num2, num_op):
    try:
        sifr_result = sifr_op(sifr1, sifr2)
        float_result = num_op(num1, num2)
        try:
            assert sifr_result.sifr == str(round(float_result, PRECISION)), \
                "Sifr result: " + sifr_result.sifr + \
                " is not equal to float result: " + \
                str(round(float_result, PRECISION))
            print("    PASS")
            print("    Result: " + sifr_result.sifr)
        except AssertionError as aser:
            print("    FAIL")
            print("    " + str(aser))
    except SifrScopeException as sse:
        print("    OUT OF SCOPE")
        print("    " + sse.message)


def rel_tester(sifr1, sifr2, sifr_op, num1, num2, num_op):
    try:
        sifr_result = sifr_op(sifr1, sifr2)
        float_result = num_op(num1, num2)
        try:
            assert sifr_result == float_result, \
                "Sifr result: " + str(sifr_result) + \
                " is not float result: " + \
                str(float_result)
            print("    PASS")
            print("    Result: " + str(sifr_result))
        except AssertionError as aser:
            print("    FAIL")
            print("    " + str(aser))
    except SifrScopeException as sse:
        print("    OUT OF SCOPE")
        print("    " + sse.message)


# BRUTE FORCE TESTING SCRIPT
# Unary tests
for funct in unary_link:
    for num in number_link:
        print("Testing the function: " + funct + " with number: " + str(num))
        unary_tester(number_link[num],
                     unary_link[funct][1],
                     num,
                     unary_link[funct][0]
                     )

# Binary function tests
for funct in arith_link:
    for num1 in number_link:
        for num2 in number_link:
            print("Testing the function: " + funct + " with numbers: "
                  + str(num1) + " and " + str(num2))
            binary_tester(number_link[num1],
                          number_link[num2],
                          arith_link[funct][1],
                          num1,
                          num2,
                          arith_link[funct][0]
                          )

# Comparison tests
for funct in compare_link:
    for num1 in number_link:
        for num2 in number_link:
            print("Testing the function: " + funct + " with numbers: "
                  + str(num1) + " and " + str(num2))
            rel_tester(number_link[num1],
                       number_link[num2],
                       compare_link[funct][1],
                       num1,
                       num2,
                       compare_link[funct][0]
                       )
