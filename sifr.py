################################################################################
#Created by Alexander Ross
#25th Novewmber 2017
################################################################################
# Sifr is the main script which calculates the main arithmetic of the
# generalised number system.
################################################################################

import sifrisation

class sifr(object):
    def __init__(self, digit_list):
        self.digit_list = digit_list

    def calcul(self, operation_string):
        '''Takes a string and parses it as a formula'''
        self.operation_string = operation_string

sifrisation.sifrise() #Needs to be added

