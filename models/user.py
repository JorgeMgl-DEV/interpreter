import sqlite3

def criar_tabela_usuarios():
    conn = sqlite3.connect("database/db.sqlite3")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        tipo TEXT NOT NULL CHECK(tipo IN ('professor', 'aluno'))
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    criar_tabela_usuarios()
