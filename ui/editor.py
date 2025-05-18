import tkinter as tk
from tkinter import messagebox
import sqlite3
import io
import sys
from datetime import datetime
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.styles import get_style_by_name

# Palavras-chave básicas do Python para autocomplete
PYTHON_KEYWORDS = [
    'print', 'input', 'if', 'else', 'elif', 'for', 'while',
    'def', 'return', 'in', 'range', 'int', 'str', 'float',
    'list', 'len', 'break', 'continue', 'True', 'False',
    'import', 'from', 'as', 'class', 'try', 'except', 'with', 'open'
]

def abrir_editor(usuario, questao_id):
    janela = tk.Toplevel()
    janela.title(f"Editor - Questão {questao_id}")
    janela.geometry("950x700")
    janela.configure(bg="#282a36")
    fullscreen = [False]

    # Alternar modo tela cheia
    def toggle_fullscreen(event=None):
        fullscreen[0] = not fullscreen[0]
        janela.attributes("-fullscreen", fullscreen[0])

    janela.bind("<F11>", toggle_fullscreen)

    # Obter a questão
    conn = sqlite3.connect("database/db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT enunciado, entrada, saida_esperada FROM questoes WHERE id = ?", (questao_id,))
    questao = cursor.fetchone()
    conn.close()

    enunciado, entrada, saida_esperada = questao

    tk.Label(janela, text="Enunciado:", font=("Arial", 14), bg="#282a36", fg="#f8f8f2").pack()
    tk.Message(janela, text=enunciado, width=900, bg="#282a36", fg="#f8f8f2").pack(pady=5)

    container = tk.Frame(janela)
    container.pack(fill="both", expand=True)

    numeros_linha = tk.Text(container, width=4, padx=4, takefocus=0, border=0,
                            background="#282a36", foreground="#6272a4", state="disabled")
    numeros_linha.pack(side="left", fill="y")

    editor = tk.Text(container, height=20, width=100, font=("Consolas", 12), bg="#282a36", fg="#f8f8f2",
                     insertbackground="white", undo=True, wrap="none")
    editor.pack(side="left", fill="both", expand=True)

    scroll = tk.Scrollbar(container, command=lambda *args: (editor.yview(*args), numeros_linha.yview(*args)))
    scroll.pack(side="right", fill="y")
    editor.config(yscrollcommand=scroll.set)
    numeros_linha.config(yscrollcommand=scroll.set)

    estilo = get_style_by_name("dracula")
    for token, style in estilo:
        if style["color"]:
            editor.tag_config(str(token), foreground="#" + style["color"])

    def colorir_sintaxe(event=None):
        codigo = editor.get("1.0", "end-1c")
        editor.mark_set("range_start", "1.0")
        editor.tag_remove("Token", "1.0", "end")

        for tag in editor.tag_names():
            editor.tag_remove(tag, "1.0", "end")

        tokens = lex(codigo, PythonLexer())
        pos = "1.0"
        for ttype, value in tokens:
            linhas = value.split("\n")
            for i, linha in enumerate(linhas):
                if linha:
                    end = f"{pos}+{len(linha)}c"
                    editor.tag_add(str(ttype), pos, end)
                    pos = end
                if i < len(linhas) - 1:
                    linha_atual = int(pos.split(".")[0]) + 1
                    pos = f"{linha_atual}.0"

    def atualizar_linhas(event=None):
        linhas = editor.index("end-1c").split(".")[0]
        numeros = "\n".join(str(i) for i in range(1, int(linhas) + 1))
        numeros_linha.config(state="normal")
        numeros_linha.delete("1.0", "end")
        numeros_linha.insert("1.0", numeros)
        numeros_linha.config(state="disabled")

    # AUTOCOMPLETE
    popup = None
    def mostrar_autocomplete(event=None):
        nonlocal popup
        palavra = editor.get("insert linestart", "insert").split()[-1]
        sugestoes = [k for k in PYTHON_KEYWORDS if k.startswith(palavra)]
        if not sugestoes:
            if popup:
                popup.destroy()
                popup = None
            return
        if popup:
            popup.destroy()
        popup = tk.Toplevel(editor)
        popup.wm_overrideredirect(True)
        x, y, _, _ = editor.bbox("insert")
        x += editor.winfo_rootx()
        y += editor.winfo_rooty() + 20
        popup.geometry(f"+{x}+{y}")
        lb = tk.Listbox(popup, bg="white", fg="black")
        for s in sugestoes:
            lb.insert(tk.END, s)
        lb.pack()

        def inserir(event):
            selecao = lb.get(tk.ACTIVE)
            editor.insert("insert", selecao[len(palavra):])
            popup.destroy()

        lb.bind("<Return>", inserir)
        lb.bind("<Button-1>", inserir)
        lb.focus_set()

    editor.bind("<KeyRelease>", lambda e: (
        colorir_sintaxe(),
        atualizar_linhas(),
        mostrar_autocomplete()
    ))

    editor.bind("<MouseWheel>", atualizar_linhas)

    resultado_label = tk.Label(janela, text="", font=("Arial", 12), bg="#282a36", fg="white")
    resultado_label.pack(pady=10)

    def executar_codigo():
        codigo = editor.get("1.0", tk.END)

        try:
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()
            sys.stdin = io.StringIO(entrada)

            exec(codigo, {})

            saida_do_aluno = sys.stdout.getvalue().strip()
            sys.stdout = old_stdout

            if saida_do_aluno == saida_esperada.strip():
                resultado_label.config(text="✅ Correto!", fg="#50fa7b")
                resultado = "correto"
            else:
                resultado_label.config(
                    text=f"❌ Errado!\nEsperado: {saida_esperada}\nObtido: {saida_do_aluno}",
                    fg="#ff5555"
                )
                resultado = "incorreto"

            salvar_submissao(usuario[0], questao_id, codigo, saida_do_aluno, resultado)
        except Exception as e:
            resultado_label.config(text=f"Erro ao executar: {str(e)}", fg="#ff5555")
            sys.stdout = old_stdout
            salvar_submissao(usuario[0], questao_id, codigo, "", "erro")

    def salvar_submissao(id_aluno, id_questao, codigo, saida, resultado):
        conn = sqlite3.connect("database/db.sqlite3")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO submissoes (id_aluno, id_questao, codigo, saida_obtida, resultado, data_hora)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            id_aluno,
            id_questao,
            codigo,
            saida,
            resultado,
            datetime.now().isoformat()
        ))
        conn.commit()
        conn.close()

    btn_frame = tk.Frame(janela, bg="#282a36")
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Executar", command=executar_codigo, bg="#44475a", fg="white").pack(side="left", padx=10)

    atualizar_linhas()
    colorir_sintaxe()

    janela.mainloop()
