import sqlite3

def criar_tabela_test_cases():
    conn = sqlite3.connect("database/db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS test_cases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        questao_id INTEGER NOT NULL,
        entrada TEXT NOT NULL,
        saida_esperada TEXT NOT NULL,
        FOREIGN KEY (questao_id) REFERENCES questoes(id) ON DELETE CASCADE
    )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    criar_tabela_test_cases()
