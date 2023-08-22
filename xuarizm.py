# #############################################################################
# XUARIZM
# This file contains Xuarizm (pronounced Kwarizm after the Persian
# mathematician from which the name algorithm originates), the class used for
# calculating arithmetic (and geometric in the future) series using a given
# function calculated until it converges to the precision given by the
# SifrSystem
# #############################################################################

import logging
import pdb

from sifr import Sifr

from systems import SifrSystem

# Mae breakpoint shorter
bp = pdb.set_trace


# DECORATORS
def mask_logging(func):
    def wrapper(*args):
        prev_log_level = logging.root.level
        logging.getLogger().setLevel(logging.ERROR)
        result = func(*args)
        logging.getLogger().setLevel(prev_log_level)
        return result
    return wrapper


class Formulae(object):
    @staticmethod
    def factorial(n):
        ssys = n.ssys
        unit = Sifr(ssys.unit, ssys)
        result = Sifr(ssys.unit, ssys)
        while n != Sifr(ssys.iden, ssys):
            result *= n
            n -= unit
        return result


class Constants(object):
    def __init__(self, sifr_system):
        self.ssys = sifr_system

    def return_leibniz_pi(self, upper_bound):
        s = self.ssys
        zero = Sifr(s.iden, s)
        one = Sifr(s.unit, s)
        two = one + one
        four = two + two

        @mask_logging
        def pi_algo(k):
            if k % two == zero:
                return four / (two * k + one)
            else:
                return -four / (two * k + one)
        return Xuarizm(pi_algo, s, upper_bound=upper_bound).arith_series()

    def return_bbp_pi(self, upper_bound):
        s = self.ssys
        one = Sifr(s.unit, s)
        two = one + one
        four = two + two
        five = four + one
        six = four + two
        eight = four + four
        sixteen = eight + eight

        def pi_algo(k):
            return (one / (sixteen ** k)) * ((four / (eight * k + one))
                                             - (two / (eight * k + four))
                                             - (one / (eight * k + five))
                                             - (one / (eight * k + six)))

        return Xuarizm(pi_algo, s, upper_bound=upper_bound).arith_series()

    def return_phi(self):
        pass

    def return_e(self):
        pass


class Xuarizm(object):
    def __init__(self, algo, sifr_system: SifrSystem,
                 lower_bound=None, upper_bound=None, step=None):
        self.lbnd = (lower_bound if lower_bound is not None
                     else Sifr(sifr_system.iden, sifr_system))
        self.ubnd = upper_bound
        self.ssys = sifr_system
        self.step = step if step is not None else Sifr(sifr_system.unit,
                                                       sifr_system)

        @mask_logging
        def masked_algo(x):
            return algo(x)

        @mask_logging
        def masked_add(x, y):
            return x + y

        @mask_logging
        def masked_prod(x, y):
            return x * y

        @mask_logging
        def masked_le(x, y):
            return x <= y

        self.algo = masked_algo
        self.m_add = masked_add
        self.m_prod = masked_prod
        self.m_le = masked_le
        self.ssys = sifr_system

    def arith_series(self):
        term = self.lbnd
        result = Sifr(self.ssys.iden, self.ssys)

        logging.debug("XUARIZM: Starting term: " + result.sifr)
        while self.m_le(term, self.ubnd):
            added_value = self.algo(term)
            logging.debug("    XUARIZM: " + added_value.sifr)
            result = self.m_add(result, added_value)
            logging.debug("  XUARIZM: Running term: " + result.sifr)
            term = self.m_add(term, self.step)

        return result

    def rational_series(self):
        term = self.lbnd
        result = Sifr(self.ssys.iden, self.ssys)

        logging.debug("XUARIZM: Starting term: " + result.sifr)
        while self.m_le(term, self.ubnd):
            result = self.m_prod(result, self.algo(term))
            logging.debug("  XUARIZM: Running term: " + result.sifr)
            term = self.m_add(term, self.step)

        return result
