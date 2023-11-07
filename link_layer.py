from modules.module import CodeHamming, DecodeHamming, DecodeCRC, CodeCRC, es_binario
from tkinter import *
from tkinter import ttk

# Declaracion de la ventana princial
window = Tk()
window.title('Capa de enlace')
window.geometry('800x600')
window.columnconfigure(0, weight=1)

# Declaracion del frame principal de la vista
frm = Frame(window, padx=20, pady=20, background='#353b48',)
frm.columnconfigure(0, weight=1)
frm.rowconfigure(0, weight=1)
frm.grid(sticky="nsew")
frm.pack(fill='both', expand=True, side='top')

# Declaracion de los distintos frames de cada vista
frm1: Frame
frm2: Frame
frm3: Frame
frm4: Frame
frm5: Frame

mode: bool  # Modo de codificacion o decodificacion
hamming: bool  # Modo Hamming o CRC
parity: bool  # Paridad par o impar
code: str  # Codigo recibido para codificar o decodificar
generator: str  # Polinomio generador
# Trama codificada anteriormente que puede ser decodificada si asi se quiere
sentFrame: str = ''

# Creacion de estilos para los botones
styles = ttk.Style()
styles.configure(
    "MyButton.TButton",
    foreground="#353b48",
    padding=10,
    font=('', 14),
    cursor='pointer'
)

""" Funcion que pasa de una vista a otra y guarda la informacion suministrada """


def destroyFrm(num, data):
    # Si el Frame es el numero 1 se destruye dicho frame y se guarda el modo codificacion o decoficacion
    if num == 1:
        frm1.destroy()
        global mode
        mode = data
        view_two(False)  # Se muestra la vista numero 2

    # Si el Frame es el numero 2 se destruye dicho frame y se guarda la cadena de bits a tratar
    elif num == 2:
        frm2.destroy()
        global code
        code = data
        # Si es codificacion se debe verificar la longitud de la cadena y cualquier caso debe verificarse que la
        # cadena sumistrada solo tenga 1s y 0s
        if mode:
            if es_binario(code) and len(code) <= 24:
                view_three()  # Se muestra la vista numero 3
            else:
                # Se muestra la vista numero 2 para que vuelve introducir la cadena y que sea valida
                view_two(True)
        else:
            if es_binario(code):
                view_three()  # Se muestra la vista numero 3
            else:
                # Se muestra la vista numero 2 para que vuelve introducir la cadena y que sea valida
                view_two(True)

    # Si el Frame es el numero 3 se destruye dicho frame y se guarda el metodo a utilizar Hamming o CRC
    elif num == 3:
        frm3.destroy()
        global hamming
        hamming = data  # True = Hamming     False = CRC
        view_four(False)  # Se muestra la vista numero 4

    # Si el Frame es el numero 4 se destruye dicho frame y se guarda la paridad en caso de ser Hamming
    elif num == 4:
        frm4.destroy()
        global parity
        parity = data

        # Se valida si es codificacion o decodificacion
        if mode:
            # Se llama al servicio Hamming de codificacion
            result: tuple = CodeHamming(code, parity)
            if result[0]:
                # Funcion que muestra el resultado de la codificacion
                hamming_result_view(result, True)
        else:
            # Se llama al servicio Hamming de decodificacion
            result: tuple = DecodeHamming(code, parity)
            if result[0]:
                # Funcion que muestra el resultado de la decodificacion
                hamming_result_view(result, False)
            else:
                # Funcion que se muestra si las banderas no son validad
                invalidBands(result)

    # Si el Frame es el numero 5 se destruye dicho frame y se guarda el polinomio generador en caso del CRC
    elif num == 5:
        frm4.destroy()
        global generator
        generator = data

        # Se valida que el generador sea valido
        if es_binario(generator) and len(generator) <= 5:
            # Se valida so es codificacion o decodificacion
            if mode:
                # Se llama al servicio CRC de codificacion
                result: tuple = CodeCRC(code, generator)
                if result[0]:
                    # Funcion que muestra el resultado de la codificacion
                    hamming_result_view(result, True)
            else:
                # Se llama al servicio CRC de decodificacion
                result: tuple = DecodeCRC(code, generator)
                if result[0]:
                    # Funcion que muestra el resultado de la decodificacion
                    hamming_result_view(result, False)
                else:
                    # Funcion que se muestra si las banderas no son validad
                    invalidBands(result)
        else:
            # Si el generador es invalido se llama de nuevo a la vista 4 para que sea ingresado de nuevo
            view_four(True)
    else:
        # Si se desea iniviar otro proceso se destruye el frame 5 y se llama de nuevo a la primera vista
        frm5.destroy()
        view_one()


