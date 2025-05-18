import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess
import tempfile
import os
from datetime import datetime
import sys


def abrir_editor(usuario, questao_id):
    janela = tk.Toplevel()
    janela.title(f"Editor – Questão {questao_id}")
    janela.geometry("950x700")

    # Busca enunciado
    conn = sqlite3.connect("database/db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT enunciado FROM questoes WHERE id = ?", (questao_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        messagebox.showerror("Erro", "Questão não encontrada.")
        return
    enunciado = row[0]

    tk.Label(janela, text="Enunciado:", font=("Arial", 14)).pack(pady=(10,0))
    tk.Message(janela, text=enunciado, width=900).pack(pady=(0,10))

    # Busca casos de teste
    conn = sqlite3.connect("database/db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT entrada, saida_esperada
        FROM test_cases
        WHERE questao_id = ?
    """, (questao_id,))
    casos = cursor.fetchall()
    conn.close()
    if not casos:
        messagebox.showerror("Erro", "Nenhum caso de teste cadastrado para esta questão.")
        return

    # Editor básico (lembra de já ter syntax, linhas etc)
    editor = tk.Text(janela, font=("Consolas", 12), height=20, wrap="none")
    editor.pack(fill="both", expand=True, padx=10, pady=5)

    resultado_label = tk.Label(janela, text="", font=("Arial", 12))
    resultado_label.pack(pady=10)

    def executar_codigo():
        codigo = editor.get("1.0", tk.END)

        # Bloqueio básico
        proibidos = ["import os", "open(", "__import__", "exec(", "eval(", "exit("]
        if any(p in codigo for p in proibidos):
            resultado_label.config(text="❌ Uso de comando proibido!", fg="red")
            salvar_submissao(usuario[0], questao_id, codigo, "", "bloqueado")
            return

        # Cria arquivo temporário só com o código
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w", encoding="utf-8") as tmp:
            tmp.write(codigo)
            temp_path = tmp.name

        outputs = []
        passou_tudo = True
        caso_falha = None

        # Executa para cada caso
        for idx, (inp, exp) in enumerate(casos, start=1):
            try:
                res = subprocess.run(
                    [sys.executable, temp_path],
                    input=inp,
                    capture_output=True,
                    text=True,
                    timeout=3
                )
                out = res.stdout.strip()
            except subprocess.TimeoutExpired:
                passou_tudo = False
                caso_falha = idx
                outputs.append("TIMEOUT")
                break
            outputs.append(out)
            if out != exp.strip():
                passou_tudo = False
                caso_falha = idx
                break

        # Limpa arquivo temporário
        os.remove(temp_path)

        # Mostra resultado no UI
        if passou_tudo:
            resultado_label.config(
                text=f"✅ Todos os {len(casos)} casos passaram!",
                fg="green"
            )
            status = "correto"
        else:
            esperado = casos[caso_falha-1][1]
            obtido = outputs[caso_falha-1]
            resultado_label.config(
                text=(
                    f"❌ Falha no caso {caso_falha}\n"
                    f"Esperado: {esperado}\nObtido: {obtido}"
                ),
                fg="red"
            )
            status = "incorreto" if outputs[caso_falha-1] not in ("TIMEOUT",) else "timeout"

        # Salva no banco (concatena todas as saídas)
        salvar_submissao(
            usuario[0],
            questao_id,
            codigo,
            "\n".join(outputs),
            status
        )

    def salvar_submissao(id_aluno, id_questao, codigo, saida, resultado):
        conn = sqlite3.connect("database/db.sqlite3")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO submissoes
            (id_aluno, id_questao, codigo, saida_obtida, resultado, data_hora)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (id_aluno, id_questao, codigo, saida, resultado, datetime.now().isoformat()))
        conn.commit()
        conn.close()

    tk.Button(janela, text="Executar", command=executar_codigo).pack(pady=5)
    janela.mainloop()
