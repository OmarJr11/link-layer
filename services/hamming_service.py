from modules.module import Hamming, removeFillerBits, addFillerBits, removeBandBits, addBandBits


def calculateBitVerification(position: int, parityPar: bool, listHamming: list[Hamming]):
    listCode = []
    bit = '0'
    for item in listHamming:
        if not item.isVerification:
            for p in item.pows:
                if p == position:
                    listCode.insert(0, item.bit)
    if parityPar:
        if listCode.count('1') % 2 != 0:
            bit = '1'
    else:
        if listCode.count('1') % 2 == 0:
            bit = '1'
    return bit


def CheckBitVerification(position: int, parityPar: bool, listHamming: list[Hamming]):
    listCode = []
    errorPosition = 0
    for item in listHamming:
        if not item.isVerification:
            for p in item.pows:
                if p == position:
                    listCode.insert(0, item.bit)
    listCode.insert(0, listHamming[position-1].bit)
    if parityPar:
        if listCode.count('1') % 2 != 0:
            errorPosition = position
    else:
        if listCode.count('1') % 2 == 0:
            errorPosition = position
    return errorPosition


def DecodeHamming(code, parityPar: bool):
    print('\nCodigo recibido:', code)
    code = removeFillerBits(removeBandBits(code))
    codeHamming = ''
    codeMessage = ''
    listCode = list(code)
    listHamming: list[Hamming] = []
    listPow = []
    exp = 0
    for i in range(len(code)):
        if len(listCode) > 0:
            resultPot = pow(2, exp)
            if resultPot == i + 1:
                listPow.insert(0, resultPot)
                exp = exp + 1
            bit = listCode.pop(0)
            listHamming.insert(i, Hamming(
                resultPot == i + 1, i+1, bit, (listPow, [])[resultPot == i + 1]))
    errorPosition: int = 0
    for item in listHamming:
        if item.isVerification:
            errorPosition = errorPosition + CheckBitVerification(
                item.position, parityPar, listHamming)
    if errorPosition > 0:
        print('Posicion del error:', errorPosition)
        listHamming[errorPosition-1].bit = (
            '1', '0')[listHamming[errorPosition-1].bit == '1']
    else:
        print('No hay error')
    for item in listHamming:
        codeHamming = codeHamming + item.bit
    for item in listHamming:
        if not item.isVerification:
            codeMessage = codeMessage + item.bit
    if errorPosition > 0:
        print('Codigo Hamming que llego: ', code)
        print('Codigo Hamming Despues de la Correccion: ', codeHamming)
        print('Codigo del Mensaje: ', codeMessage)
    else:
        print('Codigo Hamming: ', codeHamming)
        print('Codigo del Mensaje: ', codeMessage)


def CodeHamming(code, parityPar: bool):
    codeHamming = ''
    listCode = list(code)
    listHamming: list[Hamming] = []
    listPow = []
    exp = 0
    for i in range(24):
        if len(listCode) > 0:
            resultPot = pow(2, exp)
            if resultPot == i + 1:
                listPow.insert(0, resultPot)
                listHamming.insert(i, Hamming(True, i+1, '', listPow))
                exp = exp + 1
            else:
                bit = listCode.pop(0)
                listHamming.insert(i, Hamming(False, i+1, bit, listPow))
    for item in listHamming:
        if item.isVerification:
            item.bit = calculateBitVerification(
                item.position, parityPar, listHamming)
            codeHamming = codeHamming + item.bit
        else:
            codeHamming = codeHamming + item.bit

    print('Codigo Ingresado: ', code)
    print('Codigo Hamming: ', codeHamming)
    codeHamming = addFillerBits(codeHamming)
    print('Codigo Hamming con bits de relleno: ', codeHamming)
    codeHamming = addBandBits(codeHamming)
    print('Codigo Hamming con banderas: ', codeHamming)
