import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def ver_codigo(codigo):
    janela = tk.Toplevel()
    janela.title("Código da Submissão")
    janela.geometry("600x400")

    text = tk.Text(janela, wrap="word")
    text.insert("1.0", codigo)
    text.config(state="disabled")
    text.pack(expand=True, fill="both")

def tela_submissoes_professor():
    janela = tk.Toplevel()
    janela.title("Submissões dos Alunos")
    janela.geometry("900x400")

    tree = ttk.Treeview(janela, columns=("aluno", "questao", "resultado", "data", "ver"), show="headings")
    tree.heading("aluno", text="Aluno")
    tree.heading("questao", text="Questão")
    tree.heading("resultado", text="Resultado")
    tree.heading("data", text="Data e Hora")
    tree.heading("ver", text="Ver Código")

    tree.column("aluno", width=150)
    tree.column("questao", width=300)
    tree.column("resultado", width=100)
    tree.column("data", width=200)
    tree.column("ver", width=100)

    tree.pack(fill="both", expand=True)

    conn = sqlite3.connect("database/db.sqlite3")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT s.id, u.nome, q.enunciado, s.resultado, s.data_hora, s.codigo
        FROM submissoes s
        JOIN usuarios u ON s.id_aluno = u.id
        JOIN questoes q ON s.id_questao = q.id
        ORDER BY s.data_hora DESC
    """)
    dados = cursor.fetchall()
    conn.close()

    for sub in dados:
        id_sub, aluno, questao, resultado, data_hora, codigo = sub
        tree.insert("", "end", iid=id_sub, values=(aluno, questao[:50] + "...", resultado, data_hora, "Ver"))

    def on_double_click(event):
        item = tree.focus()
        if item:
            id_sub = int(item)
            for sub in dados:
                if sub[0] == id_sub:
                    ver_codigo(sub[5])  # código está na posição 5
                    break

    tree.bind("<Double-1>", on_double_click)
