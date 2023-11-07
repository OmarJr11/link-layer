from modules.module import removeFillerBits, addFillerBits, removeBandBits, addBandBits
RESPONSE = True

"""
    Codificar una cadena de bits recibida con CRC
    frame = cadena de bits a codificar
    generator = polinomio generador en bits 
"""


def CodeCRC(frame, generator):
    # Se obtiene la longitud del polinomio generador
    generatorLen = len(generator)
    polynomialGrade = generatorLen - 1  # Se obtiene el grado del polinomio generador
    code = list(frame)  # Se crea un array con la cadena de bits a codificar

    divFragmentFrame = []

    # Ciclo para agregar los 0's correspondientes a la cadena de bits
    for _ in range(polynomialGrade):
        code.append('0')

    # Llamado a la funcion que realiza la division CRC que devuelve el resto que
    # se debe agregar a la trama a enviar
    divFragmentFrame = binaryDiv(code, generator)

    # Se le da el index de la ultima posicion del array del codigo
    actIndex = len(code) - 1

    # Se le da la cantidad de iteraciones a sumar el resto de la division
    index = polynomialGrade - 1

    # Resta del codigo y el resto de la division
    while actIndex >= len(code) - polynomialGrade:
        code[actIndex] = divFragmentFrame[index]
        actIndex -= 1
        index -= 1

    crc = code
    codeWithBits = addFillerBits(code)  # Se agrega el relleno de bits
    # Se agregan los bits bandera de inicio y fin
    code = addBandBits(codeWithBits)

    # Se retorna el codigo despues de la division, el codigo con los bits de relleno y el codigo con las banderas
    return (RESPONSE, crc, codeWithBits, code)


"""
    Decodificar una cadena de bits recibida con CRC
    frame = cadena de bits a decodificar 
    generator = polinomio generador en bits 
"""


def DecodeCRC(frame, generator):
    # Se remueven las banderas del codigo a decodificar
    bandBits = removeBandBits(frame)

    # Si hubo un error en las banderas no se puede determinar la cadena original por lo tanto habra un error
    if not bandBits[0]:
        return bandBits

    # Se remueven los bits de relleno
    frame = removeFillerBits(bandBits[1])

    code = list(frame)  # Array de la cadena original

    # Se realiza la division CRC para determinar el resto y saber si hubo error en la transmision
    divFragmentFrame = binaryDiv(code, generator)

    # Longitud de digitos agregados para codificar el CRC
    lengthToCut = len(generator) - 1

    # Se determina la cadena de bits original
    originalCode = code[0:len(code)-lengthToCut]

    # Si hay algun 1 en el resto de la division calculada anteriormente es que hubo un error
    # en la transmision
    if ''.join(divFragmentFrame).find('1') != -1:
        return (RESPONSE, True, code, originalCode)
    else:
        # Si el resto es 0 es porque la transmision llego bien
        return (RESPONSE, False, code, originalCode)


"""
    Division CRC
    code = codigo a dividir
    generator = polinomio generador en bits 
"""


def binaryDiv(code, generator):
    generatorLen = len(generator)  # Longitud del generador
    divFragmentFrame = []  # fragmento del dividendo en cada momento de la division
    aux = []  # array de 0s con la longitud del generador
    quotient = []  # Cociente de la division
    frameDiv = []  # Multiplicacion del divisor en cada momento tomara el valor del generador o solo 0s
    actIndex = generatorLen

    # Se llena el fragmento de la division inicial, los primeros n digitos donde n es la cantidad de bits del generador
    # y se llena el array de 0s con la longitud del generador
    for i in range(generatorLen):
        divFragmentFrame.append(code[i])
        aux.append('0')

    # Se realizan las iteraciones correspondientes a la division
    while actIndex <= len(code):

        # Si el primer bit del fragmento actual del dividendo es 1
        # Se le agrega un 1 al cociente por lo que la multiplicacion del generador sera el mismo generador
        if divFragmentFrame[0] == '1':
            frameDiv = list(generator)
            quotient.append('1')
        else:
            # Si el primer bit del fragmento actual del dividendo es 0
            # Se le agrega un 0 al cociente por lo que la multiplicacion del generador sera un array de 0s
            frameDiv = aux
            quotient.append('0')

        # Se realiza la comparacion entre el fragmento del dividento y el fragmento del divisor
        # Si ambos digitos son iguales se introduce un 0 en esa posicion para el siguiente fragmento del dividendo
        # Si son distintos se introduce un 1
        for i in range(generatorLen):
            if divFragmentFrame[i] == frameDiv[i]:
                divFragmentFrame[i] = '0'
            else:
                divFragmentFrame[i] = '1'

        # Se descarta el 0 de mas a la izquierda del fragmento del dividendo
        divFragmentFrame.pop(0)

        # Se baja el siguiente numero en el dividendo al fragmento actual para la siguiente iteracion
        if actIndex < len(code):
            divFragmentFrame.append(code[actIndex])
        actIndex += 1  # Se aunmenta el index que va recorriendo cada digito a bajar del dividendo

    # Se retorna el resto de la division
    return divFragmentFrame
