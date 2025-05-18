import tkinter as tk
from tkinter import messagebox
import sqlite3
from ui.submissoes_professor import tela_submissoes_professor
from ui.test_cases import gerenciar_test_cases

def dashboard_professor(usuario):
    janela = tk.Tk()
    janela.title("Dashboard do Professor – Codegib")
    janela.geometry("600x600")

    tk.Label(janela, text=f"Olá, {usuario[1]}!", font=("Arial", 16)).pack(pady=10)

    # Salvar questão (apenas enunciado agora)
    tk.Label(janela, text="Cadastrar nova questão", font=("Arial", 14)).pack(pady=(10,0))
    tk.Label(janela, text="Enunciado:").pack()
    enunciado_entry = tk.Text(janela, height=5, width=60)
    enunciado_entry.pack()

    def salvar_questao():
        enunciado = enunciado_entry.get("1.0", tk.END).strip()
        if not enunciado:
            messagebox.showerror("Erro", "Enunciado vazio.")
            return
        conn = sqlite3.connect("database/db.sqlite3")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS questoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                enunciado TEXT NOT NULL
            )
        """)
        cursor.execute("INSERT INTO questoes (enunciado) VALUES (?)", (enunciado,))
        conn.commit()
        qid = cursor.lastrowid
        conn.close()
        messagebox.showinfo("Sucesso", f"Questão {qid} criada.")
        gerenciar_test_cases(qid)

    tk.Button(janela, text="Salvar Questão", command=salvar_questao).pack(pady=10)

    # Botão ver submissões
    tk.Button(janela, text="Ver Submissões", command=tela_submissoes_professor).pack(pady=10)

    # Gerenciar test cases de questões existentes
    tk.Label(janela, text="Gerenciar casos de teste:", font=("Arial", 14)).pack(pady=(20,0))
    frame = tk.Frame(janela)
    frame.pack(pady=5, fill="both", expand=False)
    listbox = tk.Listbox(frame, width=60)
    listbox.pack(side="left", fill="y")
    scroll = tk.Scrollbar(frame, command=listbox.yview)
    scroll.pack(side="right", fill="y")
    listbox.config(yscrollcommand=scroll.set)

    def carregar_questoes():
        listbox.delete(0, tk.END)
        conn = sqlite3.connect("database/db.sqlite3")
        cursor = conn.cursor()
        cursor.execute("SELECT id, enunciado FROM questoes")
        for qid, enun in cursor.fetchall():
            listbox.insert(tk.END, f"{qid} – {enun[:50]}...")
        conn.close()

    def selecionar_e_gerenciar():
        sel = listbox.curselection()
        if not sel:
            messagebox.showerror("Erro", "Selecione uma questão.")
            return
        qid = int(listbox.get(sel[0]).split(" – ")[0])
        gerenciar_test_cases(qid)

    carregar_questoes()
    tk.Button(janela, text="Gerenciar Test Cases", command=selecionar_e_gerenciar).pack(pady=5)

    janela.mainloop()
