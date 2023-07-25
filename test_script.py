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
from decimal import Decimal, getcontext

# DEBUG, INFO, WARNING, ERROR, CRITICAL are the values for logging values
log_level = logging.WARNING
PRECISION = 12

logging.getLogger().setLevel(log_level)

s = SifrSystem(xcimal_places=PRECISION)

# Sub one positive rational number
a = Sifr('0.96123724', s)
# Large positive rational number
b = Sifr('219.8459', s)
# Negative rational number
c = Sifr('-31.261234', s)
# Odd positive integer
d = Sifr('3', s)
# Even positive integer
e = Sifr('4', s)
# Negative integer
f = Sifr('-5', s)

# Set precision for decimals
getcontext().prec = PRECISION*2

ad = Decimal('0.96123724')
bd = Decimal('219.8459')
cd = Decimal('-31.261234')
dd = Decimal('3.0')
ed = Decimal('4.0')
fd = Decimal('-5.0')


number_link = {ad: a,
               bd: b,
               cd: c,
               dd: d,
               ed: e,
               fd: f}

unary_link = {'abs': (Decimal.__abs__, Sifr.__abs__),
              'neg': (Decimal.__neg__, Sifr.__neg__),
              'pos': (Decimal.__pos__, Sifr.__pos__)
              }

arith_link = {'add': (Decimal.__add__, Sifr.__add__),
              'sub': (Decimal.__sub__, Sifr.__sub__),
              'mul': (Decimal.__mul__, Sifr.__mul__),
              'floordiv': (Decimal.__floordiv__, Sifr.__floordiv__),
              'mod': (Decimal.__mod__, Sifr.__mod__),
              'truediv': (Decimal.__truediv__, Sifr.__truediv__),
              'pow': (Decimal.__pow__, Sifr.__pow__)
              }

compare_link = {'eq': (Decimal.__eq__, Sifr.__eq__),
                'gt': (Decimal.__gt__, Sifr.__gt__),
                'lt': (Decimal.__lt__, Sifr.__lt__),
                'ge': (Decimal.__ge__, Sifr.__ge__),
                'le': (Decimal.__le__, Sifr.__le__)
                }


def float_formater(decml):
    formatted = s._norm_ans(('{:.' + str(PRECISION) + 'f}').format(decml))
    formatted = formatted.replace('-0.0', '0.0')
    return formatted


# Test functions
def unary_tester(sifr, sifr_op, num, num_op):
    try:
        sifr_result = sifr_op(sifr).sifr
        float_result = float_formater(num_op(num))
        try:
            assert sifr_result == float_result, \
                "Sifr result: " + sifr_result + \
                " is not equal to decimal result: " + \
                float_result
            print("    PASS")
            print("    Result: " + sifr_result)
        except AssertionError as aser:
            print("    FAIL")
            print("    " + str(aser))
    except SifrScopeException as sse:
        print("    OUT OF SCOPE")
        print("    " + sse.message)


def binary_tester(sifr1, sifr2, sifr_op, num1, num2, num_op):
    try:
        sifr_result = sifr_op(sifr1, sifr2).sifr
        float_result = float_formater(num_op(num1, num2))
        try:
            assert sifr_result == float_result, \
                "Sifr result: " + sifr_result + \
                " is not equal to decimal result: " + \
                float_result
            print("    PASS")
            print("    Result: " + sifr_result)
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
                " is not decimal result: " + \
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