""" Funcion para reiniciar el proceso por si hubo alguna equivocacion """


def resetFrm(num):
    # Se destruye el frame actual y se llama al primer frame
    if num == 2:
        frm2.destroy()
    elif num == 3:
        frm2.destroy()
        frm3.destroy()
    elif num == 4:
        frm2.destroy()
        frm3.destroy()
        frm4.destroy()
    view_one()


""" 
Funcion que muestra la primera vista y guarda el modo si sera codificacion o decodificacion
"""


def view_one():
    global frm1

    # Se maqueta la primera vista
    frm1 = Frame(frm, padx=10, pady=10, )
    frm1.columnconfigure(0, weight=1)
    frm1.columnconfigure(1, weight=1)
    frm1.rowconfigure(0, weight=1)
    frm1.rowconfigure(1, weight=1)
    frm1.grid(sticky="nsew")

    # Label para mostrar un mensaje
    ttk.Label(frm1, text="Desea codificar o decodificar una trama:", font=('', 18)).grid(
        column=0, columnspan=2, row=0,)

    # Boton para elegir codificacion
    ttk.Button(frm1, text="Codificar",
               command=lambda: destroyFrm(1, True), style="MyButton.TButton").grid(column=0, row=1,)

    # Boton para elegir decodificaion
    ttk.Button(frm1, text="Decodificar",
               command=lambda: destroyFrm(1, False), style="MyButton.TButton").grid(column=1, row=1, )


""" 
Funcion que muestra la segunda vista y guarda la cadena binaria a utilizar
"""


def view_two(error):
    global frm2

    # Se maqueta la segunda vista
    frm2 = Frame(frm, padx=10, pady=10)
    frm2.columnconfigure(0, weight=1)
    frm2.columnconfigure(1, weight=1)
    frm2.rowconfigure(0, weight=1)
    frm2.rowconfigure(1, weight=1)
    frm2.grid(sticky="nsew")

    # Se valida si se esta mostrando de nuevo la vista por algun error
    if not error:
        # Label para mostrar un mensaje
        ttk.Label(frm2, text="Ingrese el codigo (en bits):", font=('', 18)).grid(
            column=0, columnspan=2, row=0)
    else:
        # Label para mostrar un mensaje
        ttk.Label(frm2, text="Ingrese un codigo valido (en bits):", font=('', 18)).grid(
            column=0, columnspan=2, row=0)

    # Input para recibir la cadena de bits
    entry = ttk.Entry(frm2, width=40, font=('', 14),)
    entry.grid(
        column=0, row=1, ipadx=5, ipady=5)

    # Boton para continuar
    ttk.Button(frm2, text="Enter", style="MyButton.TButton",
               command=lambda: destroyFrm(2, entry.get())).grid(column=1, row=1)

    # Se valida si es codificacion o decodificacion para colocar un boton que permita decodificar
    # la trama anteriormente decodificada
    if not mode:
        # Boton para regresar a la primera vista
        ttk.Button(frm2, text="Regresar", style="MyButton.TButton",
                   command=lambda: resetFrm(2)).grid(column=0, row=2)

        # Boton para usar la trama codificadol anteriormente
        ttk.Button(frm2, text="Codigo Anterior", style="MyButton.TButton",
                   command=lambda: entry.insert(0, sentFrame)).grid(column=1, row=2)
    else:
        # Boton para regresar a la primera vista
        ttk.Button(frm2, text="Regresar", style="MyButton.TButton",
                   command=lambda: resetFrm(2)).grid(column=0, row=2, columnspan=2)


""" 
Funcion que muestra la tercera vista y se pregunta el metodo a utilizar Hamming o CRC
"""


