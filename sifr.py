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

# DEBUG, INFO, WARNING, ERROR, CRITICAL are the values for logging values
logging.basicConfig(level=logging.INFO)


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
        # Orders the given Sifr strings
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

    def _normalize_result(self, raw_ans):
        just_neg_and_point = raw_ans == (self.neg_sym + self.sep_point)
        just_point = raw_ans == self.sep_point
        if just_neg_and_point or just_point:
            norm_ans = self.digit_list[0] + self.sep_point + self.digit_list[0]
        else:
            norm_ans = raw_ans
        return norm_ans.replace(self.neg_sym + self.digit_list[0],
                                self.digit_list[0])


class Sifr(object):
    '''A number type that takes a string representing the character
    and the number system represented as the class SifrSystem'''
    def __init__(self, sifr: str, sifr_system: SifrSystem):
        self.sifr = sifr
        self.sifr_system = sifr_system
        self.no_digits = len(sifr)
        self.is_neg = sifr[0] == sifr_system.neg_sym
        self.magnitude = sifr if sifr_system.neg_sym != sifr[0] else sifr[1:]

    def __repr__(self):
        return self.sifr

    def __add__(self, add_no):
        logging.debug("### START MAIN ADD")
        if self.sifr_system != add_no.sifr_system:
            raise Exception("Sifr Systems do not match and thus ",
                            "can't be added together")

        # Assign short names for arithmetic functions
        b_add = self.sifr_system._base_add_alg
        neg_sym = self.sifr_system.neg_sym
        dec_comb = self.sifr_system._dec_combine
        norm = self.sifr_system._normalize_result

        # Two positive numbers to add
        if not self.is_neg and not add_no.is_neg:
            logging.info("  Both numbers are not negative, proceeding to add")
            added, _ = dec_comb(self.sifr,
                                add_no.sifr,
                                b_add)
            result = Sifr(norm(added), self.sifr_system)

        # Two negative numbers to "add"
        elif self.is_neg and add_no.is_neg:
            logging.info("  Both numbers are negative, proceeding to add")
            added, _ = dec_comb(self.sifr[1:], add_no.sifr[1:], b_add)
            result = Sifr(norm(neg_sym + added),
                          self.sifr_system)

        # Negative and positive to counteract
        else:
            b_neg = self.sifr_system._base_subt_alg
            self_mag = self.sifr if not self.is_neg else self.sifr[1:]
            add_no_mag = add_no.sifr if not add_no.is_neg else add_no.sifr[1:]
            added, zero_crossed = dec_comb(self_mag, add_no_mag, b_neg)
            if self.is_neg and zero_crossed:
                result = Sifr(norm(added), self.sifr_system)
            elif self.is_neg and not zero_crossed:
                result = Sifr(norm(neg_sym + added), self.sifr_system)
            elif not self.is_neg and zero_crossed:
                result = Sifr(neg_sym + added, self.sifr_system)
            elif not self.is_neg and not zero_crossed:
                result = Sifr(norm(added), self.sifr_system)

        logging.debug("### MAIN END ADD")
        return result

    def __sub__(self, sub_no):
        logging.debug("### MAIN START SUB")
        norm = self.sifr_system._normalize_result
        # If subtracted number is negative just add
        if sub_no.sifr[0] == self.sifr_system.neg_sym:
            logging.debug("### MAIN END SUB")
            result = self.__add__(Sifr(sub_no.sifr[1:], self.sifr_system))
        # Otherwise just add the negative
        else:
            logging.debug("### MAIN END SUB")
            result = self.__add__(Sifr(norm(self.sifr_system.neg_sym
                                            + sub_no.sifr),
                                       self.sifr_system))
        result = self.sifr_system._normalize_result(result)
        return result


s = SifrSystem()
a = Sifr('32.961', s)
b = Sifr('31.2614', s)
c = Sifr('-31.261', s)
d = Sifr('92.845', s)
