# #############################################################################
# Created by Alexander Ross
# 2nd July 2022
# #############################################################################
# Sifr is the main script which calculates the main arithmetic of the
# generalised number system.
# It's purpose is not efficiency, but rather to break down mathematical
# processes to its component functions and generalizability
# #############################################################################

import logging
import pdb

# Make breakpoint shorter
bp = pdb.set_trace

# DEBUG, INFO, WARNING, ERROR, CRITICAL are the values for logging values
log_level = logging.DEBUG
logging.basicConfig(level=log_level)


def mask_logging(func):
    def wrapper(*args):
        prev_log_level = logging.root.level
        logging.getLogger().setLevel(logging.ERROR)
        result = func(*args)
        logging.getLogger().setLevel(prev_log_level)
        return result
    return wrapper


class SifrSystem(object):
    def __init__(self, digit_list='0123456789', sep_point='.', neg_sym='-',
                 xcimal_places=40):
        unique_digits = len(set(digit_list)) != len(digit_list)
        sep_not_in_digits = sep_point not in digit_list
        neg_not_in_digits = neg_sym not in digit_list
        if unique_digits and sep_not_in_digits and neg_not_in_digits:
            raise Exception("The list off characters is not unique " +
                            "and thus can't be used as a numbering system")
        self.digit_list = digit_list
        self.sep_point = sep_point
        self.neg_sym = neg_sym
        self.xcimal_places = xcimal_places

        self.base_no = len(self.digit_list)
        logging.debug("SifrSystem instantiated with characters: " +
                      str(digit_list) +
                      ", sub-integer separator: " +
                      str(sep_point) +
                      ", and negative symbol: " +
                      neg_sym)

    def incr(self, prev_no):
        if prev_no not in self.digit_list:
            raise Exception("Digit not in list and thus different " +
                            "numbering system")
        disp_next = False
        for digit in self.digit_list:
            if disp_next:
                carry = False
                return digit, carry
            if digit == prev_no:
                disp_next = True
        carry = True
        return self.digit_list[0], carry

    def _incr_inv(self, prev_no):
        if prev_no not in self.digit_list:
            raise Exception("Digit not in list and thus different " +
                            "numbering system")
        disp_next = False
        for digit in self.digit_list[::-1]:
            if disp_next:
                carry = False
                return digit, carry
            if digit == prev_no:
                disp_next = True
        carry = True
        return self.digit_list[-1], carry

    def _dec_split(self, d):
        ''' Splits a decimal (non-negative) into it's consituent parts'''
        iden = self.digit_list[0]
        d_parts = d.split(self.sep_point)
        d_num = d_parts[0]
        d_xcimal = iden if len(d_parts) == 1 else d_parts[1]

        return d_num, d_xcimal

    def _base_add_alg(self, d1, d2):
        '''Adds two sequences to the length of the maximum digit.
        Returns: [Added sequence, next digit should be carried]'''

        logging.debug("### START BASE ADD")
        result = ''

        d1, d2 = self._pad_iden(d1, d2, end=False)
        logging.debug("  Adding " + d2 + " to " + d1)

        base_digit_range = range(1, len(d1)+1)
        carry = False

        for digit in base_digit_range:
            if len(d1) == 0:
                break

            d1_digit = d1[-1]
            d1 = d1[:-1]

            # If addition exceeds base in previous another is added
            if carry:
                d1_digit, dig_carry = self.incr(d1_digit)
                carry = True if dig_carry else False

            if len(d2) != 0:
                logging.debug("  Add " + d1_digit + " and " + d2[-1])
                # Adds the digit to be added
                for dig_seq in self.digit_list:
                    if dig_seq == d2[-1]:
                        d2 = d2[:-1]
                        break
                    d1_digit, dig_carry = self.incr(d1_digit)
                    carry = True if dig_carry else carry

            logging.debug("  Result: " + d1_digit)
            result = d1_digit + result
            logging.debug("  New digit for step: " + str(result))

        logging.info("  Final Base Add Result: " + str(result))
        logging.debug("### END BASE ADD")
        return result, carry

    def _from_iden_sub(self, d):
        ''' Subtracts the digit from a set of zeroes, used for
        when zero is crossed and looking to change the numbers '''
        logging.debug("# Number to zero sub: " + d)
        result = ''
        rev_dig_list = self.digit_list[0] + self.digit_list[1:][::-1]
        for dig in d:
            ind = 0
            counts = self.digit_list
            for count in counts:
                if dig == count:
                    break
                ind += 1
            result += rev_dig_list[ind]
        logging.debug("# Zero subbed number: " + result)
        return result

    def _pad_iden(self, d1, d2, end=True):
        ''' Adds addition identity characters to digits (at end-True or
        start-False) to the arithmetic algorithm lines up to right digit '''
        iden = self.digit_list[0]
        max_len = max(len(d1), len(d2))
        d1_padded = d1
        d2_padded = d2
        for ind in range(1, max_len + 1):
            if end:
                if ind > len(d1):
                    d1_padded += iden
                if ind > len(d2):
                    d2_padded += iden
            elif not end:
                if ind > len(d1):
                    d1_padded = iden + d1_padded
                if ind > len(d2):
                    d2_padded = iden + d2_padded
        return d1_padded, d2_padded

    def _base_subt_alg(self, d1, d2):
        '''Subtracts the second sequence of digits from the first for
        only the length of the maximum digit.

        Returns: [Subtracted sequence, next digit should be carried]'''

        logging.debug("### START BASE SUBTRACT")
        result = ''
        d1, d2 = self._pad_iden(d1, d2, end=False)
        logging.debug("  Subtracting " + d2 + " from " + d1)

        base_digit_range = range(1, len(d1)+1)
        carry = False

        for digit in base_digit_range:
            if len(d1) == 0:
                break

            d1_digit = d1[-1]
            d1 = d1[:-1]

            # If subtraction goes below base unit is subtracted
            if carry:
                d1_digit, dig_carry = self._incr_inv(d1_digit)
                carry = True if dig_carry else False

            # Subtract d2 digit if there are digits left
            if len(d2) != 0:
                logging.debug("Subtract " + d2[-1] + " from " + d1_digit)
                # Adds the digit to be added
                for dig_seq in self.digit_list:
                    if dig_seq == d2[-1]:
                        d2 = d2[:-1]
                        break
                    d1_digit, dig_carry = self._incr_inv(d1_digit)
                    carry = True if dig_carry else carry

            logging.debug("  Result: " + d1_digit)
            result = d1_digit + result
            logging.debug("  New digit for step: " + result)

        logging.info("  Final Base Subtract Result: " + result)
        logging.debug("### END BASE SUBTRACT")
        return result, carry

    def _dec_combine(self, d1, d2, arith_function):
        logging.debug("### START DEC COMBINE")

        logging.debug(' d1: ' + str(d1) + ' Type: ' + str(type(d1)))
        logging.debug(' d2: ' + str(d2) + ' Type: ' + str(type(d2)))

        # Assigns identity
        iden = self.digit_list[0]
        unit, _ = self.incr(iden)
        iden_next, _ = arith_function(iden, unit)

        # Assigns the main number and xcimal from ordered numbers

        num1, xcimal1 = self._dec_split(d1)
        num2, xcimal2 = self._dec_split(d2)

        # Pads arithmetic identity to end to make equal length
        xcimal1, xcimal2 = self._pad_iden(xcimal1, xcimal2)

        # Use the described arithmetic function to calculate
        xcimal, xc_carry = arith_function(xcimal1, xcimal2)

        zero_cross = False

        if xc_carry:
            num, temp_carry = arith_function(num1, unit)
            num = num if not temp_carry else iden_next + num
            num, carry = arith_function(num, num2)
        else:
            num, carry = arith_function(num1, num2)

        if carry and iden_next == unit:
            result = unit + num + self.sep_point + xcimal
        elif carry:
            diff_num, _ = arith_function(iden*len(num), num)
            diff_num, _ = arith_function(diff_num, unit)
            diff_xcimal, _ = arith_function(iden*len(xcimal), xcimal)
            result = diff_num + self.sep_point + diff_xcimal
            zero_cross = True
        else:
            result = num + self.sep_point + xcimal

        logging.debug("### END DEC COMBINE")
        return result.strip(iden), zero_cross

    def _raise_by_base(self, d, exp):
        ''' Makes each digit in a number 'exp' bases higher for the digit (d).
        Doesn't accept negative numbers '''
        sep = self.sep_point
        if exp == 0:
            result = d
        elif exp == 1:
            if sep in d and d[-1] != sep:
                d_num, d_xcimal = self._dec_split(d)
                result = d_num + d_xcimal[0] + sep + d_xcimal[1:]
            else:
                result = d.replace(sep, '') + self.digit_list[0]
        else:
            result = self._raise_by_base(self._raise_by_base(d, 1), exp - 1)
        return result

    def knuth_up(self, d1, d2, algo, iden):
        ''' algo is add for multiply '''

        result = iden

        # Loop through each xcimal to apply 'algo' that number of times
        fig_count = 0
        for d2_dig in d2[::-1]:
            for dig in self.digit_list:
                if dig == d2_dig:
                    break
                result, _ = algo(result, self._raise_by_base(d1, fig_count))
            fig_count += 1

        return result

    def _base_mul(self, d1, d2):
        '''Multiplies two numbers together by repeatedly adding
        ignoring negative signs (only provide magnitude)'''

        logging.debug("### START BASE MULT")
        iden = self.digit_list[0]

        logging.debug(' d1: ' + str(d1) + ' Type: ' + str(type(d1)))
        logging.debug(' d2: ' + str(d2) + ' Type: ' + str(type(d2)))

        d1_num, d1_xcimal = self._dec_split(d1)

        logging.debug("d1_num :" + d1_num)
        logging.debug("d1_xcimal: " + d1_xcimal)

        @mask_logging
        def full_add(x, y):
            return self._dec_combine(x, y, self._base_add_alg)

        logging.debug("Multiplying " + d2 + " by " + d1_num)
        ans_num = self.knuth_up(d2, d1_num, full_add, iden)
        logging.debug("Answer main number: " + ans_num)

        logging.debug("Multiplying " + d2 + " by " + d1_num)
        ans_xcimal = self.knuth_up(d2,
                                   d1_xcimal,
                                   full_add,
                                   iden)
        logging.debug("Answer xcimal: " + ans_xcimal)

        # Update ans xcimal with right xcimal point
        ans_xc_num, ans_xc_xcimal = self._dec_split(ans_xcimal)

        xc_reduce = len(d1_xcimal)
        if xc_reduce >= len(ans_xc_num):
            ans_xc_fin = (iden + self.sep_point
                          + iden*(xc_reduce - len(ans_xc_num))
                          + ans_xc_xcimal)
        else:
            ans_xc_fin = (ans_xc_num[:-xc_reduce] + self.sep_point
                          + ans_xc_num[-xc_reduce:] + ans_xc_xcimal)

        multpd, _ = self._dec_combine(ans_num,
                                      ans_xc_fin,
                                      self._base_add_alg)
        logging.debug("### END BASE MULT")
        return multpd

    def _times_in_num(self, numer, denom):
        logging.debug("    ##### Begin times in num count")
        logging.debug("     ##### Dividing " + numer + " by " + denom)
        iden = self.digit_list[0]
        unit = self.digit_list[1]
        prod = iden
        quot = iden

        @mask_logging
        def full_add(x, y):
            result = self._dec_combine(x, y, self._base_add_alg)
            return result[0]

        @mask_logging
        def full_subt(x, y):
            result = self._dec_combine(x, y, self._base_subt_alg)
            return result[0]

        while True:
            logging.debug("      ##### Running quot: " + quot)
            logging.debug("      ##### Running tally: " + prod)
            new_prod = full_add(prod, denom)
            new_quot = full_add(quot, unit)
            if any(self._orderer(new_prod, numer)):
                break
            prod = new_prod
            quot = new_quot
        logging.debug("     ##### Final quotient: " + quot)
        logging.debug("     ##### Final product: " + prod)
        modulus = full_subt(numer, prod)
        logging.debug("     ##### Remainder: " + prod)
        logging.debug("    ##### End times in num count")
        return quot.split(self.sep_point)[0], modulus

    def _base_div(self, numer, denom):
        iden = self.digit_list[0]
        logging.debug("### START BASE DIV")

        @mask_logging
        def lil_div(num, den):
            return self._times_in_num(num, den)

        mod_zero = False
        xcim_count = 1
        first_div, modls = lil_div(numer, denom)
        divd = first_div + self.sep_point
        logging.debug("  Main number: " + divd)

        while not mod_zero and xcim_count <= self.xcimal_places:
            m_quot, modls = lil_div(self._raise_by_base(modls, 1), denom)
            mod_zero = self._orderer(modls, iden)[1]
            xcim_count += 1
            divd += m_quot
            logging.debug("   Modulus: " + modls)
            logging.debug("   Extra xcimal: " + m_quot
                          + " Xcimal count: " + str(xcim_count))
        logging.debug("### END BASE DIV")
        return self._norm_ans(divd)

    def _num_compare(self, d1, d2):
        ''' Compare digits magnitude, without xcimal separator
        Always starts with first digit, to be used for numbers with same
        lengths or not necessarily equal xcimals. '''

        if len(d1) > len(d2):
            longer_no = 'd1'
        elif len(d1) == len(d2):
            longer_no = 'equal'
        else:
            longer_no = 'd2'

        for dig_ind in range(min(len(d1), len(d2))):
            equal = False
            for dig in self.digit_list[::-1]:
                if d1[dig_ind] == dig and d2[dig_ind] == dig:
                    equal = True
                    to_break = False
                    break
                elif d1[dig_ind] == dig:
                    greater = True
                    equal = False
                    to_break = True
                    break
                elif d2[dig_ind] == dig:
                    greater = False
                    equal = False
                    to_break = True
                    break
                else:
                    to_break = False

            if to_break:
                break

        # Return result of equal or d1 greater than d2
        if equal:
            if longer_no == 'd1':
                equal = False
                greater = True
            elif longer_no == 'd2':
                equal = False
                greater = False
            elif longer_no == 'equal':
                equal = True
                greater = False

        return greater, equal

    def _orderer(self, d1, d2):
        d1_num, d1_xcimal = self._dec_split(d1)
        d2_num, d2_xcimal = self._dec_split(d2)

        if len(d1_num) > len(d2_num):
            greater = True
            equal = False
        elif len(d1_num) < len(d2_num):
            greater = False
            equal = False
        else:
            greater, equal = self._num_compare(d1_num, d2_num)
            if equal:
                greater, equal = self._num_compare(d1_xcimal, d2_xcimal)

        return greater, equal

    def _norm_ans(self, raw_ans: str):
        just_neg_and_point = raw_ans == (self.neg_sym + self.sep_point)
        just_point = raw_ans == self.sep_point
        if just_neg_and_point or just_point:
            norm_ans = self.digit_list[0] + self.sep_point + self.digit_list[0]
        else:
            norm_ans = raw_ans
        norm_ans = norm_ans.replace(self.neg_sym + self.digit_list[0],
                                    self.digit_list[0])
        if norm_ans[-1] == self.sep_point:
            norm_ans = norm_ans + self.digit_list[0]

        return norm_ans

