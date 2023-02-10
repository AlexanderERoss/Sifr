# #############################################################################
# Created by Alexander Ross
# 2nd July 2022
# #############################################################################
# Sifr is the main script which calculates the main arithmetic of the
# generalised number system.
# It's purpose is not efficiency, but rather to break down mathematical
# processes to its component functions.
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
        logging.getLogger().setLevel(logging.ERROR)
        result = func(*args)
        logging.getLogger().setLevel(log_level)
        return result
    return wrapper


class SifrSystem(object):
    def __init__(self, digit_list='0123456789', sep_point='.', neg_sym='-'):
        unique_digits = len(set(digit_list)) != len(digit_list)
        sep_not_in_digits = sep_point not in digit_list
        neg_not_in_digits = neg_sym not in digit_list
        if unique_digits and sep_not_in_digits and neg_not_in_digits:
            raise Exception("The list off characters is not unique " +
                            "and thus can't be used as a numbering system")
        self.digit_list = digit_list
        self.sep_point = sep_point
        self.neg_sym = neg_sym
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

    def magn(self, d):
        return d if self.neg_sym == d[0] else d[1:]

    def _base_add_alg(self, d1, d2):
        '''Adds two sequences to the length of the maximum digit.
        Returns: [Added sequence, next digit should be carried]'''

        logging.debug("### START BASE ADD")
        result = ''

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

        # Adds the first digit of system at start if there's carry at end
        if carry:
            if len(d2) == 0:
                result = result
            elif len(d2) == 1:
                result = self.incr(d2)[0] + result
            else:
                result = d2[:-1] + self.incr(d2[-1])[0] + result
        else:
            result = d2 + result

        logging.info("  Final Base Add Result: " + str(result))
        logging.debug("### END BASE ADD")
        return result, carry

    def _base_subt_alg(self, d1, d2):
        '''Subtracts the second sequence of digits from the first for
        only the length of the maximum digit.

        Returns: [Subtracted sequence, next digit should be carried]'''

        logging.debug("### START BASE SUBTRACT")
        result = ''
        logging.debug("  Subtracting " + d2 + " from " + d1)

        base_digit_range = range(1, len(d1)+1)
        carry = False

        for digit in base_digit_range:
            if len(d1) == 0:
                break

            d1_digit = d1[-1]
            d1 = d1[:-1]

            # If subtraction goes below base in previous another is subtracted
            if carry:
                d1_digit, dig_carry = self._incr_inv(d1_digit)
                carry = True if dig_carry else False

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

        # Adds the first digit of system at start if there's carry at end
        if carry:
            if len(d2) == 0:
                result = result
            elif len(d2) == 1:
                result = self._incr_inv(d2)[0] + result
            else:
                result = d2[:-1] + self._incr_inv(d2[-1])[0] + result
        else:
            result = d2 + result

        logging.info("  Final Base Subtract Result: " + result)
        logging.debug("### END BASE SUBTRACT")
        return result, carry

    def _dec_combine(self, d1, d2, arith_function):
        logging.debug("### START DEC COMBINE")
        sep = self.sep_point

        logging.debug(' d1: ' + str(d1) + ' Type: ' + str(type(d1)))
        logging.debug(' d2: ' + str(d2) + ' Type: ' + str(type(d2)))

        # Separates these into main number and xcimal
        d1_digits = d1.split(sep)
        d2_digits = d2.split(sep)

        # Assigns identity
        iden = self.digit_list[0]
        unit, _ = self.incr(iden)
        iden_next, _ = arith_function(iden, unit)

        # Assigns the main number and xcimal from ordered numbers
        num2 = d2_digits[0]
        if len(d2_digits) > 1:
            xcimal2 = d2_digits[1]
        else:
            xcimal2 = iden

        num1 = d1_digits[0]
        if len(d1_digits) > 1:
            xcimal1 = d1_digits[1]
        else:
            xcimal1 = iden

        # Assigns largest xcimal length
        xcimal_len = max(len(xcimal1), len(xcimal2))

        # Adds 0s to xcimals to the arithmetic algorithm lines up to
        # right digit
        for xcimal_ind in range(1, xcimal_len + 1):
            if xcimal_ind > len(xcimal1):
                xcimal1 += iden
            if xcimal_ind > len(xcimal2):
                xcimal2 += iden

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
                d_split = d.split(sep)
                d_num = d_split[0]
                d_xcimal = d_split[1]
                result = d_num + d_xcimal[0] + sep + d_xcimal[1:]
            else:
                result = d.replace(sep, '') + self.digit_list[0]
        else:
            result = self._raise_by_base(self._raise_by_base(d, 1), exp - 1)
        return result

    @mask_logging
    def knuth_up(self, d1, d2, algo, iden):
        ''' algo is add for multiply '''

        result = iden

        # Loop through each xcimal to apply 'algo' that number of times
        fig_count = 0
        for d2_dig in d2[::-1]:
            print("dig to multiply: " + d2_dig)
            for dig in self.digit_list:
                if dig == d2_dig:
                    break
                print("       " + self._raise_by_base(d1, fig_count))
                result, _ = algo(result, self._raise_by_base(d1, fig_count))
                print("  Result updated: " + result)
            fig_count += 1

        return result

    def _base_mul(self, d1, d2):
        '''Multiplies two numbers together by repeatedly adding
        ignoring negative signs (only provide magnitude)'''

        logging.debug("### START BASE MULT")
        iden = self.digit_list[0]

        logging.debug(' d1: ' + str(d1) + ' Type: ' + str(type(d1)))
        logging.debug(' d2: ' + str(d2) + ' Type: ' + str(type(d2)))

        d1_parts = d1.split(self.sep_point)
        d1_num = d1_parts[0]
        d1_xcimal = iden if len(d1_parts) == 0 else d1_parts[1]

        logging.debug("d1_num :" + d1_num)
        logging.debug("d1_xcimal: " + d1_xcimal)

        def full_add(x, y):
            return self._dec_combine(x, y, self._base_add_alg)

        logging.debug("Multiplying " + d2 + " by " + d1_num)
        ans_num = self.knuth_up(d2,
                                d1_num,
                                full_add,
                                iden)
        logging.debug("Answer main number: " + ans_num)

        logging.debug("Multiplying " + d2 + " by " + d1_num)
        ans_xcimal = self.knuth_up(d2,
                                   d1_xcimal,
                                   full_add,
                                   iden)
        logging.debug("Answer xcimal: " + ans_xcimal)

        # Update ans xcimal with right xcimal point
        ans_xc_split = ans_xcimal.split(self.sep_point)
        ans_xc_num = ans_xc_split[0]
        ans_xc_xcimal = iden if len(ans_xc_split) == 1 else ans_xc_split[1]

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


