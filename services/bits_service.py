import re

BAND = '01111110'

"""
    Remover bit de relleno
    code = Codigo binario con relleno 
"""


def removeFillerBits(code):
    if not code:
        return False
    else:
        bits1 = 0  # Contador de bits 1
        newCode = ''  # Nuevo codigo sin bandera
        for bit in code:
            # si no he conseguido los 5 bit 1 seguido
            if bit == '1' and bits1 < 5:
                # Se copia el bit y se aumenta el contador de bits 1
                newCode = newCode + bit
                bits1 = bits1 + 1
            elif bits1 == 5:
                # si ya hay 5 bits 1 seguido, no se copia el bit porque seria la bandera
                bits1 = 0
            else:
                # si es 0 se reinicia el conteo de bits 1 y se copia el bit
                bits1 = 0
                newCode = newCode + bit
        return newCode


"""
    Agregar bit de relleno 
    code = Codigo binario 
"""


def addFillerBits(code):
    bits1 = 0  # Contador de bit 1
    newCode = ''  # Codigo bonario con bit de relleno
    for bit in code:
        if bit == '1':
            # Si ya hay cinco bits 1 seguido, se reinicia el contador sino se auments en uno
            bits1 = (bits1 + 1, 0)[bits1 == 5]
            # si hay 5 bits 1 seguido se colocal el bit actual y se le agrega el relleno sino solo se copia el bit actual
            newCode = (newCode + bit, newCode + bit + '0')[bits1 == 5]
        else:
            bits1 = 0  # si el bit es 0 se reinicia el contador
            newCode = newCode + bit  # se copia el bit 0
    return newCode


"""
    Remover Bits Bandera 
    code = Codigo binario con bit de relleno 
"""


def removeBandBits(code):
    length = len(code)  # longitud del codigo
    global BAND  # bandera = 01111110
    # Si los primeros y los ultimos 8 bits es igual a la bandera
    if BAND == code[0:8] and BAND == code[length-8:length]:
        newCode = code[8:len(code)-8]  # Codigo sin bandera
        return (
            (False, 'Codigo invalido, el codigo sin las banderas contiene mas de 24 bits'),
            (True, newCode)
        )[len(newCode) <= 24]
    else:
        # sino se retorna  un error
        return (False, 'Codigo invalido, no contiene los bits de bandera')


"""
    Agrega los bits de bandera al inicio y al final de la bandera
    code = codigo binario con bits de relleno 
"""


def addBandBits(code):
    global BAND
    return BAND + code + BAND


"""
    Verifica si una cadena solo contiene los caracteres '0' y '1'
"""


def es_binario(cadena):
    patron = re.compile(r"^[01]+$")
    return patron.fullmatch(cadena) is not None