# As a general rule the signing of the Sifr is dealt with within the dunder
# method, all other items (xcimal points, recursion for operation etc.) are
# calculated in the SifrSystem object.

class Sifr(object):
    '''A number type that takes a string representing the character
    and the number system represented as the class SifrSystem'''
    def __init__(self, sifr: str, sifr_system: SifrSystem):
        self.sifr = sifr
        self.ssys = sifr_system
        self.no_digits = len(sifr)
        self.is_neg = sifr[0] == sifr_system.neg_sym

    # REPRESENTATIONAL DUNDERS
    def __repr__(self):
        return self.sifr

    # UNARY MAGNITUDE OPERATOR DUNDERS
    def __abs__(self):
        if self.ssys.neg_sym != self.sifr[0]:
            result = Sifr(self.sifr, self.ssys)
        else:
            result = Sifr(self.sifr[1:], self.ssys)
        return result

    def __neg__(self):
        if self.is_neg:
            result = Sifr(self.sifr[1:], self.ssys)
        else:
            norm = self.ssys._norm_ans
            result = Sifr(norm(self.ssys.neg_sym + self.sifr),
                          self.ssys)
        return result

    def __pos__(self):
        norm = self.ssys._norm_ans
        return Sifr(norm(self.sifr), self.ssys)

    # ARITHMETIC DUNDERS
    def __add__(self, add_no):
        logging.debug("### START MAIN ADD")
        if self.ssys != add_no.ssys:
            raise Exception("Sifr Systems do not match and thus ",
                            "can't be added together")

        # Assign short names for arithmetic functions
        b_add = self.ssys._base_add_alg
        neg_sym = self.ssys.neg_sym
        dec_comb = self.ssys._dec_combine
        norm = self.ssys._norm_ans

        # Two positive numbers to add
        if not self.is_neg and not add_no.is_neg:
            logging.info("  Both numbers are not negative, proceeding to add")
            added, _ = dec_comb(self.sifr, add_no.sifr, b_add)
            result = Sifr(norm(added), self.ssys)

        # Two negative numbers to "add"
        elif self.is_neg and add_no.is_neg:
            logging.info("  Both numbers are negative, proceeding to add")
            added, _ = dec_comb(self.sifr[1:], add_no.sifr[1:], b_add)
            result = Sifr(norm(neg_sym + added), self.ssys)

        # Negative and positive to counteract
        else:
            b_neg = self.ssys._base_subt_alg
            self_mag = self.sifr if not self.is_neg else self.sifr[1:]
            add_no_mag = add_no.sifr if not add_no.is_neg else add_no.sifr[1:]
            added, zero_crossed = dec_comb(self_mag, add_no_mag, b_neg)
            if self.is_neg and zero_crossed:
                result = Sifr(norm(added), self.ssys)
            elif self.is_neg and not zero_crossed:
                result = Sifr(norm(neg_sym + added), self.ssys)
            elif not self.is_neg and zero_crossed:
                result = Sifr(neg_sym + added, self.ssys)
            elif not self.is_neg and not zero_crossed:
                result = Sifr(norm(added), self.ssys)

        logging.debug("### MAIN END ADD")
        return result

    def __sub__(self, sub_no):
        logging.debug("### MAIN START SUB")
        norm = self.ssys._norm_ans
        # If subtracted number is negative just add
        if sub_no.sifr[0] == self.ssys.neg_sym:
            logging.debug("### MAIN END SUB")
            result = self.__add__(Sifr(sub_no.sifr[1:], self.ssys))
        # Otherwise just add the negative
        else:
            logging.debug("### MAIN END SUB")
            result = self.__add__(Sifr(norm(self.ssys.neg_sym + sub_no.sifr),
                                       self.ssys))
        return result

    def __mul__(self, mul_no):
        logging.debug("### START MAIN MULT")
        raw_result = self.ssys._base_mul(self.__abs__().sifr,
                                         mul_no.__abs__().sifr)
        if (self.is_neg and mul_no.is_neg) or (not self.is_neg
                                               and not mul_no.is_neg):
            result = self.ssys._norm_ans(raw_result)
        else:
            result = self.ssys._norm_ans(self.ssys.neg_sym + raw_result)
        logging.debug("### END MAIN MULT")
        return Sifr(result, self.ssys)

    def __floordiv__(self, div_no):
        logging.debug("### START FLOOR DIV")
        raw_result = self.ssys._times_in_num(self.__abs__().sifr,
                                             div_no.__abs__().sifr)[0]
        if (self.is_neg and div_no.is_neg) or (not self.is_neg
                                               and not div_no.is_neg):
            result = self.ssys._norm_ans(raw_result)
        else:
            result = self.ssys._norm_ans(self.ssys.neg_sym + raw_result)
        logging.debug("### END FLOOR DIV")
        return Sifr(result, self.ssys)

    def __mod__(self, div_no):
        logging.debug("### START MAIN MOD")
        raw_result = self.ssys._times_in_num(self.__abs__().sifr,
                                             div_no.__abs__().sifr)[1]
        if (self.is_neg and div_no.is_neg) or (not self.is_neg
                                               and not div_no.is_neg):
            result = self.ssys._norm_ans(raw_result)
        else:
            result = self.ssys._norm_ans(self.ssys.neg_sym + raw_result)
        logging.debug("### END MAIN MOD")
        return Sifr(result, self.ssys)

    def __truediv__(self, div_no):
        logging.debug("### START MAIN DIV")
        raw_result = self.ssys._base_div(self.__abs__().sifr,
                                         div_no.__abs__().sifr)
        if (self.is_neg and div_no.is_neg) or (not self.is_neg
                                               and not div_no.is_neg):
            result = self.ssys._norm_ans(raw_result)
        else:
            result = self.ssys._norm_ans(self.ssys.neg_sym + raw_result)
        logging.debug("### END MAIN DIV")
        return Sifr(result, self.ssys)

    # RELATIONAL DUNDERS
    def __eq__(self, d):
        if not self.is_neg and not d.is_neg:
            _, equal = self.ssys._orderer(self.sifr, d.sifr)
        elif self.is_neg and d.is_neg:
            _, equal = self.ssys._orderer(self.sifr.__abs__(),
                                          d.sifr.__abs__())
        elif self.is_neg and not d.is_neg:
            equal = False
        elif not self.is_neg and d.is_neg:
            equal = False
        return equal

    def __gt__(self, d):
        if not self.is_neg and not d.is_neg:
            greater, _ = self.ssys._orderer(self.sifr, d.sifr)
        elif self.is_neg and d.is_neg:
            not_greater, _ = self.ssys._orderer(self.sifr.__abs__(),
                                                d.sifr.__abs__())
            greater = not not_greater
        elif self.is_neg and not d.is_neg:
            greater = False
        elif not self.is_neg and d.is_neg:
            greater = True
        return greater

    def __lt__(self, d):
        if not self.is_neg and not d.is_neg:
            greater, equal = self.ssys._orderer(self.sifr, d.sifr)
        elif self.is_neg and d.is_neg:
            not_greater, equal = self.ssys._orderer(self.sifr.__abs__(),
                                                    d.sifr.__abs__())
            greater = not not_greater
        elif self.is_neg and not d.is_neg:
            greater = False
            equal = False
        elif not self.is_neg and d.is_neg:
            greater = True
            equal = False
        return not greater and not equal

    def __ge__(self, d):
        if not self.is_neg and not d.is_neg:
            greater, equal = self.ssys._orderer(self.sifr, d.sifr)
        elif self.is_neg and d.is_neg:
            not_greater, equal = self.ssys._orderer(self.__abs__().sifr,
                                                    d.__abs__().sifr)
            greater = not not_greater
        elif self.is_neg and not d.is_neg:
            greater = False
            equal = False
        elif not self.is_neg and d.is_neg:
            greater = True
            equal = False
        return greater or equal

    def __le__(self, d):
        if not self.is_neg and not d.is_neg:
            greater, equal = self.ssys._orderer(self.sifr, d.sifr)
        elif self.is_neg and d.is_neg:
            not_greater, equal = self.ssys._orderer(self.sifr.__abs__(),
                                                    d.sifr.__abs__())
            greater = not not_greater
        elif self.is_neg and not d.is_neg:
            greater = False
            equal = False
        elif not self.is_neg and d.is_neg:
            greater = True
            equal = False
        return not greater or equal


s = SifrSystem()
a = Sifr('32.961', s)
b = Sifr('31.2614', s)
c = Sifr('-31.261', s)
d = Sifr('2192.845', s)

ad = 32.961
bd = 31.2614
cd = -31.261
dd = 2192.845
