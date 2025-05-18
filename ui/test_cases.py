import tkinter as tk
from tkinter import messagebox
import sqlite3

def gerenciar_test_cases(questao_id):
    jan = tk.Toplevel()
    jan.title(f"Test Cases – Questão {questao_id}")
    jan.geometry("500x400")

    # Lista de casos
    frame = tk.Frame(jan)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    lista = tk.Listbox(frame, width=60)
    lista.pack(side="left", fill="both", expand=True)
    scroll = tk.Scrollbar(frame, command=lista.yview)
    scroll.pack(side="right", fill="y")
    lista.config(yscrollcommand=scroll.set)

    def carregar():
        lista.delete(0, tk.END)
        conn = sqlite3.connect("database/db.sqlite3")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, entrada, saida_esperada
            FROM test_cases
            WHERE questao_id = ?
        """, (questao_id,))
        for cid, ent, sai in cursor.fetchall():
            lista.insert(tk.END, f"{cid} – In: {ent} | Out: {sai}")
        conn.close()

    def adicionar():
        ent = entry_entrada.get().strip()
        sai = entry_saida.get().strip()
        if not ent or not sai:
            messagebox.showerror("Erro", "Preencha entrada e saída.")
            return
        conn = sqlite3.connect("database/db.sqlite3")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO test_cases (questao_id, entrada, saida_esperada)
            VALUES (?, ?, ?)
        """, (questao_id, ent, sai))
        conn.commit()
        conn.close()
        entry_entrada.delete(0, tk.END)
        entry_saida.delete(0, tk.END)
        carregar()

    def remover():
        sel = lista.curselection()
        if not sel:
            messagebox.showerror("Erro", "Selecione um caso.")
            return
        cid = int(lista.get(sel[0]).split(" – ")[0])
        conn = sqlite3.connect("database/db.sqlite3")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM test_cases WHERE id = ?", (cid,))
        conn.commit()
        conn.close()
        carregar()

    carregar()

    tk.Label(jan, text="Nova Entrada:").pack(pady=(5,0))
    entry_entrada = tk.Entry(jan, width=60)
    entry_entrada.pack()
    tk.Label(jan, text="Nova Saída Esperada:").pack(pady=(5,0))
    entry_saida = tk.Entry(jan, width=60)
    entry_saida.pack()
    tk.Button(jan, text="Adicionar Caso", command=adicionar).pack(pady=5)
    tk.Button(jan, text="Remover Selecionado", command=remover).pack(pady=5)
