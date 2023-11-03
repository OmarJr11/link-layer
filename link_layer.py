from modules.module import CodeHamming, DecodeHamming


def LinkLayer():
    verificationType = '0'
    code = '1'
    parity = True

    while True:
        code = input(
            "Desea codificar o corregir error (code = 1 decode= 0): ")
        verificationType = input("Eliga una opcion (Hamming = 1 CRC= 0): ")
        if code == '1':
            if verificationType == '1':
                CodeHamming(parity)
        else:
            if verificationType == '1':
                DecodeHamming('0111111011111000001101111110', parity)
        run = input('Quieres continuar (Si: 1, No: 0): ')
        if run == '0':
            break


LinkLayer()
