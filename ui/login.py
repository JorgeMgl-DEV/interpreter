import tkinter as tk
from tkinter import messagebox
import sqlite3
from ui.dashboard_professor import dashboard_professor
from ui.dashboard_aluno import dashboard_aluno

def tela_login(root):
    def login():
        email = entry_email.get()
        senha = entry_senha.get()

        conn = sqlite3.connect("database/db.sqlite3")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
        usuario = cursor.fetchone()
        conn.close()

        if usuario:
            messagebox.showinfo("Sucesso", f"Bem-vindo, {usuario[1]} ({usuario[4]})")
            root.destroy()

            if usuario[4] == "professor":
                dashboard_professor(usuario)
            else:
                dashboard_aluno(usuario)
        else:
            messagebox.showerror("Erro", "Email ou senha inválidos.")

    janela = tk.Toplevel(root)
    janela.title("Login")
    janela.geometry("300x200")

    tk.Label(janela, text="Email").pack()
    entry_email = tk.Entry(janela)
    entry_email.pack()

    tk.Label(janela, text="Senha").pack()
    entry_senha = tk.Entry(janela, show="*")
    entry_senha.pack()

    tk.Button(janela, text="Entrar", command=login).pack(pady=10)
