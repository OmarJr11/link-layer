import re

BAND = '01111110'


def removeFillerBits(code):
    if not code:
        return False
    else:
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
    length = len(code)
    global BAND
    if BAND == code[0:8] and BAND == code[length-8:length]:
        return (True, code[8:len(code)-8])
    else:
        return (False, 'Codigo invalido, no contiene los bits de bandera')


def addBandBits(code):
    global BAND
    return BAND + code + BAND


"""Verifica si una cadena solo contiene los caracteres '0' y '1'"""


def es_binario(cadena):
    patron = re.compile(r"^[01]+$")
    return patron.fullmatch(cadena) is not None
