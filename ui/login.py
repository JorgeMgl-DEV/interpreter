import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

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

def tela_login(root):
    janela = tk.Toplevel(root)
    janela.title("Login – Codegib")
    janela.geometry("400x350")
    janela.configure(bg="#f0f0f0")
    janela.resizable(False, False)

    # Frame de conteúdo
    frm = ttk.Frame(janela, padding=20)
    frm.pack(fill="both", expand=True)

    ttk.Label(frm, text="Faça seu login", font=("Arial", 16, "bold")).pack(pady=(0,15))

    # Email
    lbl_email = ttk.Label(frm, text="Email:", font=("Arial", 11))
    lbl_email.pack(anchor="w", pady=(5,0))
    ent_email = ttk.Entry(frm, font=("Arial", 11))
    ent_email.pack(fill="x", pady=(0,10))
    ToolTip(ent_email, "Digite seu email cadastrado")

    # Senha
    lbl_senha = ttk.Label(frm, text="Senha:", font=("Arial", 11))
    lbl_senha.pack(anchor="w", pady=(5,0))
    ent_senha = ttk.Entry(frm, font=("Arial", 11), show="*")
    ent_senha.pack(fill="x", pady=(0,20))
    ToolTip(ent_senha, "Digite sua senha secreta")

    # Botões
    btn_frame = ttk.Frame(frm)
    btn_frame.pack(fill="x", pady=(0,10))
    btn_login = ttk.Button(btn_frame, text="Entrar", command=lambda: login())
    btn_login.pack(side="left", expand=True)
    ToolTip(btn_login, "Clique para entrar no sistema")

    btn_cad = ttk.Button(btn_frame, text="Cadastrar", command=lambda: from_register())
    btn_cad.pack(side="left", expand=True, padx=(10,0))
    ToolTip(btn_cad, "Ainda não tem conta? Cadastre-se")

    def login():
        email = ent_email.get().strip()
        senha = ent_senha.get().strip()
        if not email or not senha:
            messagebox.showwarning("Atenção", "Preencha email e senha.")
            return

        conn = sqlite3.connect("database/db.sqlite3")
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuarios WHERE email=? AND senha=?", (email, senha))
        user = cur.fetchone()
        conn.close()

        if not user:
            messagebox.showerror("Erro", "Email ou senha inválidos.")
            return

        messagebox.showinfo("Sucesso", f"Bem-vindo, {user[1]}!")
        janela.destroy()
        if user[4] == "professor":
            from ui.dashboard_professor import dashboard_professor
            dashboard_professor(user)
        else:
            from ui.dashboard_aluno import dashboard_aluno
            dashboard_aluno(user)

    def from_register():
        from ui.register import tela_cadastro
        tela_cadastro(root)
        janela.destroy()
