class Cipher:
    def __init__(self, seed:int, taps:int, length:int):
        self.seed = seed
        self.taps = taps
        self.length = length

        self.curr = seed
        self.stream = self.curr & 1

    def calculate(self):
        tmp = 0
        for j in range(self.length):
            # XOR with taps
            if ((self.taps >> j) & 1):
                tmp ^= (self.curr >> j) & 1

        self.curr = (self.curr >> 1) | (tmp << (self.length - 1)) # new bit added
        self.stream = (self.stream << 1) | (self.curr & 1)        # new bit to stream
    

    def nextStep(self):
        # get next number
        res = self.curr
        self.calculate()
        return res

    def nextStream(self):
        #get next stream bits
        res = self.stream
        self.calculate()

        res = res & ((1 << self.length) - 1)
        return res
    

    def nextPair(self):
        # get next number and stream bits
        res = (self.curr, self.stream)
        self.calculate()
        return res