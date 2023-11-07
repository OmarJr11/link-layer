from modules.module import CodeHamming, DecodeHamming, DecodeCRC, CodeCRC, es_binario
from tkinter import *
from tkinter import ttk

window = Tk()
window.title('Capa de enlace')
window.geometry('800x600')
window.columnconfigure(0, weight=1)
frm = Frame(window, padx=20, pady=20, background='#353b48',)
frm.columnconfigure(0, weight=1)
frm.rowconfigure(0, weight=1)

frm.grid(sticky="nsew")
frm.pack(fill='both', expand=True, side='top')

frm1: Frame
frm2: Frame
frm3: Frame
frm4: Frame
frm5: Frame

mode: bool
hamming: bool
parity: bool
code: str
generator: str
sentFrame: str = ''

styles = ttk.Style()
styles.configure(
    "MyButton.TButton",
    foreground="#353b48",
    padding=10,
    font=('', 14),
    cursor='pointer'
)


def destroyFrm(num, data):
    if num == 1:
        frm1.destroy()
        global mode
        mode = data
        view_two(False)
    elif num == 2:
        frm2.destroy()
        global code
        code = data
        if mode:
            if es_binario(code) and len(code) <= 24:
                view_three()
            else:
                view_two(True)
        else:
            view_three()
    elif num == 3:
        frm3.destroy()
        global hamming
        hamming = data
        view_four(False)
    elif num == 4:
        frm4.destroy()
        global parity
        parity = data

        if mode:
            result: tuple = CodeHamming(code, parity)
            if result[0]:
                hamming_result_view(result, True)
        else:
            result: tuple = DecodeHamming(code, parity)
            if result[0]:
                hamming_result_view(result, False)
            else:
                invalidBands(result)
    elif num == 5:
        frm4.destroy()
        global generator
        generator = data

        if es_binario(generator) and len(generator) <= 5:
            if mode:
                result: tuple = CodeCRC(code, generator)
                if result[0]:
                    hamming_result_view(result, True)
            else:
                result: tuple = DecodeCRC(code, generator)
                if result[0]:
                    hamming_result_view(result, False)
                else:
                    invalidBands(result)
        else:
            view_four(True)
    else:
        frm5.destroy()
        view_one()


def resetFrm(num):
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


def view_one():
    global frm1

    frm1 = Frame(frm, padx=10, pady=10, )
    frm1.columnconfigure(0, weight=1)
    frm1.columnconfigure(1, weight=1)
    frm1.rowconfigure(0, weight=1)
    frm1.rowconfigure(1, weight=1)
    frm1.grid(sticky="nsew")

    ttk.Label(frm1, text="Desea codificar o decodificar una trama:", font=('', 18)).grid(
        column=0, columnspan=2, row=0,)

    ttk.Button(frm1, text="Codificar",
               command=lambda: destroyFrm(1, True), style="MyButton.TButton").grid(column=0, row=1,)
    ttk.Button(frm1, text="Decodificar",
               command=lambda: destroyFrm(1, False), style="MyButton.TButton").grid(column=1, row=1, )


def view_two(error):
    global frm2

    frm2 = Frame(frm, padx=10, pady=10)
    frm2.columnconfigure(0, weight=1)
    frm2.columnconfigure(1, weight=1)
    frm2.rowconfigure(0, weight=1)
    frm2.rowconfigure(1, weight=1)
    if not mode:
        frm2.rowconfigure(2, weight=1)

    frm2.grid(sticky="nsew")

    if not error:
        ttk.Label(frm2, text="Ingrese el codigo (en bits):", font=('', 18)).grid(
            column=0, columnspan=2, row=0)
    else:
        ttk.Label(frm2, text="Ingrese un codigo valido (en bits):", font=('', 18)).grid(
            column=0, columnspan=2, row=0)
    entry = ttk.Entry(frm2, width=40, font=('', 14),)
    entry.grid(
        column=0, row=1, ipadx=5, ipady=5)
    ttk.Button(frm2, text="Enter", style="MyButton.TButton",
               command=lambda: destroyFrm(2, entry.get())).grid(column=1, row=1)
    if not mode:
        ttk.Button(frm2, text="Regresar", style="MyButton.TButton",
                   command=lambda: resetFrm(2)).grid(column=0, row=2)
        ttk.Button(frm2, text="Codigo Anterior", style="MyButton.TButton",
                   command=lambda: entry.insert(0, sentFrame)).grid(column=1, row=2)
    else:
        ttk.Button(frm2, text="Regresar", style="MyButton.TButton",
                   command=lambda: resetFrm(2)).grid(column=0, row=3, columnspan=2)


