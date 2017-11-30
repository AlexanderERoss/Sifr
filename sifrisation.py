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

    def sifr_dictise(self):
        sifr_dict = {}
        counter = 1
        
        for sifr in dig_list:
            sifr_dict[counter] = sifr
            counter += 1

        ret sifr_dict            
        
    def string_to_list(num_string):
        ret_list = []
        for num in num_string:
            ret_list.append(int(num))

        return ret_list

    def list_to_string(num_list):
        ret_string = ""
        for num in num_list:
            ret_string += str(num)

        return ret_string
