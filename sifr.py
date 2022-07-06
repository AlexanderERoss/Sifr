################################################################################
#Created by Alexander Ross
#2nd July 2022
################################################################################
# Sifr is the main script which calculates the main arithmetic of the
# generalised number system.
################################################################################

class SifrSystem(object):
    def __init__(self, digit_list, dec_point, neg_sym='-'):
        if len(set(digit_list)) != len(digit_list):
            raise Exception("The list off characters is not unique " +
                            "and thus can't be used as a numbering system")
        self.digit_list = digit_list
        self.dec_point = dec_point
        self.base_no = len(self.digit_list)

    def base_add_alg(self, d1, d2):
        if len(d1) > len(d2):
            small_no = d2
            large_no = d1
        else:
            small_no = d1
            large_no = d2

        result = ''
        print("Large no: ", large_no)
        print("Small no: ", small_no)

        carry = False
        
        for digit in range(1, len(large_no)+1):
            addition_counter = [c for c in self.digit_list[::-1]*2]
            if carry:
                addition_counter.pop()
            for s in [sc for sc in self.digit_list]:
                if s == large_no[-digit]:
                    break
                last_no = addition_counter.pop()
                print("    last no:  ", last_no)

            if digit <= len(small_no):
                for l in [lc for lc in self.digit_list]:
                    if l == small_no[-digit]:
                        break
                    last_no = addition_counter.pop()
                    print("    last no:  ", last_no)

            carry = True if len([d for d in addition_counter \
                                 if d==self.digit_list[-1]])==1 \
                        else False
            print(str(carry))

            result = addition_counter[-1] + result
            print("  Result: ", result)
        if carry:
            result = self.digit_list[1] + result
            
        print(" Final Result: ", result)
        return result

class Sifr(object):
    def __init__(self, sifr: str, sifr_system: SifrSystem):
        self.sifr = sifr
        self.sifr_system = sifr_system
        self.no_digits = len(sifr)

    def __repr__(self):
        return self.sifr

    def __add__(self, add_no):
        dec = self.sifr_system.dec_point
        digits1 = self.sifr.split(dec)
        digits2 = add_no.sifr.split(dec)
        iden = self.sifr_system.digit_list[0]
        n1 = digits1[0]
        
        if len(digits2) > 1:
            d1 = digits1[1] 
        else:
            d1 = iden

        if len(digits2) > 1:
            d2 = digits2[1]
        else:
            d2 = iden
            
        n2 = digits2[0]


        print("n1: ", n1)
        print("d1: ", d1)
        print("n2: ", n2)
        print("d2: ", d2)
        
        b_add = self.sifr_system.base_add_alg

        if len(d1) >= len(d2):
            dlg = [dg1 for dg1 in d1]
            dsml = [dg2 for dg2 in d2]
        else:
            dlg = [dg2 for dg2 in d2]
            dsml = [dg1 for dg1 in d1]

        d_large = ''
        d_small = ''
        
        for dig in dlg:
            d_large += dig
            if len(dsml) > 0:
                d_small += dsml[0]
                dsml = dsml[1:]
            else:
                d_small += iden

        print("d_large: ", d_large)
        print("d_small: ", d_small)
            
        d_tot = [dt for dt in b_add(d_large, d_small)]
        d = ''

        # Takes the extra number at the start of the decimal add
        for d_fin in d_large:
            d = d_tot.pop() + d

        if len(d_tot) > 0:
            n = b_add(b_add(n1, n2), d_tot[0])
        else:
            n = b_add(n1, n2)
        
        sifr_string = n + dec + d

        return Sifr(sifr_string, self.sifr_system)
