################################################################################
#Created by Alexander Ross
#2nd July 2022
################################################################################
# Sifr is the main script which calculates the main arithmetic of the
# generalised number system.
################################################################################

class SifrSystem(object):
    def __init__(self, digit_list):
        if len(set(digit_list)) != len(digit_list):
            raise Exception("The list off characters is not unique and thus can't be used as a numbering system")
        self.digit_list = digit_list
        self.base_no = len(self.digit_list)

class Sifr(object):
    def __init__(self, sifr: str, sifr_system: SifrSystem):
        self.sifr = sifr
        self.sifr_system = sifr_system
        self.no_digits = len(sifr)

    def __repr__(self):
        return self.sifr

    def __add__(self, add_no):
        if add_no.no_digits > self.no_digits:
            small_no = self
            large_no = add_no
        else:
            small_no = add_no
            large_no = self

        result = ''
        print("Large no: ", str(large_no))
        print("Small no: ", str(small_no))

        carry = False
        
        for digit in range(1, large_no.no_digits+1):
            addition_counter = [c for c in self.sifr_system.digit_list[::-1]*2]
            if carry:
                addition_counter.pop()
            for s in [sc for sc in self.sifr_system.digit_list]:
                if s == large_no.sifr[-digit]:
                    break
                last_no = addition_counter.pop()
                print("    last no:  ", last_no)

            if digit <= small_no.no_digits:
                for l in [lc for lc in self.sifr_system.digit_list]:
                    if l == small_no.sifr[-digit]:
                        break
                    last_no = addition_counter.pop()
                    print("    last no:  ", last_no)

            carry = True if len([d for d in addition_counter \
                                 if d==self.sifr_system.digit_list[0]])==0 \
                        else False

            result = addition_counter[-1] + result
            print("  Result: ", result)
            
        return Sifr(result, self.sifr_system)