def view_three():
    global frm3

    # Se maqueta la tercera vista
    frm3 = Frame(frm, padx=10, pady=10)
    frm3.columnconfigure(0, weight=1)
    frm3.columnconfigure(1, weight=1)
    frm3.rowconfigure(0, weight=1)
    frm3.rowconfigure(1, weight=1)
    frm3.grid(sticky="nsew")

    # Label para mostrar un mensaje
    ttk.Label(frm3, text="Metodo a utilizar:", font=('', 18)).grid(
        column=0, columnspan=2, row=0)

    # Boton para elegir metodo Hamming
    ttk.Button(frm3, text="Hamming", style="MyButton.TButton", command=lambda: destroyFrm(3, True)).grid(
        column=0, row=1)

    # Boton para elegir metodo CRC
    ttk.Button(frm3, text="CRC", style="MyButton.TButton",
               command=lambda: destroyFrm(3, False)).grid(column=1, row=1)

    # Boton para regresar a la primera vista
    ttk.Button(frm3, text="Regresar", style="MyButton.TButton",
               command=lambda: resetFrm(3)).grid(column=0, row=2, columnspan=2)


""" 
Funcion que muestra la cuarta vista y se pregunta la paridad a utilizar si es Hamming o
polinomio generador si es CRC
"""


def view_four(error):
    global frm4
    global hamming

    # Se maqueta la cuarta vista vista
    frm4 = Frame(frm, padx=10, pady=10)
    frm4.columnconfigure(0, weight=1)
    frm4.columnconfigure(1, weight=1)
    frm4.rowconfigure(0, weight=1)
    frm4.rowconfigure(1, weight=1)
    frm4.grid(sticky="nsew")

    # Se validad si es Hamming o CRC
    if hamming:
        # Label para mostrar un mensaje
        ttk.Label(frm4, text="Paridad a utilizar:", font=('', 18)).grid(
            column=0, columnspan=2, row=0)

        # Boton para elegit partidad par
        ttk.Button(frm4, text="Par", style="MyButton.TButton", command=lambda: destroyFrm(4, True)).grid(
            column=0, row=1)

        # Boton para elegit partidad impar
        ttk.Button(frm4, text="Impar", style="MyButton.TButton",
                   command=lambda: destroyFrm(4, False)).grid(column=1, row=1)
    else:
        # Se validad si hubo un erro al ingresar el polinomio anteriormente
        if not error:
            # Label para mostrar un mensaje
            ttk.Label(frm4, text="Ingrese el polinomio generador (en bits, maximo 5 bits):", font=('', 18)).grid(
                column=0, columnspan=2, row=0)
        else:
            # Label para mostrar un mensaje
            ttk.Label(frm4, text="Ingrese un polinomio generador valido (en bits, maximo 5 bits):", font=('', 18)).grid(
                column=0, columnspan=2, row=0)

        # Input para recibir el polinomio generador
        entry = ttk.Entry(frm4, width=40, font=('', 14),)
        entry.grid(
            column=0, row=1, ipadx=5, ipady=5)

        # Boton para continuar
        ttk.Button(frm4, text="Enter", style="MyButton.TButton",
                   command=lambda: destroyFrm(5, entry.get())).grid(column=1, row=1)

    # Boton para regresar a la primera vista
    ttk.Button(frm4, text="Regresar", style="MyButton.TButton",
               command=lambda: resetFrm(4)).grid(column=0, row=2, columnspan=2)


""" 
Funcion que muestra los resultados
"""


