# 🧠 Codegib

**Codegib** é uma plataforma local de desafios de programação desenvolvida em Python com Tkinter, voltada para ambientes educacionais. Professores podem cadastrar questões e alunos podem resolvê-las com um editor de código embutido, tudo com análise automática e histórico de submissões.

---

## 🎯 Funcionalidades

### 👨‍🏫 Para Professores
- Cadastro de questões com enunciado, entrada e saída esperada
- Visualização de todas as submissões dos alunos
- Sistema local seguro, com possibilidade de integração futura com a nuvem (Firebase)

### 👨‍🎓 Para Alunos
- Lista de questões disponíveis
- Editor de código completo com:
  - Syntax Highlight (tema Dracula)
  - Autocomplete básico
  - Numeração de linhas
  - Modo Tela Cheia (F11)
- Execução do código com entrada simulada
- Análise automática da saída
- Histórico completo de todas as tentativas

---

## 🛠 Tecnologias Utilizadas

- **Python 3**
- **Tkinter** — interface gráfica
- **SQLite** — banco de dados local
- **Pygments** — destaque de sintaxe
- **io + sys** — manipulação de entrada/saída do código
- **(Em breve) Firebase** — para sincronização em nuvem

---

## 🚀 Como executar

```bash
# Cria e ativa o ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows

# Instala dependências
pip install Pygments

# Executa o app
python main.py
#   i n t e r p r e t e r  
 