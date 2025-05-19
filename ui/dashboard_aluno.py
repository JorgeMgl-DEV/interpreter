import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

class ToolTip:
    # Tooltip básico para widgets
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
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
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def dashboard_aluno(usuario):
    janela = tk.Tk()
    janela.title("Dashboard do Aluno - Codegib")
    janela.geometry("650x500")
    janela.configure(bg="#f0f0f0")

    tk.Label(janela, text=f"Olá, {usuario[1]}!", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=15)

    tk.Label(janela, text="Selecione uma questão para resolver:", font=("Arial", 14), bg="#f0f0f0").pack(pady=10)

    frame_lista = tk.Frame(janela)
    frame_lista.pack(pady=5, padx=20, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(frame_lista)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    lista = tk.Listbox(frame_lista, font=("Consolas", 12), yscrollcommand=scrollbar.set, selectmode=tk.SINGLE)
    lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=lista.yview)

    # Carregar questões
    conn = sqlite3.connect("database/db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT id, enunciado FROM questoes ORDER BY id")
    questoes = cursor.fetchall()
    conn.close()

    for q in questoes:
        lista.insert(tk.END, f"{q[0]} - {q[1][:60]}{'...' if len(q[1])>60 else ''}")

    # Instruções adicionais
    instrucao = tk.Label(janela, text="Dica: selecione uma questão e clique no botão abaixo para abrir o editor.",
                        font=("Arial", 11), fg="#555555", bg="#f0f0f0")
    instrucao.pack(pady=10)

    def abrir_questao():
        selecao = lista.curselection()
        if not selecao:
            messagebox.showwarning("Atenção", "Por favor, selecione uma questão antes de continuar.")
            return
        idx = selecao[0]
        questao_id = questoes[idx][0]

        # Importa aqui para evitar ciclo de importações
        from ui.editor import abrir_editor
        abrir_editor(usuario, questao_id)

    btn_abrir = tk.Button(janela, text="Abrir Questão", font=("Arial", 14, "bold"), bg="#4CAF50", fg="white",
                        activebackground="#45a049", activeforeground="white", command=abrir_questao)
    btn_abrir.pack(pady=15, ipadx=15, ipady=7)

    ToolTip(btn_abrir, "Clique para abrir o editor e resolver a questão selecionada")

    # Botão histórico
    def abrir_historico():
        from ui.historico_aluno import tela_historico_aluno
        tela_historico_aluno(usuario)

    btn_hist = tk.Button(janela, text="Ver Histórico de Submissões", font=("Arial", 12),
                        bg="#2196F3", fg="white", activebackground="#1976D2",
                        activeforeground="white", command=abrir_historico)
    btn_hist.pack(pady=5, ipadx=10, ipady=5)
    ToolTip(btn_hist, "Veja todas as suas tentativas anteriores")

    janela.mainloop()
