from modules.module import removeFillerBits, addFillerBits, removeBandBits, addBandBits
RESPONSE = True


def CodeCRC(frame, generator):
    generatorLen = len(generator)
    polynomialGrade = generatorLen - 1
    code = list(frame)

    divFragmentFrame = []

    for _ in range(polynomialGrade):
        code.append('0')

    divFragmentFrame = binaryDiv(code, generator)

    actIndex = len(code) - 1
    index = polynomialGrade - 1
    while actIndex >= len(code) - polynomialGrade:
        code[actIndex] = divFragmentFrame[index]
        actIndex -= 1
        index -= 1

    crc = code
    codeWithBits = addFillerBits(code)
    code = addBandBits(codeWithBits)

    return (RESPONSE, crc, codeWithBits, code)


def DecodeCRC(frame, generator):
    bandBits = removeBandBits(frame)
    if not bandBits[0]:
        return bandBits
    frame = removeFillerBits(bandBits[1])
    code = list(frame)

    divFragmentFrame = binaryDiv(code, generator)

    lengthToCut = len(generator) - 1

    originalCode = code[0:len(code)-lengthToCut]

    if ''.join(divFragmentFrame).find('1') != -1:
        return (RESPONSE, True, code, originalCode)
    else:
        return (RESPONSE, False, code, originalCode)


def binaryDiv(code, generator):
    generatorLen = len(generator)
    divFragmentFrame = []
    aux = []
    quotient = []
    frameDiv = []
    actIndex = generatorLen

    for i in range(generatorLen):
        divFragmentFrame.append(code[i])
        aux.append('0')

    while actIndex <= len(code):
        if divFragmentFrame[0] == '1':
            frameDiv = list(generator)
            quotient.append('1')
        else:
            frameDiv = aux
            quotient.append('0')

        for i in range(generatorLen):
            if divFragmentFrame[i] == frameDiv[i]:
                divFragmentFrame[i] = '0'
            else:
                divFragmentFrame[i] = '1'

        divFragmentFrame.pop(0)

        if actIndex < len(code):
            divFragmentFrame.append(code[actIndex])
        actIndex += 1

    return divFragmentFrame
