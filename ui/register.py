import tkinter as tk
from tkinter import messagebox
import sqlite3
import time

def tela_cadastro(root):
    def cadastrar():
        nome = entry_nome.get()
        email = entry_email.get()
        senha = entry_senha.get()
        tipo = var_tipo.get()

        if not nome or not email or not senha or not tipo:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        for tentativa in range(5):  # tenta até 5 vezes caso o banco esteja travado
            try:
                conn = sqlite3.connect("database/db.sqlite3", timeout=5)
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO usuarios (nome, email, senha, tipo)
                    VALUES (?, ?, ?, ?)
                """, (nome, email, senha, tipo))

                conn.commit()
                conn.close()
                messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
                root.destroy()
                break
            except sqlite3.IntegrityError:
                messagebox.showerror("Erro", "Esse e-mail já está cadastrado.")
                break
            except sqlite3.OperationalError as e:
                if "locked" in str(e):
                    time.sleep(1)  # espera 1 segundo e tenta de novo
                else:
                    messagebox.showerror("Erro", f"Erro no banco de dados: {e}")
                    break

    janela = tk.Toplevel(root)
    janela.title("Cadastro")
    janela.geometry("300x300")

    tk.Label(janela, text="Nome").pack()
    entry_nome = tk.Entry(janela)
    entry_nome.pack()

    tk.Label(janela, text="Email").pack()
    entry_email = tk.Entry(janela)
    entry_email.pack()

    tk.Label(janela, text="Senha").pack()
    entry_senha = tk.Entry(janela, show="*")
    entry_senha.pack()

    tk.Label(janela, text="Tipo").pack()
    var_tipo = tk.StringVar()
    tk.Radiobutton(janela, text="Professor", variable=var_tipo, value="professor").pack()
    tk.Radiobutton(janela, text="Aluno", variable=var_tipo, value="aluno").pack()

    tk.Button(janela, text="Cadastrar", command=cadastrar).pack(pady=10)
