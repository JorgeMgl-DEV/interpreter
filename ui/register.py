import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import time

class ToolTip:
    """Tooltip simples para widgets."""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, _event=None):
        if self.tip or not self.text:
            return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 10
        self.tip = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        lbl = tk.Label(tw, text=self.text, background="#ffffe0",
                       relief="solid", borderwidth=1, font=("Arial", 10))
        lbl.pack(ipadx=5, ipady=3)

    def hide(self, _event=None):
        if self.tip:
            self.tip.destroy()
            self.tip = None

def tela_cadastro(root):
    janela = tk.Toplevel(root)
    janela.title("Cadastro – Codegib")
    janela.geometry("400x450")
    janela.configure(bg="#f0f0f0")
    janela.resizable(False, False)

    frm = ttk.Frame(janela, padding=20)
    frm.pack(fill="both", expand=True)

    ttk.Label(frm, text="Crie sua conta", font=("Arial", 16, "bold")).pack(pady=(0,15))

    # Nome
    ttk.Label(frm, text="Nome Completo:", font=("Arial", 11)).pack(anchor="w", pady=(5,0))
    ent_nome = ttk.Entry(frm, font=("Arial", 11))
    ent_nome.pack(fill="x", pady=(0,10))
    ToolTip(ent_nome, "Digite seu nome completo")

    # Email
    ttk.Label(frm, text="Email:", font=("Arial", 11)).pack(anchor="w", pady=(5,0))
    ent_email = ttk.Entry(frm, font=("Arial", 11))
    ent_email.pack(fill="x", pady=(0,10))
    ToolTip(ent_email, "Escolha um email válido")

    # Senha
    ttk.Label(frm, text="Senha:", font=("Arial", 11)).pack(anchor="w", pady=(5,0))
    ent_senha = ttk.Entry(frm, font=("Arial", 11), show="*")
    ent_senha.pack(fill="x", pady=(0,10))
    ToolTip(ent_senha, "Use pelo menos 6 caracteres")

    # Tipo
    ttk.Label(frm, text="Você é:", font=("Arial", 11)).pack(anchor="w", pady=(5,0))
    tipo = tk.StringVar()
    r1 = ttk.Radiobutton(frm, text="Professor", variable=tipo, value="professor")
    r2 = ttk.Radiobutton(frm, text="Aluno", variable=tipo, value="aluno")
    r1.pack(anchor="w")
    r2.pack(anchor="w")
    ToolTip(r1, "Selecione se você for professor")
    ToolTip(r2, "Selecione se você for aluno")

    # Botão cadastrar
    btn = ttk.Button(frm, text="Cadastrar", command=lambda: cadastrar())
    btn.pack(pady=(20,0), ipadx=10, ipady=5)
    ToolTip(btn, "Clique para criar sua conta")

    def cadastrar():
        nome = ent_nome.get().strip()
        email = ent_email.get().strip()
        senha = ent_senha.get().strip()
        tp = tipo.get()

        if not nome or not email or not senha or not tp:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return

        for _ in range(3):
            try:
                conn = sqlite3.connect("database/db.sqlite3", timeout=5)
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO usuarios (nome, email, senha, tipo)
                    VALUES (?, ?, ?, ?)
                """, (nome, email, senha, tp))
                conn.commit()
                conn.close()
                messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
                janela.destroy()
                return
            except sqlite3.IntegrityError:
                messagebox.showerror("Erro", "Este email já está cadastrado.")
                return
            except sqlite3.OperationalError as e:
                if "locked" in str(e):
                    time.sleep(1)
                else:
                    messagebox.showerror("Erro", f"Erro no banco: {e}")
                    return

    # Botão voltar ao login
    def voltar_login():
        from ui.login import tela_login
        tela_login(root)
        janela.destroy()

    btn_voltar = ttk.Button(frm, text="Voltar ao Login", command=voltar_login)
    btn_voltar.pack(pady=(10,0))
    ToolTip(btn_voltar, "Já tem conta? Volte ao login")

