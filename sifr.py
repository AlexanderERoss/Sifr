# #############################################################################
# Created by Alexander Ross
# 2nd July 2022
# #############################################################################
# Sifr is the main script which calculates the main arithmetic of the
# generalised number system.
# #############################################################################

class SifrSystem(object):
    def __init__(self, digit_list='0123456789', sep_point='.', neg_sym='-'):
        unique_digits = len(set(digit_list)) != len(digit_list)
        sep_not_in_digits = sep_point not in digit_list
        neg_not_in_digits = neg_sym not in digit_list
        if unique_digits and sep_not_in_digits and neg_not_in_digits:
            Exception("The list off characters is not unique " +
                      "and thus can't be used as a numbering system")
        self.digit_list = digit_list
        self.sep_point = sep_point
        self.neg_sym = neg_sym
        self.base_no = len(self.digit_list)

    def _magn_sort(self, d1, d2, main_no=True):
        '''Sorts the Sifr numbers in order of their magnitude from smallest
        to largest. Does not accept negative numbers, only xcimals'''

        print("sort started")
        # Split the numbers on the xcimal point to get both components
        if self.sep_point in d1:
            d1_maj, d1_min = d1.split(self.sep_point)
        else:
            d1_maj = d1
            d1_min = self.digit_list[0]
        if self.sep_point in d2:
            d2_maj, d2_min = d2.split(self.sep_point)
        else:
            d2_maj = d2
            d2_min = self.digit_list[0]

        # If first number has more digits
        if len(d1_maj) > len(d2_maj):
            return d2, d1, False
        # If second number has more digits
        elif len(d1_maj) < len(d2_maj):
            return d1, d2, False
        # If same number of digits cycle through all digits and compare
        # their sequence in the digit list
        else:
            print("Loop started")
            for digit in self.digit_list[::-1]:
                # If there are no digits left of the major number
                print(digit)
                if len(d1_maj) == 0:
                    if main_no:
                        # Compare the number after xcimal point
                        d_min_less, d_min_more, xcmeq = self._magn_sort(d1_min,
                                                                        d2_min,
                                                                        False)
                        # If d2 had the smaller xcimal
                        if d_min_less == d2_min:
                            return d2, d1, False
                        # If d1 is smaller xcimal or equal
                        else:
                            return d1, d2, xcmeq
                    else:
                        # Two numbers are completely equal
                        return d1, d2, True
                # Checks if either number's digit is equal to next highest
                # in digit list
                d1_eq = digit == d1[0]
                d2_eq = digit == d2[0]
                print('d1_eq: ', d1_eq)
                print('d2_eq: ', d2_eq)
                # If both are equal
                if d1_eq and d2_eq:
                    # Recursively check next number sequence
                    d_less, d_more, _ = self._magn_sort(d1_maj[1:],
                                                        d2_maj[1:],
                                                        False)
                    if d_less == d1_maj[1:]:
                        return d1, d2, False
                    else:
                        return d2, d1, False
                elif d1_eq:
                    return d2, d1, False
                elif d2_eq:
                    return d1, d2, False

    def _base_add_alg(self, d1, d2):
        print("### START BASE ADD")
        small_no, large_no, _ = self._magn_sort(d1, d2)
        print("Large no: ", large_no)
        print("Small no: ", small_no)
        result = ''
        carry = False

        for digit in range(1, len(large_no)+1):
            # Use counter to track addition sequence
            addition_counter = [c for c in self.digit_list[::-1]*2]

            # Loops through counter for large number to add
            for l_count in [lc for lc in self.digit_list]:
                if l_count == large_no[-digit]:
                    break
                last_no = addition_counter.pop()
                print("    last no:  ", last_no)

            # If addition exceeds base in previous another is added
            if carry:
                addition_counter.pop()

            # Loops through each number in small number to add
            if digit <= len(small_no):
                for s_count in [lc for lc in self.digit_list]:
                    if s_count == small_no[-digit]:
                        break
                    last_no = addition_counter.pop()
                    print("    last no:  ", last_no)

            # Adds a carry for the next loop if there is only one last digit
            # in counter (i.e. base number has been crossed)
            carry = True if len([d for d in addition_counter
                                 if d == self.digit_list[-1]]) == 1 else False
            print("Carry: ", str(carry))

            result = addition_counter[-1] + result
            print("  Result: ", result)

        # Adds the first digit of system at start if there's carry at end
        if carry:
            result = self.digit_list[1] + result

        print(" Final Result: ", result)
        print("### END BASE ADD")
        return result

    def _base_neg_alg(self, d1, d2):
        '''Base algorithm to negate two numbers however the largest
        number must go first for simplicity'''
        print("### START BASE NEG")        
        small_no, large_no = self._magn_sort(d1, d2)
        print("Large no: ", large_no)
        print("Small no: ", small_no)
        result = ''
        carry = False

        for digit in range(1, len(large_no)+1):
            # Use counter to track subtractions stack
            subtraction_counter = self.digit_list

            # Loops through counter for large number to add
            for l_count in [lc for lc in self.digit_list]:
                last_no = subtraction_counter.append(l_count)
                if l_count == large_no[-digit]:
                    break
                print("    last no:  ", last_no)

            # If addition exceeds base in previous another is added
            if carry:
                subtraction_counter.pop()

            # Loops through each number in small number to subtract
            if digit <= len(small_no):
                for s_count in [lc for lc in self.digit_list]:
                    if s_count == small_no[-digit]:
                        break
                    last_no = subtraction_counter.pop()
                    print("    last no:  ", last_no)

            # Adds a carry for the next loop if there is only one last digit
            # in counter (i.e. base number has been crossed)
            carry = True if len([d for d in subtraction_counter
                                 if d == self.digit_list[-1]]) == 1 else False
            print("Carry: ", str(carry))

            result = subtraction_counter[-1] + result
            print("  Result: ", result)

        # Adds the first digit of system at start if there's carry at end
        if carry:
            result = self.digit_list[1] + result

        print(" Final Result: ", result)
        print("### END BASE NEG")      
        return result

    def _dec_combine(self, d1, d2, arith_function):
        print("### START DEC COMBINE")
        sep = self.sep_point
        # Orders the given Sifr strings
        print('d1: ', d1, ' Type: ', str(type(d1)))
        print('d2: ', d2, ' Type: ', str(type(d2)))
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

        print("### END DEC COMBINE")      
        return arith_answer


