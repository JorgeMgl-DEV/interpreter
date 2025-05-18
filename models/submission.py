import sqlite3

def criar_tabela_submissoes():
    conn = sqlite3.connect("database/db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS submissoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_aluno INTEGER NOT NULL,
        id_questao INTEGER NOT NULL,
        codigo TEXT NOT NULL,
        saida_obtida TEXT,
        resultado TEXT NOT NULL,
        data_hora TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    criar_tabela_submissoes()
