# ui/editor.py

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import subprocess
import tempfile
import os
import sys
from datetime import datetime
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.styles import get_style_by_name
import difflib

def abrir_editor(usuario, questao_id):
    # --- Carrega dados da questão e casos de teste ---
    conn = sqlite3.connect("database/db.sqlite3")
    cur = conn.cursor()
    cur.execute("SELECT enunciado FROM questoes WHERE id = ?", (questao_id,))
    row = cur.fetchone()
    cur.execute("SELECT entrada, saida_esperada FROM test_cases WHERE questao_id = ?", (questao_id,))
    casos = cur.fetchall()
    conn.close()

    if not row or not casos:
        messagebox.showerror("Erro", "Questão ou casos de teste não encontrados.")
        return
    enunciado = row[0]

    # --- Janela principal ---
    win = tk.Toplevel()
    win.title(f"Editor – Questão {questao_id}")
    win.geometry("950x700")
    win.configure(bg="#282a36")
    fullscreen = False

    def toggle_fullscreen(event=None):
        nonlocal fullscreen
        fullscreen = not fullscreen
        win.attributes("-fullscreen", fullscreen)

    win.bind("<F11>", toggle_fullscreen)

    # --- Toolbar ---
    toolbar = ttk.Frame(win)
    toolbar.pack(fill="x", pady=2)
    btn_run   = ttk.Button(toolbar, text="▶️ Run",       command=lambda: run_code())
    btn_clear = ttk.Button(toolbar, text="✖ Clear",     command=lambda: clear_code())
    btn_fs    = ttk.Button(toolbar, text="⛶ Fullscreen", command=toggle_fullscreen)
    for b in (btn_run, btn_clear, btn_fs):
        b.pack(side="left", padx=4)

    # --- Container de editor + linhas ---
    container = ttk.Frame(win)
    container.pack(fill="both", expand=True, padx=5, pady=5)

    ln = tk.Text(container, width=4, padx=4, takefocus=0, border=0,
                 bg="#282a36", fg="#6272a4", state="disabled")
    ln.pack(side="left", fill="y")

    editor = tk.Text(container, font=("Consolas",12), bg="#282a36", fg="#f8f8f2",
                     insertbackground="white", undo=True, wrap="none")
    editor.pack(side="left", fill="both", expand=True)

    scroll = ttk.Scrollbar(container,
        command=lambda *a: (editor.yview(*a), ln.yview(*a)))
    scroll.pack(side="right", fill="y")
    editor.config(yscrollcommand=scroll.set)
    ln.config(yscrollcommand=scroll.set)

    # --- Syntax Highlight (Dracula) ---
    style = get_style_by_name("dracula")
    for ttype, spec in style:
        if spec["color"]:
            editor.tag_config(str(ttype), foreground="#" + spec["color"])

    # --- Status Bar ---
    status = ttk.Frame(win)
    status.pack(fill="x")
    cursor_lbl = ttk.Label(status, text="Ln 1, Col 0",
                           background="#282a36", foreground="#f8f8f2")
    result_lbl = ttk.Label(status, text="",
                           background="#282a36", foreground="#50fa7b")
    cursor_lbl.pack(side="left", padx=5)
    result_lbl.pack(side="left", padx=20)

    # --- Funções de apoio ---
    def update_lines(event=None):
        total = int(editor.index("end-1c").split(".")[0])
        nums  = "\n".join(str(i) for i in range(1, total+1))
        ln.config(state="normal")
        ln.delete("1.0","end")
        ln.insert("1.0", nums)
        ln.config(state="disabled")

    def color_syntax(event=None):
        code = editor.get("1.0","end-1c")
        editor.mark_set("range_start","1.0")
        for tag in editor.tag_names():
            editor.tag_remove(tag,"1.0","end")
        for ttype, val in lex(code, PythonLexer()):
            if not val:
                continue
            start = editor.index("range_start")
            end   = f"{start}+{len(val)}c"
            editor.tag_add(str(ttype), start, end)
            editor.mark_set("range_start", end)

    def update_cursor(event=None):
        idx = editor.index("insert")
        line, col = idx.split(".")
        cursor_lbl.config(text=f"Ln {line}, Col {col}")

    def clear_code():
        editor.delete("1.0","end")
        result_lbl.config(text="")
        update_lines(); color_syntax()

    def run_code():
        code = editor.get("1.0","end")
        forbidden = ("import os", "open(", "exec(", "eval(", "exit(")
        if any(p in code for p in forbidden):
            result_lbl.config(text="❌ Comando proibido", foreground="#ff5555")
            return

        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".py",
                                          mode="w", encoding="utf-8")
        tmp.write(f"import sys, io\nsys.stdin = io.StringIO('''{casos[0][0]}''')\n")
        tmp.write(code)
        tmp.close()

        outputs = []; ok = True; fail = 0
        for i, (inp, exp) in enumerate(casos, start=1):
            try:
                res = subprocess.run(
                    [sys.executable, tmp.name],
                    input=inp, capture_output=True, text=True, timeout=3
                )
                out = res.stdout.strip()
            except subprocess.TimeoutExpired:
                ok=False; fail=i; outputs.append("TIMEOUT"); break
            outputs.append(out)
            if out != exp.strip():
                ok=False; fail=i; break

        try:
            os.remove(tmp.name)
        except OSError:
            pass

        if ok:
            result_lbl.config(text=f"✅ {len(casos)} OK", foreground="#50fa7b")
            status_txt = "correto"
        else:
            esperado = casos[fail-1][1].strip()
            obtido   = outputs[fail-1]
            hint = ""
            if esperado == obtido.strip():
                hint = "Verifique espaços/linhas."
            elif any("invalid literal for int" in o for o in outputs):
                hint = "Use int(input())."
            else:
                diff = "\n".join(difflib.ndiff(
                    esperado.splitlines(),
                    obtido.splitlines()
                ))
                hint = f"Diferenças:\n{diff}"
            result_lbl.config(
                text=f"❌ Caso {fail} falhou\n{hint}",
                foreground="#ff5555"
            )
            status_txt = "incorreto" if outputs[fail-1] != "TIMEOUT" else "timeout"

        # Salva submissão
        conn2 = sqlite3.connect("database/db.sqlite3")
        cur2 = conn2.cursor()
        cur2.execute("""
            INSERT INTO submissoes
            (id_aluno, id_questao, codigo, saida_obtida, resultado, data_hora)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            usuario[0],
            questao_id,
            code,
            "\n".join(outputs),
            status_txt,
            datetime.now().isoformat()
        ))
        conn2.commit()
        conn2.close()

    # --- Bindings ---
    editor.bind("<KeyRelease>", update_lines)
    editor.bind("<KeyRelease>", color_syntax, add='+')
    editor.bind("<KeyRelease>", update_cursor, add='+')
    editor.bind("<ButtonRelease>", update_cursor)
    editor.bind("<MouseWheel>",    update_lines)

    # --- Inicialização ---
    update_lines(); color_syntax(); update_cursor()
    win.mainloop()
