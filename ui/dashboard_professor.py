import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

class ToolTip:
    """Tooltip básico para widgets."""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        if self.tipwindow or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert") if hasattr(self.widget, 'bbox') else (0,0,0,0)
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("Arial", 10))
        label.pack(ipadx=5, ipady=3)

    def hide(self, event=None):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None

def dashboard_professor(usuario):
    janela = tk.Tk()
    janela.title("Dashboard do Professor - Codegib")
    janela.geometry("700x650")
    janela.configure(bg="#f0f0f0")

    # Saudação
    tk.Label(janela, text=f"Olá, {usuario[1]}!", font=("Arial", 18, "bold"), bg="#f0f0f0")\
      .pack(pady=15)

    # Seção de cadastro de questão
    frame_cad = tk.LabelFrame(janela, text="Cadastrar Nova Questão", font=("Arial", 12, "bold"),
                              bg="#f0f0f0", padx=10, pady=10)
    frame_cad.pack(fill="x", padx=20, pady=(0,10))

    tk.Label(frame_cad, text="Enunciado:", font=("Arial", 11), bg="#f0f0f0")\
      .pack(anchor="w")
    enunciado_entry = tk.Text(frame_cad, height=4, font=("Consolas", 11), wrap="word")
    enunciado_entry.pack(fill="x", pady=5)

    def salvar_questao():
        enunciado = enunciado_entry.get("1.0", tk.END).strip()
        if not enunciado:
            messagebox.showwarning("Atenção", "O enunciado não pode ficar vazio.")
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
        messagebox.showinfo("Sucesso", f"Questão {qid} criada com sucesso!")
        enunciado_entry.delete("1.0", tk.END)
        # Abre gerenciador de casos de teste
        from ui.test_cases import gerenciar_test_cases
        gerenciar_test_cases(qid)
        carregar_questoes()

    btn_salvar = tk.Button(frame_cad, text="Salvar Questão", font=("Arial", 11, "bold"),
                           bg="#4CAF50", fg="white", activebackground="#45a049",
                           command=salvar_questao)
    btn_salvar.pack(pady=5, ipadx=10, ipady=5)
    ToolTip(btn_salvar, "Salva o enunciado e adiciona casos de teste")

    # Botões de ação
    frame_btns = tk.Frame(janela, bg="#f0f0f0")
    frame_btns.pack(fill="x", padx=20, pady=(0,10))

    def ver_submissoes():
        from ui.submissoes_professor import tela_submissoes_professor
        tela_submissoes_professor()
    btn_sub = tk.Button(frame_btns, text="Ver Submissões", font=("Arial", 11),
                        bg="#2196F3", fg="white", activebackground="#1976D2",
                        command=ver_submissoes)
    btn_sub.pack(side="left", padx=(0,10), ipadx=10, ipady=5)
    ToolTip(btn_sub, "Veja todas as submissões dos alunos")

    # Lista de questões existentes
    tk.Label(janela, text="Questões Cadastradas:", font=("Arial", 14), bg="#f0f0f0")\
      .pack(anchor="w", padx=20)

    frame_list = tk.Frame(janela, bg="#f0f0f0")
    frame_list.pack(fill="both", expand=True, padx=20, pady=(5,10))

    scrollbar = tk.Scrollbar(frame_list)
    scrollbar.pack(side="right", fill="y")

    listbox = tk.Listbox(frame_list, font=("Consolas", 12), yscrollcommand=scrollbar.set)
    listbox.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=listbox.yview)

    def carregar_questoes():
        listbox.delete(0, tk.END)
        conn = sqlite3.connect("database/db.sqlite3")
        cursor = conn.cursor()
        cursor.execute("SELECT id, enunciado FROM questoes ORDER BY id")
        for qid, enun in cursor.fetchall():
            texto = enun if len(enun) <= 60 else enun[:60] + "..."
            listbox.insert(tk.END, f"{qid} – {texto}")
        conn.close()

    def gerenciar_selecionada():
        sel = listbox.curselection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione uma questão para editar casos de teste.")
            return
        qid = int(listbox.get(sel[0]).split(" – ")[0])
        from ui.test_cases import gerenciar_test_cases
        gerenciar_test_cases(qid)

    btn_gc = tk.Button(janela, text="Gerenciar Test Cases", font=("Arial", 11),
                       bg="#FF9800", fg="white", activebackground="#F57C00",
                       command=gerenciar_selecionada)
    btn_gc.pack(pady=(0,15), ipadx=10, ipady=5)
    ToolTip(btn_gc, "Adicione ou remova casos de teste da questão selecionada")

    carregar_questoes()
    janela.mainloop()
