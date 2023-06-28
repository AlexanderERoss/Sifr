# #############################################################################
# This file contains system. The primary one being the SifrSystem class which
# defines an Arabic-like numbering system that is universally definable by
# allocating neg, xcimal separators etc. and assigning the sequence of
# of characters to use as digits, the length of which is used as the base
# number for the system
# #############################################################################

import logging
import pdb

# Make breakpoint shorter
bp = pdb.set_trace

# DEBUG, INFO, WARNING, ERROR, CRITICAL are the values for logging values
log_level = logging.ERROR
logging.basicConfig(level=log_level)

# DECORATORS


def mask_logging(func):
    def wrapper(*args):
        prev_log_level = logging.root.level
        logging.getLogger().setLevel(logging.ERROR)
        result = func(*args)
        logging.getLogger().setLevel(prev_log_level)
        return result
    return wrapper


# SYSTEMS


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
        self.iden = digit_list[0]
        self.unit = self.digit_list[1]

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
        d_parts = d.split(self.sep_point)
        d_num = d_parts[0]
        d_xcimal = self.iden if len(d_parts) == 1 else d_parts[1]

        return d_num, d_xcimal

    def _base_add_alg(self, d1, d2):
        '''Adds two sequences to the length of the maximum digit.
        Returns: [Added sequence, next digit should be carried]'''

        logging.debug("  ### START BASE ADD")
        result = ''

        d1, d2 = self._pad_iden(d1, d2, end=False)
        logging.debug("   Adding " + d2 + " to " + d1)

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
                logging.debug("   Add " + d1_digit + " and " + d2[-1])
                # Adds the digit to be added
                for dig_seq in self.digit_list:
                    if dig_seq == d2[-1]:
                        d2 = d2[:-1]
                        break
                    d1_digit, dig_carry = self.incr(d1_digit)
                    carry = True if dig_carry else carry

            logging.debug("   Result: " + d1_digit)
            result = d1_digit + result
            logging.debug("   New digit for step: " + str(result))

        logging.info("   Final Base Add Result: " + str(result))
        logging.debug("  ### END BASE ADD")
        return result, carry

    def _from_iden_sub(self, d):
        ''' Subtracts the digit from a set of zeroes, used for
        when zero is crossed and looking to change the numbers '''
        logging.debug("   # Number to zero sub: " + d)
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
        logging.debug("   # Zero subbed number: " + result)
        return result

    def _pad_iden(self, d1, d2, end=True):
        ''' Adds addition identity characters to digits (at end-True or
        start-False) to the arithmetic algorithm lines up to right digit '''
        max_len = max(len(d1), len(d2))
        d1_padded = d1
        d2_padded = d2
        for ind in range(1, max_len + 1):
            if end:
                if ind > len(d1):
                    d1_padded += self.iden
                if ind > len(d2):
                    d2_padded += self.iden
            elif not end:
                if ind > len(d1):
                    d1_padded = self.iden + d1_padded
                if ind > len(d2):
                    d2_padded = self.iden + d2_padded
        return d1_padded, d2_padded

    def _base_subt_alg(self, d1, d2):
        '''Subtracts the second sequence of digits from the first for
        only the length of the maximum digit.

        Returns: [Subtracted sequence, next digit should be carried]'''

        logging.debug("  ### START BASE SUBTRACT")
        result = ''
        d1, d2 = self._pad_iden(d1, d2, end=False)
        logging.debug("   Subtracting " + d2 + " from " + d1)

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
                logging.debug("   Subtract " + d2[-1] + " from " + d1_digit)
                # Adds the digit to be added
                for dig_seq in self.digit_list:
                    if dig_seq == d2[-1]:
                        d2 = d2[:-1]
                        break
                    d1_digit, dig_carry = self._incr_inv(d1_digit)
                    carry = True if dig_carry else carry

            logging.debug("   Result: " + d1_digit)
            result = d1_digit + result
            logging.debug("   New digit for step: " + result)

        logging.info("   Final Base Subtract Result: " + result)
        logging.debug("  ### END BASE SUBTRACT")
        return result, carry

    def _dec_combine(self, d1, d2, arith_function):
        logging.debug(" ### START DEC COMBINE")

        logging.debug(' d1: ' + str(d1) + ' Type: ' + str(type(d1)))
        logging.debug(' d2: ' + str(d2) + ' Type: ' + str(type(d2)))

        # Assigns identity
        unit, _ = self.incr(self.iden)
        iden_next, _ = arith_function(self.iden, unit)

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
            diff_num, _ = arith_function(self.iden*len(num), num)
            diff_num, _ = arith_function(diff_num, unit)
            diff_xcimal, _ = arith_function(self.iden*len(xcimal), xcimal)
            result = diff_num + self.sep_point + diff_xcimal
            zero_cross = True
        else:
            result = num + self.sep_point + xcimal

        logging.debug(" ### END DEC COMBINE")
        return result.strip(self.iden), zero_cross

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
        '''algo is add for multiply, and algo is multiply for exponentiation'''

        result = iden

        # Loop through each xcimal to apply 'algo' that number of times
        fig_count = 0
        for d2_dig in d2[::-1]:
            for dig in self.digit_list:
                if dig == d2_dig:
                    break
                result = algo(result, self._raise_by_base(d1, fig_count))
            fig_count += 1
        return result

    def _base_mul(self, d1, d2):
        '''Multiplies two numbers together by repeatedly adding
        ignoring negative signs (only provide magnitude)'''

        logging.debug(" ### START BASE MULT")

        logging.debug(' d1: ' + str(d1) + ' Type: ' + str(type(d1)))
        logging.debug(' d2: ' + str(d2) + ' Type: ' + str(type(d2)))

        d1_num, d1_xcimal = self._dec_split(d1)

        logging.debug("  d1_num :" + d1_num)
        logging.debug("  d1_xcimal: " + d1_xcimal)

        @mask_logging
        def full_add(x, y):
            return self._dec_combine(x, y, self._base_add_alg)[0]

        logging.debug("  Multiplying " + d2 + " by " + d1_num)
        ans_num = self.knuth_up(d2, d1_num, full_add, self.iden)
        logging.debug("  Answer main number: " + ans_num)

        logging.debug("  Multiplying " + d2 + " by " + d1_num)
        ans_xcimal = self.knuth_up(d2,
                                   d1_xcimal,
                                   full_add,
                                   self.iden)
        logging.debug("  Answer xcimal: " + ans_xcimal)

        # Update ans xcimal with right xcimal point
        ans_xc_num, ans_xc_xcimal = self._dec_split(ans_xcimal)

        xc_reduce = len(d1_xcimal)
        if xc_reduce >= len(ans_xc_num):
            ans_xc_fin = (self.iden + self.sep_point
                          + self.iden*(xc_reduce - len(ans_xc_num))
                          + ans_xc_xcimal)
        else:
            ans_xc_fin = (ans_xc_num[:-xc_reduce] + self.sep_point
                          + ans_xc_num[-xc_reduce:] + ans_xc_xcimal)

        multpd, _ = self._dec_combine(ans_num,
                                      ans_xc_fin,
                                      self._base_add_alg)
        logging.debug(" ### END BASE MULT")
        return multpd

    def _times_in_num(self, numer, denom):
        logging.debug("    ##### ḂEGIN TIMES IN NUM COUNT")
        logging.debug("     ##### Dividing " + numer + " by " + denom)
        unit = self.digit_list[1]
        prod = self.iden
        quot = self.iden

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
        logging.debug("    ##### END TIMES IN NUM COUNT")
        return quot.split(self.sep_point)[0], modulus

    def _base_div(self, numer, denom):
        logging.debug(" ### START BASE DIV")
        logging.debug("  # Dividing " + numer + " by " + denom)

        # @mask_logging
        def lil_div(num, den):
            return self._times_in_num(num, den)

        mod_zero = False
        xcim_count = 1
        first_div, modls = lil_div(numer, denom)
        divd = first_div + self.sep_point
        logging.debug("  Main number: " + self._norm_ans(divd))
        logging.debug("  Modulus to be divided in xcimal: " + modls)

        while not mod_zero and xcim_count <= self.xcimal_places:
            logging.debug("   # New decimal")
            m_quot, modls = lil_div(self._raise_by_base(modls, 1), denom)
            mod_zero = self._orderer(modls, self.iden)[1]
            xcim_count += 1
            divd += m_quot
            logging.debug("   Extra xcimal: " + m_quot
                          + " Xcimal count: " + str(xcim_count - 1))
            logging.debug("   Modulus: " + self._norm_ans(modls))
        logging.debug(" ### END BASE DIV")
        return self._norm_ans(divd)

    def _int_exp(self, base, exp):
        exp_num, exp_xcim = self._dec_split(exp)
        if self._orderer(exp_xcim, self.iden)[0]:
            raise Exception("Exponentiation only implemented for integers " +
                            "at this point")
        base_num, base_xcim = self._dec_split(base)

        @mask_logging
        def full_mult(x, y):
            return self._base_mul(x, y)

        return self.knuth_up(base, exp, full_mult, self.unit)

    def _num_compare(self, d1, d2):
        ''' Compare digits magnitude, without xcimal separator
        Always starts with first digit, to be used for numbers with same
        lengths or not necessarily equal xcimals. '''

        logging.debug("  ### START NUM COMPARE")
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
        logging.debug("  ### END NUM COMPARE")
        return greater, equal

    def _orderer(self, d1, d2):
        logging.debug(" ### START ORDERER")
        d1 = self._norm_ans(d1)
        d2 = self._norm_ans(d2)
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
        logging.debug(" ### END ORDERER")
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
        # Intentionally chosen to always have a zero to indicate that this
        # type is always capable of behaving as a float.
        if norm_ans[-1] == self.sep_point:
            norm_ans = norm_ans + self.digit_list[0]
        logging.debug("  ### NORMALIZED ANSWER")
        return norm_ans
