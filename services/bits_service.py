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
    bandPos = code.find('01111110')
    if (bandPos != -1) and (bandPos == 0):
        code = code[8:len(code)]

    bandPos = code.find('01111110')
    if (bandPos != -1):
        code = code[0: bandPos]

    print(code)
    return code


def addBandBits(code):
    return '01111110' + code + '01111110'
