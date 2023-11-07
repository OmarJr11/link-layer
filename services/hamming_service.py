from modules.module import Hamming, removeFillerBits, addFillerBits, removeBandBits, addBandBits
RESPONSE = True

"""
    Calcular bit de verificacion en la posicion n (position)
    position = la posicion del bit en la cadena
    paridad = booleano que indica que tipo de paridad se est usando
    listHamming = lista de la clase hamming
"""


def calculateBitVerification(position: int, parityPar: bool, listHamming: list[Hamming]):
    listCode = []  # lista para calcular la paridad
    bit = '0'
    for item in listHamming:
        if not item.isVerification:  # Si el bit no es de verificacion
            # Recorro la lista de la descompisicion de la posicion del bit (posicion 5 = [4(2**2), 1(2**0)])
            for p in item.pows:
                # Si la posicion del bit de verificacion esta en la lista, agrego el bit a la lista para comprobar la paridad
                if p == position:
                    listCode.insert(0, item.bit)
    if parityPar:  # Si es paridad par
        if listCode.count('1') % 2 != 0:  # compruebo si la cantidad de 1 no es par
            bit = '1'  # si no es par agrego el bit 1
    else:  # Si es paridad impar
        if listCode.count('1') % 2 == 0:  # compruebo si la cantidad de 1 es par
            bit = '1'  # si es par agrego el bit 1
    return bit


"""
    Verificar bit de verificacion
    position = position del bit
    parityPar = Booleano que indica si se esta usando paridad par
    listHamming = lista de la clase hamming
"""


def CheckBitVerification(position: int, parityPar: bool, listHamming: list[Hamming]):
    listCode = []  # lista para comprobar la paridad
    errorPosition = 0
    for item in listHamming:
        if not item.isVerification:  # Si el bit no es de verificacion
            # Recorro la lista de la descompisicion de la posicion del bit (posicion 5 = [4(2**2), 1(2**0)])
            for p in item.pows:
                # Si la posicion del bit de verificacion esta en la lista, agrego el bit a la lista para comprobar la paridad
                if p == position:
                    listCode.insert(0, item.bit)
    # Agrego el bit de verificacion
    listCode.insert(0, listHamming[position-1].bit)
    if parityPar:  # Si es paridad par
        if listCode.count('1') % 2 != 0:  # compruebo si la cantidad de 1 no es par
            errorPosition = position  # si no es par, en esa posicion hay un error
    else:
        if listCode.count('1') % 2 == 0:  # compruebo si la cantidad de 1 es par
            errorPosition = position  # si es par, en esa posicion hay un error
    return errorPosition


"""
    Decodificar codigo hamming
    position = position del bit
    parityPar = Booleano que indica si se esta usando paridad par
    listHamming = lista de la clase hamming
"""


def DecodeHamming(code, parityPar: bool):
    bandBits = removeBandBits(code)  # Se remueven los bits de bandera
    if not bandBits[0]:  # Si hubo error en las banderas se devueleve el error
        return bandBits

    # Se quitan los bits de relleno si tienen
    code = removeFillerBits(bandBits[1])
    codeHamming = ''  # Codigo hamming
    codeMessage = ''  # Codigo decodificado
    listCode = list(code)  # Se crea lista con el codigo recibido
    listHamming: list[Hamming] = []
    listPow = []  # Lista para la posiciones que sean igual potencias 2**n
    exp = 0  # Primer exponente

    for i in range(len(code)):  # Se recorre el codigo ingresado
        if len(listCode) > 0:  # Si la lista todavia contiene bits

            resultPot = pow(2, exp)  # Se calcula la potencia 2**exp
            if resultPot == i + 1:  # Si la potencia es igual a la posicion actual + 1 entonces es un bit de verificacion
                listPow.insert(0, resultPot)  # Se guarda la potencia 2**exp
                exp = exp + 1  # Se pasa al siguiente exponente

            # Se desencola la primera posicion de la lista y se guarda
            bit = listCode.pop(0)

            # Se crea el objeto con la clase Hamming donde
            # Hamming( Es bit de verificacion?, Posicion, Bit, Lista de potencia hasta esa posicion )
            # y se inserta a la lista
            listHamming.insert(i, Hamming(
                resultPot == i + 1, i+1, bit, (listPow, [])[resultPot == i + 1]))

    errorPosition: int = 0
    for item in listHamming:  # Se recorre la lista hamming creada anteriormente
        if item.isVerification:  # Verifica que el bit sea de verificacion

            # Se comprueba si hay error con ese bit de verificacion
            # Si hay error se va sumando para obtener la posicion del error
            errorPosition = errorPosition + CheckBitVerification(
                item.position, parityPar, listHamming)
    print(errorPosition, len(listHamming))
    # Si es mayor a 0 es porque hay al menos un error
    if errorPosition > 0 and errorPosition < len(listHamming):
        # Se cambia el bit donde ocurrio el error 0 --> 1 o 1 --> 0
        listHamming[errorPosition-1].bit = (
            '1', '0')[listHamming[errorPosition-1].bit == '1']
    else:
        return (False, 'No se ha podido corregir el error, hay mas de un error en la trama')

    # Se crea la cadena del codigo hamming sin error
    for item in listHamming:
        codeHamming = codeHamming + item.bit

    # Se crea la cadena del codigo que se queria transmitir
    for item in listHamming:
        if not item.isVerification:
            codeMessage = codeMessage + item.bit

    return (RESPONSE, errorPosition, codeHamming, codeMessage)


"""
    Codificar codigo hamming
    code = cadena binaria ingresada
    parityPar = Booleano que indica si se esta usando paridad par
"""


def CodeHamming(code, parityPar: bool):
    codeHamming = ''
    listCode = list(code)  # Se crea lista con el codigo recibido
    listHamming: list[Hamming] = []
    listPow = []  # Lista para la posiciones que sean igual potencias 2**n
    exp = 0  # Primer exponente

    for i in range(24):  # Se recorre el codigo ingresado

        if len(listCode) > 0:  # Si la lista todavia contiene bits
            resultPot = pow(2, exp)  # Se calcula la potencia 2**exp

            if resultPot == i + 1:  # Si la potencia es igual a la posicion actual + 1 entonces es un bit de verificacion
                listPow.insert(0, resultPot)  # Se guarda la potencia 2**exp

                # Se crea el objeto con la clase Hamming donde
                # Hamming( Es bit de verificacion?, Posicion, Bit, Lista de potencia hasta esa posicion )
                # y se inserta a la lista
                listHamming.insert(i, Hamming(True, i+1, '', listPow))
                exp = exp + 1  # Se pasa al siguiente exponente

            else:  # Si no es un bit de verificacion
                # Se guarda el primer bit de la lista que seria el primer bit de mensaje
                bit = listCode.pop(0)

                # Se crea el objeto con la clase Hamming donde
                # Hamming( Es bit de verificacion?, Posicion, Bit, Lista de potencia hasta esa posicion )
                # y se inserta a la lista
                listHamming.insert(i, Hamming(False, i+1, bit, listPow))

    for item in listHamming:  # Se recorre la lista hamming creada anteriormente
        if item.isVerification:  # Verifica que el bit sea de verificacion
            # Se calcula el valor del bit de verificacion
            item.bit = calculateBitVerification(
                item.position, parityPar, listHamming)
        codeHamming = codeHamming + item.bit

    global RESPONSE
    fillerBits = addFillerBits(codeHamming)  # se agregan el relleno de bits
    return (RESPONSE, codeHamming, fillerBits, addBandBits(fillerBits))