class Sifr(object):
    '''A number type that takes a string representing the character
    and the number system represented as the class SifrSystem'''
    def __init__(self, sifr: str, sifr_system: SifrSystem):
        self.sifr = sifr
        self.ssys = sifr_system
        self.no_digits = len(sifr)
        self.is_neg = sifr[0] == sifr_system.neg_sym
        self.magn = sifr if sifr_system.neg_sym != sifr[0] else sifr[1:]

    def __repr__(self):
        return self.sifr

    def __neg__(self):
        if self.is_neg:
            return Sifr(self.sifr[1:], self.ssys)
        else:
            norm = self.ssys._norm_ans
            return Sifr(norm(self.ssys.neg_sym + self.sifr),
                        self.ssys)

    def __pos__(self):
        norm = self.ssys._norm_ans
        return Sifr(norm(self.sifr), self.ssys)

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
        raw_result = self.ssys._base_mul(self.magn, mul_no.magn)
        if (self.is_neg and mul_no.is_neg) or (not self.is_neg
                                               and not mul_no.is_neg):
            result = self.ssys._norm_ans(raw_result)
        else:
            result = self.ssys._norm_ans(self.ssys.neg_sym + raw_result)
        logging.debug("### END MAIN MULT")
        return result


s = SifrSystem()
a = Sifr('32.961', s)
b = Sifr('31.2614', s)
c = Sifr('-31.261', s)
d = Sifr('92.845', s)

ad = 32.961
bd = 31.2614
cd = -31.261
dd = 92.845