def view_three():
    global frm3

    frm3 = Frame(frm, padx=10, pady=10)
    frm3.columnconfigure(0, weight=1)
    frm3.columnconfigure(1, weight=1)
    frm3.rowconfigure(0, weight=1)
    frm3.rowconfigure(1, weight=1)
    frm3.grid(sticky="nsew")

    ttk.Label(frm3, text="Metodo a utilizar:", font=('', 18)).grid(
        column=0, columnspan=2, row=0)
    ttk.Button(frm3, text="Hamming", style="MyButton.TButton", command=lambda: destroyFrm(3, True)).grid(
        column=0, row=1)
    ttk.Button(frm3, text="CRC", style="MyButton.TButton",
               command=lambda: destroyFrm(3, False)).grid(column=1, row=1)
    ttk.Button(frm3, text="Regresar", style="MyButton.TButton",
               command=lambda: resetFrm(3)).grid(column=0, row=3, columnspan=2)


def view_four(error):
    global frm4
    global hamming

    frm4 = Frame(frm, padx=10, pady=10)
    frm4.columnconfigure(0, weight=1)
    frm4.columnconfigure(1, weight=1)
    frm4.rowconfigure(0, weight=1)
    frm4.rowconfigure(1, weight=1)
    frm4.rowconfigure(0, weight=1)
    frm4.grid(sticky="nsew")

    if hamming:
        ttk.Label(frm4, text="Paridad a utilizar:", font=('', 18)).grid(
            column=0, columnspan=2, row=0)
        ttk.Button(frm4, text="Par", style="MyButton.TButton", command=lambda: destroyFrm(4, True)).grid(
            column=0, row=1)
        ttk.Button(frm4, text="Impar", style="MyButton.TButton",
                   command=lambda: destroyFrm(4, False)).grid(column=1, row=1)
    else:
        if not error:
            ttk.Label(frm4, text="Ingrese el polinomio generador (en bits, maximo 5 bits):", font=('', 18)).grid(
                column=0, columnspan=2, row=0)
        else:
            ttk.Label(frm4, text="Ingrese un polinomio generador valido (en bits, maximo 5 bits):", font=('', 18)).grid(
                column=0, columnspan=2, row=0)
        entry = ttk.Entry(frm4, width=40, font=('', 14),)
        entry.grid(
            column=0, row=1, ipadx=5, ipady=5)
        ttk.Button(frm4, text="Enter", style="MyButton.TButton",
                   command=lambda: destroyFrm(5, entry.get())).grid(column=1, row=1)
    ttk.Button(frm4, text="Regresar", style="MyButton.TButton",
               command=lambda: resetFrm(4)).grid(column=0, row=3, columnspan=2)


def hamming_result_view(result: tuple, isCode: bool):
    global frm5
    global sentFrame

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

    if result[0]:
        if isCode:
            if hamming:
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
        else:
            if hamming:
                if result[1] > 0:
                    ttk.Label(frm5, text="Error en la posicion: ", font=('', 18), width=100).grid(
                        column=0, row=0)
                    ttk.Label(frm5, text=result[1], font=('', 18)).grid(
                        column=0, row=1)
                else:
                    ttk.Label(frm5, text="No hay error", font=('', 18), width=100).grid(
                        column=0, row=0)
                ttk.Label(frm5, text="Codigo Hamming: ", font=('', 18), width=100).grid(
                    column=0, row=2)
                ttk.Label(frm5, text=result[2], font=('', 18)).grid(
                    column=0, row=3)
                ttk.Label(frm5, text="Codigo Hamming decodificado: ", font=('', 18), width=100).grid(
                    column=0, row=4)
                ttk.Label(frm5, text=result[3], font=('', 18)).grid(
                    column=0, row=5)
            else:
                if result[1]:
                    ttk.Label(frm5, text="Hubo un error en la transmicion", font=('', 18), width=100).grid(
                        column=0, row=0)
                else:
                    ttk.Label(frm5, text="Trama recibida correctamente", font=('', 18), width=100).grid(
                        column=0, row=0)
                ttk.Label(frm5, text="Codigo CRC: ", font=('', 18), width=100).grid(
                    column=0, row=1)
                ttk.Label(frm5, text=result[2], font=('', 18)).grid(
                    column=0, row=2)
                if not result[1]:
                    ttk.Label(frm5, text="Codigo Original: ", font=('', 18), width=100).grid(
                        column=0, row=3)
                    ttk.Label(frm5, text=result[3], font=('', 18)).grid(
                        column=0, row=4)

    ttk.Button(frm5, text="Regresar", style="MyButton.TButton",
               command=lambda: destroyFrm(0, False)).grid(column=0, row=6)


def invalidBands(result: tuple):
    global frm5

    frm5 = Frame(frm, padx=10, pady=10)
    frm5.columnconfigure(0, weight=1)
    frm5.columnconfigure(1, weight=1)
    frm5.rowconfigure(0, weight=1)
    frm5.rowconfigure(1, weight=1)

    frm5.grid(sticky="nsew")
    ttk.Label(frm5, text=result[1], font=('', 18)).grid(
        column=0, columnspan=2, row=0)
    ttk.Button(frm5, text="Regresar", style="MyButton.TButton",
               command=lambda: destroyFrm(0, False)).grid(column=0, columnspan=2, row=1)


view_one()
window.mainloop()

# window.configure(background="")