def hamming_result_view(result: tuple, isCode: bool):
    global frm5
    global sentFrame

    # Se maqueta la quinta vista
    frm5 = Frame(frm, padx=10, pady=10)
    frm5.columnconfigure(0, weight=1)
    frm5.rowconfigure(0, weight=1)
    frm5.rowconfigure(1, weight=1)
    frm5.rowconfigure(2, weight=1)
    frm5.rowconfigure(3, weight=1)
    frm5.rowconfigure(4, weight=1)
    frm5.rowconfigure(5, weight=1)
    frm5.rowconfigure(6, weight=1)
    frm5.grid(sticky="nsew")

    # Se valida que el resultado el resultado fue obtenido satisfactoriamente
    if result[0]:
        # Se valida si es codificacion o decodificacion
        if isCode:
            # Se valida si es hamming o CRC
            if hamming:
                # Se imprimen los resultados del Hamming
                ttk.Label(frm5, text="Codigo Hamming: ", font=('', 18), width=100).grid(
                    column=0, row=0)
                ttk.Label(frm5, text=result[1], font=('', 18)).grid(
                    column=0, row=1)
                ttk.Label(frm5, text="Codigo Hamming con relleno de bit: ", font=('', 18), width=100).grid(
                    column=0, row=2)
                ttk.Label(frm5, text=result[2], font=('', 18),).grid(
                    column=0, row=3)
                ttk.Label(frm5, text="Codigo Hamming con bits bandera: ", font=('', 18), width=100).grid(
                    column=0, row=4)
                ttk.Label(frm5, text=result[3], font=('', 18)).grid(
                    column=0, row=5)
                sentFrame = result[3]
            else:
                # Se imprimen los resultados del CRC
                ttk.Label(frm5, text="Codigo CRC: ", font=('', 18), width=100).grid(
                    column=0, row=0)
                ttk.Label(frm5, text=result[1], font=('', 18)).grid(
                    column=0, row=1)
                ttk.Label(frm5, text="Codigo CRC con relleno de bit: ", font=('', 18), width=100).grid(
                    column=0, row=2)
                ttk.Label(frm5, text=result[2], font=('', 18)).grid(
                    column=0, row=3)
                ttk.Label(frm5, text="Codigo CRC con bits bandera: ", font=('', 18), width=100).grid(
                    column=0, row=4)
                ttk.Label(frm5, text=result[3], font=('', 18)).grid(
                    column=0, row=5)
                sentFrame = result[3]

        # Decodificacion
        else:
            # Se valida si es hamming o CRC
            if hamming:
                # Se validad si hay un error
                if result[1] > 0:
                    # Se muestran los detalles del error
                    ttk.Label(frm5, text="Error en la posicion: ", font=('', 18), width=100).grid(
                        column=0, row=0)
                    ttk.Label(frm5, text=result[1], font=('', 18)).grid(
                        column=0, row=1)
                else:
                    ttk.Label(frm5, text="No hay error", font=('', 18), width=100).grid(
                        column=0, row=0)
                # Se imprimen los resultados
                ttk.Label(frm5, text="Codigo Hamming: ", font=('', 18), width=100).grid(
                    column=0, row=2)
                ttk.Label(frm5, text=result[2], font=('', 18)).grid(
                    column=0, row=3)
                ttk.Label(frm5, text="Codigo Hamming decodificado: ", font=('', 18), width=100).grid(
                    column=0, row=4)
                ttk.Label(frm5, text=result[3], font=('', 18)).grid(
                    column=0, row=5)
            else:
                # Se validad si hay un error
                if result[1]:
                    ttk.Label(frm5, text="Hubo un error en la transmicion", font=('', 18), width=100).grid(
                        column=0, row=0)
                else:
                    ttk.Label(frm5, text="Trama recibida correctamente", font=('', 18), width=100).grid(
                        column=0, row=0)
                # Se imprimen los resultados
                ttk.Label(frm5, text="Codigo CRC: ", font=('', 18), width=100).grid(
                    column=0, row=1)
                ttk.Label(frm5, text=result[2], font=('', 18)).grid(
                    column=0, row=2)
                # Si no hubo error se imprime el codigo original en bits
                if not result[1]:
                    ttk.Label(frm5, text="Codigo Original: ", font=('', 18), width=100).grid(
                        column=0, row=3)
                    ttk.Label(frm5, text=result[3], font=('', 18)).grid(
                        column=0, row=4)

    # Boton para regresar a la vista principal
    ttk.Button(frm5, text="Regresar", style="MyButton.TButton",
               command=lambda: destroyFrm(0, False)).grid(column=0, row=6)


""" 
Funcion que se muestra cuando ocurre un error en las banderas y no permite determinar la trama a decodificar 
"""


def invalidBands(result: tuple):
    global frm5

    # Se maqueta la quinta vista cuando hay un error de bandera
    frm5 = Frame(frm, padx=10, pady=10)
    frm5.columnconfigure(0, weight=1)
    frm5.columnconfigure(1, weight=1)
    frm5.rowconfigure(0, weight=1)
    frm5.rowconfigure(1, weight=1)
    frm5.grid(sticky="nsew")

    # Label para mostrar un mensaje
    ttk.Label(frm5, text=result[1], font=('', 18)).grid(
        column=0, columnspan=2, row=0)

    # Boton para regresar a la primera vista
    ttk.Button(frm5, text="Regresar", style="MyButton.TButton",
               command=lambda: destroyFrm(0, False)).grid(column=0, columnspan=2, row=1)


# Se llama a la primera funcion que muestra la primera vista
view_one()

# Servicio que mantiene actualizada la vista
window.mainloop()
