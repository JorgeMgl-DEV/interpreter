import tkinter as tk
from tkinter import messagebox
import sqlite3
from ui.editor import abrir_editor
from ui.historico_aluno import tela_historico_aluno

def dashboard_aluno(usuario):
    janela = tk.Tk()
    janela.title("Dashboard do Aluno - Codegib")
    janela.geometry("600x500")

    tk.Label(janela, text=f"Bem-vindo, {usuario[1]}", font=("Arial", 16)).pack(pady=10)
    tk.Label(janela, text="Selecione uma questão:", font=("Arial", 14)).pack(pady=5)

    frame = tk.Frame(janela)
    frame.pack(pady=10, fill=tk.BOTH, expand=True)

    lista = tk.Listbox(frame, font=("Arial", 12))
    lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)
    lista.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=lista.yview)

    conn = sqlite3.connect("database/db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT id, enunciado FROM questoes")
    questoes = cursor.fetchall()
    conn.close()

    for q in questoes:
        lista.insert(tk.END, f"{q[0]} - {q[1][:50]}...")

    def abrir_questao():
        selecao = lista.curselection()
        if not selecao:
            messagebox.showerror("Erro", "Selecione uma questão.")
            return
        index = selecao[0]
        questao_id = questoes[index][0]
        abrir_editor(usuario, questao_id)

    tk.Button(janela, text="Abrir Questão", command=abrir_questao).pack(pady=10)
    tk.Button(janela, text="Ver Meu Histórico", command=lambda: tela_historico_aluno(usuario)).pack(pady=10)

    janela.mainloop()
