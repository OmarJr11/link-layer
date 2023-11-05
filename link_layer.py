from modules.module import CodeHamming, DecodeHamming
from tkinter import *
from tkinter import ttk

window = Tk()
window.title('Capa de enlace')
window.geometry('800x600')
frm = Frame(window, padx=10, pady=10)
frm.grid()
frm2 = Frame(frm, padx=10, pady=10)
frm2.grid()
frm3 = Frame(frm, padx=10, pady=10)
frm3.grid()
frm4 = Frame(frm, padx=10, pady=10)
frm4.grid()
frm5 = Frame(frm, padx=10, pady=10)
frm5.grid()
frm6 = Frame(frm, padx=10, pady=10)
frm6.grid()
code: bool
hamming: bool
parity: bool
reopen: bool = False


def destroyFrm(num, decision):
    global reopen
    if num == 2:
        frm2.destroy()
        global code
        code = decision
        view_two(reopen)
    elif num == 3:
        frm3.destroy()
        global hamming
        hamming = decision
        view_three(reopen)
    elif num == 4:
        frm4.destroy()
        global parity
        parity = decision
        view_four(reopen)
    elif num == 5:
        frm5.destroy()
        if code:
            result: tuple = CodeHamming(decision, parity)
            if result[0]:
                hamming_result_view(result, True)
        else:
            result: tuple = DecodeHamming(decision, parity)
            if result[0]:
                hamming_result_view(result, False)
    else:
        frm6.destroy()
        reopen = True
        view_one(reopen)


def view_one(reopen: bool):
    global frm2
    if reopen:
        frm2 = Frame(frm, padx=10, pady=10)
        frm2.grid()
    ttk.Label(frm2, text="Quieres codificar o decodificar:").grid(
        column=0, row=0)
    ttk.Button(frm2, text="Codificar",
               command=lambda: destroyFrm(2, True)).grid(column=1, row=0)
    ttk.Button(frm2, text="Decodificar",
               command=lambda: destroyFrm(2, False)).grid(column=2, row=0)


def view_two(reopen: bool):
    global frm3
    if reopen:
        frm3 = Frame(frm, padx=10, pady=10)
        frm3.grid()
    ttk.Label(frm3, text="Metodo:").grid(column=0, row=1)
    ttk.Button(frm3, text="Hamming", command=lambda: destroyFrm(3, True)).grid(
        column=1, row=1)
    ttk.Button(frm3, text="CRC",
               command=lambda: destroyFrm(3, False)).grid(column=2, row=1)


def view_three(reopen: bool):
    global frm4
    if reopen:
        frm4 = Frame(frm, padx=10, pady=10)
        frm4.grid()
    ttk.Label(frm4, text="Paridad:").grid(column=0, row=1)
    ttk.Button(frm4, text="Par", command=lambda: destroyFrm(4, True)).grid(
        column=1, row=1)
    ttk.Button(frm4, text="Impar",
               command=lambda: destroyFrm(4, False)).grid(column=2, row=1)


def view_four(reopen: bool):
    global frm5
    if reopen:
        frm5 = Frame(frm, padx=10, pady=10)
        frm5.grid()
    ttk.Label(frm5, text="Ingrese su codigo:").grid(column=0, row=2)
    entry = ttk.Entry(frm5)
    entry.grid(
        column=1, row=2)
    ttk.Button(frm5, text="Enter",
               command=lambda: destroyFrm(5, entry.get())).grid(column=2, row=2)


def hamming_result_view(result: tuple, isCode: bool):
    global frm6
    if reopen:
        frm6 = Frame(frm, padx=10, pady=10)
        frm6.grid()
    if result[0]:
        if isCode:
            ttk.Label(frm6, text="Codigo Hamming: ").grid(
                column=0, row=0)
            ttk.Label(frm6, text=result[1]).grid(
                column=1, row=0)
            ttk.Label(frm6, text="Codigo Hamming con relleno de bit: ").grid(
                column=0, row=1)
            ttk.Label(frm6, text=result[2]).grid(
                column=1, row=1)
            ttk.Label(frm6, text="Codigo Hamming con bits bandera: ").grid(
                column=0, row=2)
            ttk.Label(frm6, text=result[3]).grid(
                column=1, row=2)
        else:
            if result[1] > 0:
                ttk.Label(frm6, text="Error en la posicion: ").grid(
                    column=0, row=0)
                ttk.Label(frm6, text=result[1]).grid(
                    column=1, row=0)
            else:
                ttk.Label(frm6, text="No hay error").grid(
                    column=0, row=0)
            ttk.Label(frm6, text="Codigo Hamming: ").grid(
                column=0, row=1)
            ttk.Label(frm6, text=result[2]).grid(
                column=1, row=1)
            ttk.Label(frm6, text="Codigo Hamming decodificado: ").grid(
                column=0, row=2)
            ttk.Label(frm6, text=result[3]).grid(
                column=1, row=2)
    else:
        ttk.Label(frm6, text=result[1]).grid(
            column=0, row=0)
    ttk.Button(frm6, text="Regresar",
               command=lambda: destroyFrm(0, False)).grid(column=1, row=3)


view_one(reopen)
window.mainloop()

# window.configure(background="")
