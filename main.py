import tkinter as tk
from ui.register import tela_cadastro
from ui.login import tela_login

def iniciar_app():
    root = tk.Tk()
    root.title("Codegib")
    root.geometry("400x300")

    tk.Label(root, text="Bem-vindo ao Codegib!", font=("Arial", 20)).pack(pady=30)

    tk.Button(root, text="Login", width=20, command=lambda: tela_login(root)).pack(pady=10)
    tk.Button(root, text="Cadastro", width=20, command=lambda: tela_cadastro(root)).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    iniciar_app()
