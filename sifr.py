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
logging.basicConfig(level=logging.DEBUG)


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

    def _magn_sort(self, d1, d2, main_no=True):
        '''Sorts the Sifr numbers in order of their magnitude from smallest
        to largest. Does not accept negative numbers, only xcimals'''
        if main_no:
            logging.debug("### Magnitude sort started with " +
                          str(d1) +
                          " and " +
                          str(d2))
        else:
            logging.debug("### Sub-magnitude sort started with " +
                          str(d1) + " and " + str(d2))

        d1 = self.magn(d1)
        d2 = self.magn(d2)

        # Split the numbers on the xcimal point to get both components
        if self.sep_point in d1:
            logging.debug("First number has separator")
            d1_maj, d1_min = d1.split(self.sep_point)
        else:
            logging.debug("First number does not have separator")
            d1_maj = d1
            d1_min = self.digit_list[0]
        if self.sep_point in d2:
            logging.debug("Second number has separator")
            d2_maj, d2_min = d2.split(self.sep_point)
        else:
            logging.debug("Second number does not have separator")
            d2_maj = d2
            d2_min = self.digit_list[0]

        # If first number has more digits
        if len(d1_maj) > len(d2_maj):
            logging.info("   " + d2 + " smaller than " + d1)
            return d2, d1, False
        # If second number has more digits
        elif len(d1_maj) < len(d2_maj):
            logging.info(d1 + " smaller than " + d2)
            return d1, d2, False
        # If same number of digits cycle through all digits and compare
        # their sequence in the digit list
        else:
            logging.debug("  Main digit is same length so comparing values")
            for digit in self.digit_list[::-1]:
                # If there are no digits left of the major number
                if len(d1_maj) == 0:
                    if main_no:
                        # Compare the number after xcimal point
                        d_min_less, d_min_more, xcmeq = self._magn_sort(d1_min,
                                                                        d2_min,
                                                                        False)
                        # If d2 had the smaller xcimal
                        if d_min_less == d2_min:
                            logging.info(d2 + " smaller than " + d1)
                            return d2, d1, False
                        # If d1 is smaller xcimal or equal
                        else:
                            logging.info(d1 + " smaller than " + d2)
                            return d1, d2, xcmeq
                    else:
                        # Two numbers are completely equal
                        logging.info(d1 + " smaller than " + d2)
                        return d1, d2, True
                # Checks if either number's digit is equal to next highest
                # in digit list
                d1_eq = digit == d1[0]
                d2_eq = digit == d2[0]
                # If both are equal
                if d1_eq and d2_eq:
                    # Recursively check next number sequence
                    d_less, d_more, _ = self._magn_sort(d1_maj[1:],
                                                        d2_maj[1:],
                                                        False)
                    if d_less == d1_maj[1:]:
                        logging.info(d1 + " smaller than " + d2)
                        return d1, d2, False
                    else:
                        logging.info(str(d2) + " smaller than " + str(d1))
                        return d2, d1, False
                elif d1_eq:
                    logging.info(str(d2) + " smaller than " + str(d1))
                    return d2, d1, False
                elif d2_eq:
                    logging.info(d1 + " smaller than " + d2)
                    return d1, d2, False

    def _base_add_alg(self, d1, d2):
        logging.debug("### Base addition algorithm commenced")
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
                result = self.digit_list[1] + result
            elif len(d2) == 1:
                result = self.incr(d2)[0] + result
            else:
                result = d2[:-1] + self.incr(d2[-1])[0] + result

        logging.info("Final Base Add Result: " + str(result))
        logging.debug("### END BASE ADD")
        return result

    def _base_neg_alg(self, d1, d2):
        '''Base algorithm to negate two numbers however the largest
        number must go first for simplicity'''
        logging.debug("### START BASE NEG")
        small_no, large_no, _ = self._magn_sort(d1, d2)
        logging.debug("  Small no: " + small_no + " Large no: " + large_no)
        result = ''
        carry = False

        for digit in range(1, len(large_no)+1):
            logging.info("    Large number digit being added: "
                         + str(large_no[-digit]))
            # Use counter to track subtractions stack
            subtraction_counter = self.digit_list

            # Loops through counter for large number to add
            for l_dig in self.digit_list:
                if l_dig == large_no[-digit]:
                    break
                subtraction_counter = subtraction_counter + l_dig

            # If addition exceeds base in previous another is added
            if carry:
                subtraction_counter = subtraction_counter[1:]

            # Loops through each number in small number to subtract
            if digit <= len(small_no):
                logging.info("    Small number digit to subtract: "
                             + str(small_no[-digit]))
                for s_count in self.digit_list:
                    if s_count == small_no[-digit]:
                        break
                    subtraction_counter = subtraction_counter[:-1]

            # Adds a carry for the next loop if there is only one last digit
            # in counter (i.e. base number has been crossed)
            carry = True if len([d for d in subtraction_counter
                                 if d == self.digit_list[-1]]) == 1 else False
            logging.debug("    Carry: " + str(carry))

            result = subtraction_counter[-1] + result
            logging.debug("  Sequence result: " + result)

        # Adds the first digit of system at start if there's carry at end
        if carry:
            result = self.digit_list[1] + result

        logging.info("Final Result: " + result)
        logging.debug("### END BASE NEG")
        return result

    def _dec_combine(self, d1, d2, arith_function):
        logging.debug("### START DEC COMBINE")
        sep = self.sep_point
        # Orders the given Sifr strings
        logging.debug('d1: ' + str(d1) + ' Type: ' + str(type(d1)))
        logging.debug('d2: ' + str(d2) + ' Type: ' + str(type(d2)))
        sml_no, lg_no, _ = self._magn_sort(d1, d2, True)

        # Separates these into main number and xcimal
        dsml_digits = sml_no.split(sep)
        dlg_digits = lg_no.split(sep)

        # Assigns identity
        iden = self.digit_list[0]

        # Assigns the main number and xcimal from ordered numbers
        num_lg = dlg_digits[0]
        if len(dlg_digits) > 1:
            xcimal_lg = dlg_digits[1]
        else:
            xcimal_lg = iden

        num_sml = dsml_digits[0]
        if len(dsml_digits) > 1:
            xcimal_sml = dsml_digits[1]
        else:
            xcimal_sml = iden

        # Adds zeroes to main number of smaller at start to align
        for lg_ind in range(1, len(num_lg) + 1):
            if lg_ind > len(num_sml):
                num_sml = iden + num_sml

        # Assigns largest xcimal length
        xcimal_len = max(len(xcimal_sml), len(xcimal_lg))

        # Adds 0s to xcimals to the arithmetic algorithm lines up to
        # right digit
        for xcimal_ind in range(1, xcimal_len + 1):
            if xcimal_ind > len(xcimal_sml):
                xcimal_sml += iden
            if xcimal_ind > len(xcimal_lg):
                xcimal_lg += iden

        # Create raw number without xcimal point
        raw_lg = num_lg + xcimal_lg
        raw_sml = num_sml + xcimal_sml

        # Use the described arithmetic function to calculate
        raw_tot = arith_function(raw_lg, raw_sml)

        arith_answer = ''

        # Put the answer together with the decimal
        for _ in range(0, xcimal_len):
            arith_answer = raw_tot[-1] + arith_answer
            raw_tot = raw_tot[:-1]

        arith_answer = self.sep_point + arith_answer

        arith_answer = raw_tot + arith_answer

        # Strip arithmetic identity values from start and end
        while arith_answer[0] == iden:
            arith_answer = arith_answer[1:]

        while arith_answer[-1] == iden:
            arith_answer = arith_answer[:-1]

        logging.debug("### END DEC COMBINE")
        return arith_answer


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
        b_add = self.sifr_system._base_add_alg

        neg_sym = self.sifr_system.neg_sym

        if not self.is_neg and not add_no.is_neg:
            logging.info("  Both numbers are not negative, proceeding to add")
            return Sifr(self.sifr_system._dec_combine(self.sifr,
                                                      add_no.sifr,
                                                      b_add),
                        self.sifr_system)
        elif self.is_neg and add_no.is_neg:
            logging.info("  Both numbers are negative, proceeding to add")
            ans = Sifr(neg_sym + self.sifr_system._dec_combine(self.sifr[1:],
                                                               add_no.sifr[1:],
                                                               b_add),
                       self.sifr_system)
            return ans

        b_neg = self.sifr_system._base_neg_alg
        self_mag = self.sifr if not self.is_neg else self.sifr[1:]
        add_no_mag = add_no.sifr if not add_no.is_neg else add_no.sifr[1:]

        sml_mag, big_mag, _ = self.sifr_system._magn_sort(self_mag, add_no_mag)
        is_self_bigger = big_mag == self_mag

        if is_self_bigger:
            logging.debug("  First number is bigger")
            result = self.sifr_system._dec_combine(self_mag, add_no_mag, b_neg)
            result = result if not self.is_neg else neg_sym + result
        else:
            logging.debug("  Second number is bigger")
            result = self.sifr_system._dec_combine(add_no_mag, self_mag, b_neg)
            result = result if self.is_neg else neg_sym + result
        logging.debug("### MAIN END ADD")
        return result

    def __sub__(self, sub_no):
        logging.debug("### MAIN START SUB")
        # If subtracted number is negative just add
        if sub_no.sifr[0] == self.sifr_system.sep_point:
            logging.debug("### MAIN END SUB")
            return self.__add__(Sifr(sub_no.sifr[1:], self.sifr_system))
        # Otherwise just add the negative
        else:
            logging.debug("### MAIN END SUB")
            return self.__add__(Sifr(self.sifr_system.neg_sym + sub_no.sifr,
                                     self.sifr_system))


s = SifrSystem()
a = Sifr('32.461', s)
b = Sifr('31.2614', s)
c = Sifr('-31.261', s)
