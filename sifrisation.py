###############################################################################
# Created by Alexander Ross
# 25th November 2017
###############################################################################
# This script takes the number system from the list and turns it into a
# numerical dictionary number object which can then be subjected to the
# arithmetical operations in the rest of the program.
###############################################################################


class sifrisation(object):
    def __init__(self, dig_list):
        self.dig_list = dig_list

        sifr_sys = {}
        sifr_desys = {}
        counter = 0

        for sifr in dig_list:
            sifr_sys[counter] = sifr
            sifr_desys[sifr] = counter
            counter += 1

        self.sifr_sys = sifr_sys
        self.sifr_desys = sifr_desys
        self.base_no = len(dig_list)

    def sifrise(self, num_string):
        @staticmethod
        ret_list = []
        for num in num_string:
            ret_list.append(self.sifr_desys[num])

        return ret_list

    def symbolise(self, num_list):
        @staticmethod
        ret_string = ""
        for num in num_list:
            ret_string += str(self.sifr_sys[num])

        return ret_string

    def addn(self, a1, a2):
        '''Adds two numbers together (as sifrised objects).'''
        @staticmethod
        if len(a1) > len(a2):
            big_num = num1
            lit_num = num2
        else:
            big_num = num2
            lit_num = num1

            lit_num = [0] * (len(big_num) - len(lit_num)) + lit_num

        num_ans = [0]


    def mult(self, m1, m2):
        '''Multiplies two numbers (as sifrised objects). Multiple options
        including traditional and karatsuba multiplication can be used)'''

    def trad_mult(self, t1, t2):
        num_ans = [0] * (len(num1) + len(num2))

        for i1 in range(1, len(num1) + 1):
            for i2 in range(1, len(num2) + 1):
                num_ans[-(i1 + i2) + 1] += num1[-i1] * num2[-i2]
                if num_ans[-(i1 + i2) + 1] > 9:
                    tot_prod = num_ans[-(i1 + i2) + 1]
                    num_ans[-(i1 + i2) + 1] -= tot_prod - (tot_prod % 10)
                    num_ans[-(i1 + i2)] += (tot_prod - (tot_prod % 10)) / 10

        zero_count = 0

        while num_ans[zero_count] == 0 or len(num_ans) == 0:
            num_ans = num_ans[1:]
            zero_count += 1

            return num_ans

        def karatsuba_mult(self, k1, k2):
            a = num1[0:len(num1)/2]
            b = num1[-len(num1)/2:]
            c = num2[0:len(num2)/2]
            d = num2[-len(num2)/2:]
            comp1 = trad_mult(a, c)
            comp2 = trad_mult(b, d)
