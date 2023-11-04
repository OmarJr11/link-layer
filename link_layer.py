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
code: bool
hamming: bool
parity: bool


def destroyFrm(num, decision):
    if num == 2:
        frm2.destroy()
        global code
        code = decision
        view_two()
    elif num == 3:
        frm3.destroy()
        global hamming
        hamming = decision
        view_three()
    elif num == 4:
        frm4.destroy()
        global parity
        parity = decision
        view_four()
    elif num == 5:
        print(decision)


def view_one():
    ttk.Label(frm2, text="Quieres codificar o decodificar:").grid(
        column=0, row=0)
    ttk.Button(frm2, text="Codificar",
               command=lambda: destroyFrm(2, True)).grid(column=1, row=0)
    ttk.Button(frm2, text="Decodificar",
               command=lambda: destroyFrm(2, False)).grid(column=2, row=0)


def view_two():
    ttk.Label(frm3, text="Metodo:").grid(column=0, row=1)
    ttk.Button(frm3, text="Hamming", command=lambda: destroyFrm(3, True)).grid(
        column=1, row=1)
    ttk.Button(frm3, text="CRC",
               command=lambda: destroyFrm(3, False)).grid(column=2, row=1)


def view_three():
    ttk.Label(frm4, text="Paridad:").grid(column=0, row=1)
    ttk.Button(frm4, text="Par", command=lambda: destroyFrm(4, True)).grid(
        column=1, row=1)
    ttk.Button(frm4, text="Impar",
               command=lambda: destroyFrm(4, False)).grid(column=2, row=1)


def view_four():
    ttk.Label(frm5, text="Ingrese su codigo:").grid(column=0, row=2)
    entry = ttk.Entry(frm5)
    entry.grid(
        column=1, row=2)
    ttk.Button(frm5, text="Enter",
               command=lambda: destroyFrm(5, entry.get())).grid(column=2, row=2)


view_one()
window.mainloop()

# window.configure(background="")
