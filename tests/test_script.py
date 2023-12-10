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

from xuarizm import Constants

# DEBUG, INFO, WARNING, ERROR, CRITICAL are the values for logging values
log_level = logging.WARNING
PRECISION = 20
TIMEOUT = 15000  # In milliseconds

logging.getLogger().setLevel(log_level)

s = SifrSystem(xcimal_places=PRECISION*2)

# Zero
a = Sifr('0', s)
# Sub one positive rational number
b = Sifr('0.96123724', s)
# Large positive rational number
c = Sifr('219.8459', s)
# Negative rational number
d = Sifr('-31.26001234', s)
# Odd positive integer
e = Sifr('3', s)
# Even positive integer
f = Sifr('4', s)
# Negative integer
g = Sifr('-5', s)
# Double digit positive integer
h = Sifr('13', s)

# Set precision for decimals
getcontext().prec = PRECISION * 3

ad = Decimal('0.0')
bd = Decimal('0.96123724')
cd = Decimal('219.8459')
dd = Decimal('-31.26001234')
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

# #############################################################################
# Xuarizm tests against known constants

xuarizm_test = True

arabic_det = SifrSystem(xcimal_places=100)
c = Constants(arabic_det)

print("XUARIZM TESTS: Testing against known constants")

pi_text1000 = '3.1415926535897932384626433832795028841971693993751058209749' +\
    '4459230781640628620899862803482534211706798214808651328230664709384460' +\
    '9550582231725359408128481117450284102701938521105559644622948954930381' +\
    '9644288109756659334461284756482337867831652712019091456485669234603486' +\
    '1045432664821339360726024914127372458700660631558817488152092096282925' +\
    '4091715364367892590360011330530548820466521384146951941511609433057270' +\
    '3657595919530921861173819326117931051185480744623799627495673518857527' +\
    '2489122793818301194912983367336244065664308602139494639522473719070217' +\
    '9860943702770539217176293176752384674818467669405132000568127145263560' +\
    '8277857713427577896091736371787214684409012249534301465495853710507922' +\
    '7968925892354201995611212902196086403441815981362977477130996051870721' +\
    '1349999998372978049951059731732816096318595024459455346908302642522308' +\
    '2533446850352619311881710100031378387528865875332083814206171776691473' +\
    '0359825349042875546873115956286388235378759375195778185778053217122680' +\
    '66130019278766111959092164201989'

phi_text1000 = '1.618033988749894848204586834365638117720309179805762862135' +\
    '4486227052604628189024497072072041893911374847540880753868917521266338' +\
    '6222353693179318006076672635443338908659593958290563832266131992829026' +\
    '7880675208766892501711696207032221043216269548626296313614438149758701' +\
    '2203408058879544547492461856953648644492410443207713449470495658467885' +\
    '0987433944221254487706647809158846074998871240076521705751797883416625' +\
    '6249407589069704000281210427621771117778053153171410117046665991466979' +\
    '8731761356006708748071013179523689427521948435305678300228785699782977' +\
    '8347845878228911097625003026961561700250464338243776486102838312683303' +\
    '7242926752631165339247316711121158818638513316203840052221657912866752' +\
    '9465490681131715993432359734949850904094762132229810172610705961164562' +\
    '9909816290555208524790352406020172799747175342777592778625619432082750' +\
    '5131218156285512224809394712341451702237358057727861600868838295230459' +\
    '2647878017889921990270776903895321968198615143780314997411069260886742' +\
    '962267575605231727775203536139362'

e_text1000 = '2.71828182845904523536028747135266249775724709369995957496696' +\
    '7627724076630353547594571382178525166427427466391932003059921817413596' +\
    '6290435729003342952605956307381323286279434907632338298807531952510190' +\
    '1157383418793070215408914993488416750924476146066808226480016847741185' +\
    '3742345442437107539077744992069551702761838606261331384583000752044933' +\
    '8265602976067371132007093287091274437470472306969772093101416928368190' +\
    '2551510865746377211125238978442505695369677078544996996794686445490598' +\
    '7931636889230098793127736178215424999229576351482208269895193668033182' +\
    '5288693984964651058209392398294887933203625094431173012381970684161403' +\
    '9701983767932068328237646480429531180232878250981945581530175671736133' +\
    '2069811250996181881593041690351598888519345807273866738589422879228499' +\
    '8920868058257492796104841984443634632449684875602336248270419786232090' +\
    '0216099023530436994184914631409343173814364054625315209618369088870701' +\
    '6768396424378140592714563549061303107208510383750510115747704171898610' +\
    '6873969655212671546889570350354'

if xuarizm_test:
    pi = c.return_bbp_pi(Sifr('80', arabic_det))
    phi = c.return_phi(Sifr('40', arabic_det))
    e = c.return_e(Sifr('40', arabic_det))

    pi_calc = str(pi)[:92]
    pi_ans = pi_text1000[:92]

    phi_calc = str(phi)[:28]
    phi_ans = phi_text1000[:28]

    e_calc = str(e)[:50]
    e_ans = e_text1000[:50]

    print("# ########")
    print("# Pi TEST")
    print(" Calculated pi:")
    print("    " + pi_calc)
    if pi_calc == pi_ans:
        print("        PASS")
    else:
        print("        FAIL")
        print(" Correct value:")
        print("    " + pi_ans)
    print("")

    print("# ########")
    print("# Phi TEST")
    print(" Calculated phi:")
    print("    " + phi_calc)
    if phi_calc == phi_ans:
        print("        PASS")
    else:
        print("        FAIL")
        print(" Correct value:")
        print("    " + phi_ans)
    print("")

    print("# ########")
    print("# Natural Number TEST")
    print(" Calculated e:")
    print("    " + e_calc)
    if e_calc == e_ans:
        print("        PASS")
    else:
        print("        FAIL")
        print(" Correct value:")
        print("    " + e_ans)
    print("")

else:
    print("Xuarizm test not run")
