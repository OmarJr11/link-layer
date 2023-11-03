def removeFillerBits(code):
    bits1 = 0
    newCode = ''
    for bit in code:
        if bit == '1' and bits1 < 5:
            newCode = (newCode, newCode + bit)[bits1 < 5]
            bits1 = (0, bits1 + 1)[bits1 < 5]
        elif bits1 == 5:
            bits1 = 0
        else:
            bits1 = 0
            newCode = newCode + bit
    return newCode


def addFillerBits(code):
    bits1 = 0
    newCode = ''
    for bit in code:
        if bit == '1':
            bits1 = (bits1 + 1, 0)[bits1 == 5]
            newCode = (newCode + bit, newCode + bit + '0')[bits1 == 5]
        else:
            bits1 = 0
            newCode = newCode + bit
    return newCode


def removeBandBits(code):
    return code[8:len(code)-8]


def addBandBits(code):
    return '01111110' + code + '01111110'
