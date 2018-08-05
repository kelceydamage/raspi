import math

def normalize_2d_by_pct(l1, l2):
    v1_max = max(l1)
    v2_max = max(l2)
    o1 = []
    o2 = []
    for v1, v2 in zip(l1, l2):
        o1.append(v1 / v1_max * 100)
        o2.append(v2 / v2_max * 100)   
    return o1, o2

class ChiSquare(object):
    def __init__(self, observed_series, expected_series):
        self.values = []
        self.o_series = observed_series
        self.e_series = expected_series
        self.o_max = max(self.o_series)
        self.e_max = max(self.e_series)
        self.o_test = []
        self.e_test = []
        self.chi_square = 0.0
        self.cdf = 0.0
        self.df = 1
        self.cdf_values = []

    def chi_square_single_compare(self, o, e):
        return math.pow((float(o) - float(e)), 2) / float(e)

    def calculate(self):
        for o, e in zip(self.o_series, self.e_series):
            o, e = self.normalize(o, e)
            self.o_test.append(o)
            self.e_test.append(e)
            self.values.append(self.chi_square_single_compare(o, e))
        self.chi_square = sum(self.values)

    def ilgf(self):
        s = self.df / 2.0
        z = self.chi_square / 2.0
        for k in range(0, 100):
            i1 = (math.pow((-1), float(k)) * math.pow(z, (s + float(k))))
            i2 = (math.factorial(k) * (s + k))
            if i2 != 0.0:
                v = i1 / i2
            else:
                v = 0.0
            self.cdf_values.append(v)
        return sum(self.cdf_values)

    def gamma_function(self):
        x = self.df / 2.0
        #Play with these values to adjust the error of the approximation.
        upper_bound=100.0
        resolution=1000000.0

        step= upper_bound / resolution

        val=step
        rolling_sum=0

        while val<=upper_bound:
            #print('STEP: ', step)
            #print('VAL: ', val)
            #print('X: ', x)
            rolling_sum += step * (val ** (x-1) * 2.7182818284590452353602874713526624977 ** (-val))
            #print(rolling_sum)
            val+=step

        return rolling_sum

    def cdf_func(self):
        i = self.ilgf()
        g = self.gamma_function()
        self.cdf = i / g
        print(self.cdf, i, g)
        print(self.cdf_values)

    def run(self):
        self.calculate()
        self.cdf_func()
        return self.chi_square, self.cdf

    def normalize(self, o, e):
        o = o / self.o_max
        e = e / self.e_max
        return o, e

if __name__ == "__main__":
    o = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0]
    e = [2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0]
    C = ChiSquare(o, e)
    result = C.run()
    print(result)
    print(C.o_test)
    print(C.e_test)
    print(C.values)
