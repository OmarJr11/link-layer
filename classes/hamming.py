"""
    Clase Hamming
    Contará con las variables:
        isVerification = Booleano indica si el bit es de verificacion o mensaje
        position =  Entero que indica la posicion del bit
        bit =  0 o 1
        pow =  Array de Enteros que indica la descomposicion de la posicion del bit en 2**n
               Es decir la posicion 5 = [4(2**2), 1(2**1)]
    Para crear pow de la posicion se envia una lista listPow que contiene los numeros de 2**n
    donde n es el ultimo bit de verificacion hasta el bit en el que se este trabajando
"""


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
