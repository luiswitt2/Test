import tkinter
from tkinter import messagebox

import customtkinter as ck

ck.set_appearance_mode("Dark")
ck.set_default_color_theme("blue")

class MyGUI:

    def __init__(self, master):
        self.master = master

        master.geometry('400x300')
        self.label = ck.CTkLabel(master, text="FaceRecon", font=('Arial', 20))
        self.label.pack(padx=20, pady=25)

        self.btnIniciar = ck.CTkButton(master, text="Iniciar", font=('Arial', 16))
        self.btnIniciar.pack(padx=20, pady=25)

        self.btnConfiguracoes = ck.CTkButton(master, text="Configurações", font=('Arial', 16), command=self.openConfigs)
        self.btnConfiguracoes.pack(padx=20, pady=0)

        master.protocol("WM_DELETE_WINDOW", self.on_closing)


    def openConfigs(self):
        self.newWindow = ck.CTkToplevel(self.master)
        self.app = PagCofigs(self.newWindow)
        self.newWindow.grab_set()

    def show_message(self):
        pass

    def on_closing(self):
        if messagebox.askyesno(title="Sair?", message="Tem certeza que deseja sair?"):
            self.master.destroy()



class PagCofigs:

    def __init__(self, master):
        self.master = master
        master.title("Configurações")
        master.geometry("600x400")
        master.protocol("WM_DELETE_WINDOW", self.on_closing)
        lblTitulo = ck.CTkLabel(master, font=('Arial', 20), text='Configurações')
        lblTitulo.pack()
        lblEntrada = ck.CTkLabel(master, font=('Arial', 16), text='Horario de entrada:', padx=5)
        lblEntrada.place(x=5, y=45)
        txtEntrada = ck.CTkTextbox(master, width=100, height=10, fg_color='grey')
        txtEntrada.place(x=150, y=45)

        lblSaida = ck.CTkLabel(master, font=('Arial', 16), text='Horario de saída:', padx=5)
        lblSaida.place(x=300, y=45)
        txtSaida = ck.CTkTextbox(master, width=100, height=10, fg_color='grey')
        txtSaida.place(x=430, y=45)
    def on_closing(self):
        if messagebox.askyesno(title="Sair?", message="Tem certeza que deseja sair?"):
            self.master.destroy()


root = ck.CTk()
app = MyGUI(root)
root.mainloop()

'''
O que configurar

Hora de entrada/saida
Tolerancia de entrada
modo de segurança(senha de admin ou não)
alterar senha

'''