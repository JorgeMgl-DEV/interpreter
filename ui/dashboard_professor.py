import tkinter as tk
from tkinter import messagebox
import sqlite3
from ui.submissoes_professor import tela_submissoes_professor

def dashboard_professor(usuario):
    janela = tk.Tk()
    janela.title("Dashboard do Professor - Codegib")
    janela.geometry("500x550")

    tk.Label(janela, text=f"Olá, {usuario[1]}!", font=("Arial", 16)).pack(pady=10)
    tk.Label(janela, text="Cadastrar nova questão", font=("Arial", 14)).pack(pady=10)

    tk.Label(janela, text="Enunciado:").pack()
    enunciado_entry = tk.Text(janela, height=5, width=50)
    enunciado_entry.pack()

    tk.Label(janela, text="Entrada de teste:").pack()
    entrada_entry = tk.Entry(janela, width=50)
    entrada_entry.pack()

    tk.Label(janela, text="Saída esperada:").pack()
    saida_entry = tk.Entry(janela, width=50)
    saida_entry.pack()

    def salvar_questao():
        enunciado = enunciado_entry.get("1.0", tk.END).strip()
        entrada = entrada_entry.get()
        saida = saida_entry.get()

        if not enunciado or not entrada or not saida:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return

        conn = sqlite3.connect("database/db.sqlite3")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                enunciado TEXT NOT NULL,
                entrada TEXT NOT NULL,
                saida_esperada TEXT NOT NULL
            )
        """)
        cursor.execute("INSERT INTO questoes (enunciado, entrada, saida_esperada) VALUES (?, ?, ?)",
                    (enunciado, entrada, saida))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Questão cadastrada com sucesso!")

    tk.Button(janela, text="Salvar Questão", command=salvar_questao).pack(pady=20)

    tk.Button(janela, text="Ver Submissões dos Alunos", command=tela_submissoes_professor).pack(pady=10)

    janela.mainloop()
