import tkinter as tk
from tkinter import ttk
import sqlite3

def ver_codigo(codigo):
    janela = tk.Toplevel()
    janela.title("Código Enviado")
    janela.geometry("600x400")

    text = tk.Text(janela, wrap="word")
    text.insert("1.0", codigo)
    text.config(state="disabled")
    text.pack(expand=True, fill="both")

def tela_historico_aluno(usuario):
    janela = tk.Toplevel()
    janela.title("Meu Histórico de Submissões")
    janela.geometry("900x400")

    tree = ttk.Treeview(janela, columns=("questao", "resultado", "data", "ver"), show="headings")
    tree.heading("questao", text="Questão")
    tree.heading("resultado", text="Resultado")
    tree.heading("data", text="Data e Hora")
    tree.heading("ver", text="Ver Código")

    tree.column("questao", width=400)
    tree.column("resultado", width=100)
    tree.column("data", width=200)
    tree.column("ver", width=100)

    tree.pack(fill="both", expand=True)

    conn = sqlite3.connect("database/db.sqlite3")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT s.id, q.enunciado, s.resultado, s.data_hora, s.codigo
        FROM submissoes s
        JOIN questoes q ON s.id_questao = q.id
        WHERE s.id_aluno = ?
        ORDER BY s.data_hora DESC
    """, (usuario[0],))
    dados = cursor.fetchall()
    conn.close()

    for sub in dados:
        id_sub, questao, resultado, data_hora, codigo = sub
        tree.insert("", "end", iid=id_sub, values=(questao[:60] + "...", resultado, data_hora, "Ver"))

    def on_double_click(event):
        item = tree.focus()
        if item:
            id_sub = int(item)
            for sub in dados:
                if sub[0] == id_sub:
                    ver_codigo(sub[4])  # código está na posição 4
                    break

    tree.bind("<Double-1>", on_double_click)
