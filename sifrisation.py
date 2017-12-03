################################################################################
#Created by Alexander Ross
#25th November 2017
################################################################################
# This script takes the number system from the list and turns it into a
# numerical dictionary number object which can then be subjected to the
# arithmetical operations in the rest of the program.
################################################################################

class sifrisation(object):
    def __init__(self, dig_list):
        self.dig_list = dig_list

        sifr_sys = {}
        sifr_desys = {}
        counter = 1
        
        for sifr in dig_list:
            sifr_sys[counter] = sifr
            sifr_desys[sifr] = counter
            counter += 1

        self.sifr_sys = sifr_sys
        self.sifr_desys = sifr_desys
        
    def sifrise(self, num_string):
        ret_list = []
        for num in num_string:
            ret_list.append(self.sifr_desys[num])

        return ret_list

    def symbolise(self, num_list):
        ret_string = ""
        for num in num_list:
            ret_string += str(self.sifr_sys[num])

        return ret_string
    

    def addn(self, a1, a2):
        pass
    
    def mult(self, m1, m2):
        pass