class Sifr(object):
    '''A number type that takes a string representing the character
    and the number system represented as the class SifrSystem'''
    def __init__(self, sifr: str, sifr_system: SifrSystem):
        self.sifr = sifr
        self.sifr_system = sifr_system
        self.no_digits = len(sifr)
        self.is_neg = sifr[0] == sifr_system.sep_point

    def __repr__(self):
        return self.sifr

    def __add__(self, add_no):
        print("### START MAIN ADD")
        if self.sifr_system != add_no.sifr_system:
            raise Exception("Sifr Systems do not match and thus ",
                            "can't be added together")
        b_add = self.sifr_system._base_add_alg

        neg_sym = self.sifr_system.neg_sym

        if (not self.is_neg and not add_no.is_neg):
            return self.sifr_system._dec_combine(self.sifr,
                                                 add_no.sifr,
                                                 b_add)
        elif self.is_neg and add_no.is_neg:
            return neg_sym + self.sifr_system.dec_combine(self.sifr[1:],
                                                          add_no.sifr[1:],
                                                          b_add)

        b_neg = self.sifr_system._base_neg_alg
        self_mag = self.sifr if not self.is_neg else self.sifr[1:]
        add_no_mag = add_no.sifr if not add_no.is_neg else add_no.sifr[1:]

        sml_mag, big_mag = self.sifr_system._magn_sort(self_mag, add_no_mag)
        is_self_bigger = big_mag == self_mag

        if is_self_bigger:
            result = self.sifr_system.dec_combine(self_mag, add_no_mag, b_neg)
            result = result if not self.is_neg else neg_sym + result
        else:
            result = self.sifr_system.dec_combine(add_no_mag, self_mag, b_neg)
            result = result if self.is_neg else neg_sym + result
        print("### MAIN END ADD")
        return result

    def __sub__(self, sub_no):
        print("### MAIN START SUB")
        # If subtracted number is negative just add
        if sub_no.sifr[0] == self.sifr_system.sep_point:
            print("### MAIN END SUB")
            return self.__add__(Sifr(sub_no.sifr[1:], self.sifr_system))
        # Otherwise just add the negative
        else:
            print("### MAIN END SUB")
            return self.__add__(Sifr(self.sifr_system.neg_sym + sub_no.sifr,
                                     self.sifr_system))
