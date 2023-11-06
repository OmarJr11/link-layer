from modules.module import CodeHamming, DecodeHamming, DecodeCRC, CodeCRC
from tkinter import *
from tkinter import ttk

window = Tk()
window.title('Capa de enlace')
window.geometry('800x600')
frm = Frame(window, padx=10, pady=10)
frm.grid()
frm1 = Frame(frm, padx=10, pady=10)
frm1.grid()
frm2 = Frame(frm, padx=10, pady=10)
frm2.grid()
frm3 = Frame(frm, padx=10, pady=10)
frm3.grid()
frm4 = Frame(frm, padx=10, pady=10)
frm4.grid()
frm5 = Frame(frm, padx=10, pady=10)
frm5.grid()
mode: bool
hamming: bool
parity: bool
reopen: bool = False
code: str
generator: str


def destroyFrm(num, data):
    global reopen
    if num == 1:
        frm1.destroy()
        global mode
        mode = data
        view_two(reopen)
    elif num == 2:
        frm2.destroy()
        global code
        code = data
        view_three(reopen)
    elif num == 3:
        frm3.destroy()
        global hamming
        hamming = data
        view_four(reopen)
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
    elif num == 5:
        frm4.destroy()
        global generator
        generator = data

        if mode:
            result: tuple = CodeCRC(code, generator, hamming)
            if result[0]:
                hamming_result_view(result, True)
        else:
            result: tuple = DecodeCRC(code, generator, hamming)
            if result[0]:
                hamming_result_view(result, False)
    else:
        frm5.destroy()
        reopen = True
        view_one(reopen)


def view_one(reopen: bool):
    global frm1
    if reopen:
        frm1 = Frame(frm, padx=10, pady=10)
        frm1.grid()
    ttk.Label(frm1, text="Quieres codificar o decodificar:").grid(
        column=0, row=0)
    ttk.Button(frm1, text="Codificar",
               command=lambda: destroyFrm(1, True)).grid(column=1, row=0)
    ttk.Button(frm1, text="Decodificar",
               command=lambda: destroyFrm(1, False)).grid(column=2, row=0)


def view_two(reopen: bool):
    global frm2
    if reopen:
        frm2 = Frame(frm, padx=10, pady=10)
        frm2.grid()
    ttk.Label(frm2, text="Ingrese su codigo:").grid(column=0, row=1)
    entry = ttk.Entry(frm2)
    entry.grid(
        column=1, row=2)
    ttk.Button(frm2, text="Enter",
               command=lambda: destroyFrm(2, entry.get())).grid(column=2, row=2)


def view_three(reopen: bool):
    global frm3
    if reopen:
        frm3 = Frame(frm, padx=10, pady=10)
        frm3.grid()
    ttk.Label(frm3, text="Metodo:").grid(column=0, row=1)
    ttk.Button(frm3, text="Hamming", command=lambda: destroyFrm(3, True)).grid(
        column=1, row=1)
    ttk.Button(frm3, text="CRC",
               command=lambda: destroyFrm(3, False)).grid(column=2, row=1)


def view_four(reopen: bool):
    global frm4
    global hamming
    if reopen:
        frm4 = Frame(frm, padx=10, pady=10)
        frm4.grid()

    if hamming:
        ttk.Label(frm4, text="Paridad:").grid(column=0, row=1)
        ttk.Button(frm4, text="Par", command=lambda: destroyFrm(4, True)).grid(
            column=1, row=1)
        ttk.Button(frm4, text="Impar",
                   command=lambda: destroyFrm(4, False)).grid(column=2, row=1)
    else:
        ttk.Label(frm4, text="Ingrese el polinomio generador(en bits):").grid(
            column=0, row=1)
        entry = ttk.Entry(frm4)
        entry.grid(
            column=1, row=2)
        ttk.Button(frm4, text="Enter",
                   command=lambda: destroyFrm(4, entry.get())).grid(column=2, row=2)


def hamming_result_view(result: tuple, isCode: bool):
    global frm5
    if reopen:
        frm5 = Frame(frm, padx=10, pady=10)
        frm5.grid()
    if result[0]:
        if isCode:
            if hamming:
                ttk.Label(frm5, text="Codigo Hamming: ").grid(
                    column=0, row=0)
                ttk.Label(frm5, text=result[1]).grid(
                    column=1, row=0)
                ttk.Label(frm5, text="Codigo Hamming con relleno de bit: ").grid(
                    column=0, row=1)
                ttk.Label(frm5, text=result[2]).grid(
                    column=1, row=1)
                ttk.Label(frm5, text="Codigo Hamming con bits bandera: ").grid(
                    column=0, row=2)
                ttk.Label(frm5, text=result[3]).grid(
                    column=1, row=2)
            else:
                ttk.Label(frm5, text="Codigo CRC: ").grid(
                    column=0, row=0)
                ttk.Label(frm5, text=result[1]).grid(
                    column=1, row=0)
                ttk.Label(frm5, text="Codigo CRC con relleno de bit: ").grid(
                    column=0, row=1)
                ttk.Label(frm5, text=result[2]).grid(
                    column=1, row=1)
                ttk.Label(frm5, text="Codigo CRC con bits bandera: ").grid(
                    column=0, row=2)
                ttk.Label(frm5, text=result[3]).grid(
                    column=1, row=2)
        else:
            if hamming:
                if result[1] > 0:
                    ttk.Label(frm5, text="Error en la posicion: ").grid(
                        column=0, row=0)
                    ttk.Label(frm5, text=result[1]).grid(
                        column=1, row=0)
                else:
                    ttk.Label(frm5, text="No hay error").grid(
                        column=0, row=0)
                ttk.Label(frm5, text="Codigo Hamming: ").grid(
                    column=0, row=1)
                ttk.Label(frm5, text=result[2]).grid(
                    column=1, row=1)
                ttk.Label(frm5, text="Codigo Hamming decodificado: ").grid(
                    column=0, row=2)
                ttk.Label(frm5, text=result[3]).grid(
                    column=1, row=2)
            else:
                if result[1]:
                    ttk.Label(frm5, text="Hubo un error en la transmicion ").grid(
                        column=0, row=0)
                else:
                    ttk.Label(frm5, text="No hay error").grid(
                        column=0, row=0)
                ttk.Label(frm5, text="Codigo CRC: ").grid(
                    column=0, row=1)
                ttk.Label(frm5, text=result[2]).grid(
                    column=1, row=1)
        print(result)
    else:
        ttk.Label(frm5, text=result[1]).grid(
            column=0, row=0)
    ttk.Button(frm5, text="Regresar",
               command=lambda: destroyFrm(0, False)).grid(column=1, row=3)


view_one(reopen)
window.mainloop()

# window.configure(background="")
