# #############################################################################
# Created by Alexander Ross
# 2nd July 2022
# Version 0.2
# #############################################################################
# Sifr is the main script which calculates the main arithmetic of the
# generalised number system.
# It's purpose is not efficiency, but rather to break down mathematical
# processes to its component functions and generalizability.
# This file contains the code to instantiated a Sifr number whilst importing
# SifrSystem class to define the system in which it operates.
# As a general rule the signing of the Sifr is dealt with within the dunder
# method in this file, all other items (xcimal points, recursion for operation
# etc.) are calculated in the SifrSystem object imported.
# #############################################################################

import logging
import pdb

from systems import SifrSystem

# Make breakpoint shorter
bp = pdb.set_trace


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
        logging.debug("### START MAIN MAGNITUDE")
        if self.ssys.neg_sym != self.sifr[0]:
            result = Sifr(self.ssys._norm_ans(self.sifr), self.ssys)
        else:
            result = Sifr(self.ssys._norm_ans(self.sifr[1:]), self.ssys)
        logging.debug("### END MAIN MAGNITUDE")
        return result

    def __neg__(self):
        logging.debug("### START MAIN NEGATION")
        if self.is_neg:
            result = Sifr(self.ssys._norm_ans(self.sifr[1:]), self.ssys)
        else:
            result = Sifr(self.ssys._norm_ans(self.ssys.neg_sym + self.sifr),
                          self.ssys)
        logging.debug("### END MAIN NEGATION")
        return result

    def __pos__(self):
        logging.debug("### START MAIN POSITIVE")
        logging.debug("### END MAIN POSITIVE")
        return Sifr(self.ssys._norm_ans(self.sifr), self.ssys)

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
            logging.info("  Only one of either numbers is negative, " +
                         "to subtract absolute values")
            b_neg = self.ssys._base_subt_alg
            self_mag = self.sifr if not self.is_neg else self.sifr[1:]
            add_no_mag = add_no.sifr if not add_no.is_neg else add_no.sifr[1:]
            added, zero_crossed = dec_comb(self_mag, add_no_mag, b_neg)
            if self.is_neg and zero_crossed:
                result = Sifr(norm(added), self.ssys)
            elif self.is_neg and not zero_crossed:
                result = Sifr(norm(neg_sym + added), self.ssys)
            elif not self.is_neg and zero_crossed:
                result = Sifr(norm(neg_sym + added), self.ssys)
            elif not self.is_neg and not zero_crossed:
                result = Sifr(norm(added), self.ssys)

        logging.debug("### END MAIN ADD")
        return result

    def __sub__(self, sub_no):
        logging.debug("### MAIN START SUB")
        norm = self.ssys._norm_ans
        # If subtracted number is negative just add
        if sub_no.sifr[0] == self.ssys.neg_sym:
            logging.debug("### END MAIN SUB")
            result = self.__add__(Sifr(sub_no.sifr[1:], self.ssys))
        # Otherwise just add the negative
        else:
            logging.debug("### END MAIN SUB")
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
            result = Sifr(self.ssys._norm_ans(raw_result), self.ssys)
        else:
            result = Sifr(self.ssys._norm_ans(self.ssys.neg_sym + raw_result),
                          self.ssys)
            result = result - Sifr(self.ssys.digit_list[1], self.ssys)
        logging.debug("### END FLOOR DIV")
        return result

    def __mod__(self, div_no):
        logging.debug("### START MAIN MOD")
        logging.debug("    Seeing what is left over when int " + div_no.sifr +
                      "'s are removed from " + self.sifr)
        raw_result = self.ssys._times_in_num(self.__abs__().sifr,
                                             div_no.__abs__().sifr)[1]
        if div_no.is_neg:
            result = Sifr(self.ssys._norm_ans(self.ssys.neg_sym + raw_result),
                          self.ssys)
        else:
            result = Sifr(self.ssys._norm_ans(raw_result),
                          self.ssys)
        if self.is_neg != div_no.is_neg:
            result = div_no - result
        logging.debug("### END MAIN MOD")
        return result

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

    def __pow__(self, exp):
        logging.info("### START MAIN EXPONENTIATION")
        logging.info("   " + self.sifr + " to the power of " + exp.sifr)

        raw_result = self.ssys._int_exp(self.__abs__().sifr,
                                        exp.__abs__().sifr)
        logging.debug("  Raw result without negatives: " + raw_result)

        if exp.is_neg:
            logging.debug("    Exponent is negative")
            inv_result = Sifr(self.ssys._norm_ans(raw_result), self.ssys)
            result = Sifr(self.ssys.unit, self.ssys) / inv_result

        else:
            logging.debug("    Exponent is positive")
            result = Sifr(self.ssys._norm_ans(raw_result), self.ssys)

        if self.is_neg:
            logging.debug("    Number to be exponentiated is negative")
            two_mod = exp % (Sifr(self.ssys.unit, self.ssys) +
                             Sifr(self.ssys.unit, self.ssys))
            if two_mod == Sifr(self.ssys.unit, self.ssys):
                logging.debug("    Exponent is odd therefore answer " +
                              "is negative")
                result = Sifr(self.ssys.neg_sym + result.sifr, self.ssys)

        logging.info("### END MAIN EXPONENTIATION: " + result.sifr)
        return result

    # RELATIONAL DUNDERS
    def __eq__(self, d):
        logging.debug("### START MAIN EQUAL")
        logging.debug("    Comparing " + self.sifr + " and " + d.sifr)
        if not self.is_neg and not d.is_neg:
            _, equal = self.ssys._orderer(self.sifr, d.sifr)
        elif self.is_neg and d.is_neg:
            _, equal = self.ssys._orderer(self.__abs__().sifr,
                                          d.__abs__().sifr)
        elif self.is_neg and not d.is_neg:
            equal = False
        elif not self.is_neg and d.is_neg:
            equal = False
        logging.debug("### END MAIN EQUAL")
        return equal

    def __gt__(self, d):
        logging.debug("### START MAIN GREATER THAN")
        if not self.is_neg and not d.is_neg:
            greater, _ = self.ssys._orderer(self.sifr, d.sifr)
        elif self.is_neg and d.is_neg:
            not_greater, equal = self.ssys._orderer(self.__abs__().sifr,
                                                    d.__abs__().sifr)
            greater = not not_greater and not equal
        elif self.is_neg and not d.is_neg:
            greater = False
        elif not self.is_neg and d.is_neg:
            greater = True
        logging.debug("### END MAIN GREATER THAN")
        return greater

    def __lt__(self, d):
        logging.debug("### START MAIN LESS THAN")
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
        logging.debug("### END MAIN LESS THAN")
        return not greater and not equal

    def __ge__(self, d):
        logging.debug("### START MAIN GREATER THAN OR EQUAL TO")
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
        logging.debug("### END MAIN GREATER THAN OR EQUAL TO")
        return greater or equal

    def __le__(self, d):
        logging.debug("### START MAIN LESS THAN OR EQUAL TO")
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
        logging.debug("### END MAIN LESS THAN OR EQUAL TO")
        return not greater or equal

    # Extra Unary Functions

    def round(self, round_level):
        if not self.is_neg:
            rounded = self.ssys.round(self.sifr, round_level)
        else:
            rounded = self.ssys.neg_sym + self.ssys.round(self.__abs__().sifr,
                                                          round_level)
        return Sifr(rounded, self.ssys)
