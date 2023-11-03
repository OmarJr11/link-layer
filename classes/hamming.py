class Hamming:
    def __init__(self, isVerification: bool, position: int, bit, listPow):
        self.isVerification = isVerification
        self.position = position
        self.bit = bit
        self.pows = []
        if not isVerification:
            num = position
            for item in listPow:
                if num >= 0 and num - item >= 0:
                    num = num - item
                    self.pows.insert(0, item)
