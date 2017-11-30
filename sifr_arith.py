################################################################################
#Created by Alexander Ross
#25th Novewmber 2017
################################################################################
# Sifr is the main script which calculates the main arithmetic of the
# generalised number system.
################################################################################

class sifr_add(object):
    '''Adds two numbers together (as sifrised objects).'''
    def __init__(self, add_no1, add_no2):
        self.add_no1 = add_no1
        self.add_no2 = add_no2

    def trad_add(num1, num2):
        if len(num1) > len(num2):
            big_num = num1
            lit_num = num2
        else:
            big_num = num2
            lit_num = num1
            
        lit_num = [0] * (len(big_num) - len(lit_num)) + lit_num

        num_ans = [0]
        

class sifr_mult(object):
    '''Multiplies two numbers (as sifrised objects). Multiple options including
    traditional and karatsuba multiplication can be used)'''
    
    def __init__(self, mult_no1, mult_no2):
        self.mult_no1 = mult_no1
        self.mult_no2 = mult_no2

    def trad_mult(num1, num2):
        num_ans = [0] * (len(num1) + len(num2))
    
        for i1 in range(1,len(num1) + 1):
            for i2 in range(1,len(num2) + 1):
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

    def karatsuba(num1, num2):
        a = num1[0:len(num1)/2]
        b = num1[-len(num1)/2:]
        c = num2[0:len(num2)/2]
        d = num2[-len(num2)/2:]
        comp1 = trad_mult(a, c)
        comp2 = trad_mult(b, d)
