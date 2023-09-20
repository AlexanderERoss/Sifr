# #############################################################################
# Test script to run through terminal: python testscript.py
# Tests various versions of the standard Western decimal Arabic numbering
# system comparing the sifr string with the number converted to string in the
# standard python
# #############################################################################

import logging
import multiprocessing
import time

from systems import SifrSystem
from systems import SifrScopeException
from sifr import Sifr
from decimal import Decimal, getcontext

# DEBUG, INFO, WARNING, ERROR, CRITICAL are the values for logging values
log_level = logging.WARNING
PRECISION = 20
TIMEOUT = 15000  # In milliseconds

logging.getLogger().setLevel(log_level)

s = SifrSystem(xcimal_places=PRECISION)

# Zero
a = Sifr('0', s)
# Sub one positive rational number
b = Sifr('0.96123724', s)
# Large positive rational number
c = Sifr('219.8459', s)
# Negative rational number
d = Sifr('-31.261234', s)
# Odd positive integer
e = Sifr('3', s)
# Even positive integer
f = Sifr('4', s)
# Negative integer
g = Sifr('-5', s)
# Double digit positive integer
h = Sifr('13', s)

# Set precision for decimals
getcontext().prec = PRECISION

ad = Decimal('0.0')
bd = Decimal('0.96123724')
cd = Decimal('219.8459')
dd = Decimal('-31.261234')
ed = Decimal('3.0')
fd = Decimal('4.0')
gd = Decimal('-5.0')
hd = Decimal('13.0')


number_link = {ad: a,
               bd: b,
               cd: c,
               dd: d,
               ed: e,
               fd: f,
               gd: g,
               hd: h}


class ExcessTimeException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


def time_tester(test_func):
    def wrapper(*args):
        start_time = time.time()
        proc = multiprocessing.Process(target=test_func, args=[*args])
        proc.start()
        proc.join(TIMEOUT/1000)
        end_time = time.time()
        try:
            if not proc.is_alive():
                print("  Time taken: " + str(end_time - start_time)
                      + " seconds\n")
            else:
                proc.terminate()
                print('    TIMEOUT')
                raise ExcessTimeException('   Timeout of ' + str(TIMEOUT)
                                          + 'ms exceeded\n')
        except ExcessTimeException as ete:
            print(ete.message)
        return proc
    return wrapper


def dec_mod(n1, n2):
    '''Fixes decimals poorlly functioning modulus function'''
    dec_zero = Decimal('0')
    n1_neg = n1 < dec_zero
    n2_neg = n2 < dec_zero

    base_mod = n1 % n2
    divs_exactly = base_mod == dec_zero
    if not divs_exactly and ((n1_neg and not n2_neg) or
                             (n2_neg and not n1_neg)):
        return (n1 % n2) + n2
    else:
        return n1 % n2


def dec_floordiv(n1, n2):
    '''Fixes decimals poorlly functioning modulus function'''
    base_div = n1 / n2
    base_floordiv = n1 // n2
    if base_div < Decimal('0') and base_div != base_floordiv:
        return base_floordiv - Decimal('1')
    else:
        return base_floordiv


unary_link = {'abs': (Decimal.__abs__, Sifr.__abs__),
              'neg': (Decimal.__neg__, Sifr.__neg__),
              'pos': (Decimal.__pos__, Sifr.__pos__)
              }

arith_link = {'add': (Decimal.__add__, Sifr.__add__),
              'sub': (Decimal.__sub__, Sifr.__sub__),
              'mul': (Decimal.__mul__, Sifr.__mul__),
              'floordiv': (dec_floordiv, Sifr.__floordiv__),
              'mod': (dec_mod, Sifr.__mod__),
              'truediv': (Decimal.__truediv__, Sifr.__truediv__),
              'pow': (Decimal.__pow__, Sifr.__pow__)
              }

compare_link = {'eq': (Decimal.__eq__, Sifr.__eq__),
                'gt': (Decimal.__gt__, Sifr.__gt__),
                'lt': (Decimal.__lt__, Sifr.__lt__),
                'ge': (Decimal.__ge__, Sifr.__ge__),
                'le': (Decimal.__le__, Sifr.__le__)
                }


def decimal_formater(decml):
    formatted = s._norm_ans(('{:.' + str(PRECISION//2) + 'f}').format(decml))
    # formatted = formatted if formatted != '-0.0' else '0.0'
    return formatted


# Test functions
@time_tester
def unary_tester(sifr, sifr_op, num, num_op):
    try:
        sifr_result = sifr_op(sifr).round(PRECISION//2).sifr
        float_result = decimal_formater(num_op(num))
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


@time_tester
def binary_tester(sifr1, sifr2, sifr_op, num1, num2, num_op):
    try:
        sifr_result = sifr_op(sifr1, sifr2).round(PRECISION//2).sifr
        float_result = decimal_formater(num_op(num1, num2))
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


@time_tester
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
