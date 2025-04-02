import sqlite3

def criar_tabela_projetos():
    conn = sqlite3.connect('gestao_projetos.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS projetos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_projeto TEXT,
        descricao_projeto TEXT,
        data_inicio TEXT,
        data_fim TEXT,
        status_projeto TEXT,
        prioridade_projeto TEXT,
        categoria_projeto TEXT
    )
    ''')
    conn.commit()
    conn.close()

def criar_tabela_tarefas_projetos():
    # Conectar ao banco de dados
    conn = sqlite3.connect('gestao_projetos.db')
    cursor = conn.cursor()

    # Criar a tabela tarefas, caso não exista
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tarefas_projetos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_projeto INTEGER,
        nome_tarefa TEXT,
        descricao_tarefa TEXT,
        data_inicio_tarefa TEXT,
        data_termino_tarefa TEXT,
        status_tarefa TEXT,
        prioridade_tarefa TEXT,
        FOREIGN KEY (id_projeto) REFERENCES projetos(id)
    )
    ''')

    conn.commit()
    conn.close()

def criar_tabela_melhorias():
    # Conectar ao banco de dados
    conn = sqlite3.connect('gestao_projetos.db')
    cursor = conn.cursor()

    # Criar a tabela melhorias, caso não exista
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS melhorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_projeto INTEGER,
        nome_melhoria TEXT,
        descricao_melhoria TEXT,
        impacto_melhoria TEXT,
        data_inicio_melhoria TEXT,
        data_termino_melhoria TEXT,
        status_melhoria TEXT,
        FOREIGN KEY (id_projeto) REFERENCES projetos(id)
    )
    ''')

    conn.commit()
    conn.close()

def criar_tabela_tarefas_melhorias():
    # Conectar ao banco de dados
    conn = sqlite3.connect('gestao_projetos.db')
    cursor = conn.cursor()

    # Criar a tabela tarefas_melhorias, caso não exista
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tarefas_melhorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_melhoria INTEGER,
        nome_tarefa TEXT,
        descricao_tarefa TEXT,
        data_inicio_tarefa TEXT,
        data_termino_tarefa TEXT,
        status_tarefa TEXT,
        prioridade_tarefa TEXT,
        FOREIGN KEY (id_melhoria) REFERENCES melhorias(id)
    )
    ''')

    conn.commit()
    conn.close()




def salvar_projeto(nome, descricao, data_inicio, data_fim, status, prioridade, categoria):
    conn = sqlite3.connect('gestao_projetos.db')
    cursor = conn.cursor()

    criar_tabela_projetos()

    # Inserir os dados do projeto
    cursor.execute('''
    INSERT INTO projetos (nome_projeto, descricao_projeto, data_inicio, data_fim, status_projeto, prioridade_projeto, categoria_projeto)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (nome, descricao, data_inicio, data_fim, status, prioridade, categoria))

    conn.commit()
    conn.close()

def listar_projetos():
    conn = sqlite3.connect('gestao_projetos.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome_projeto, status_projeto FROM projetos")
    projetos = cursor.fetchall()
    conn.close()
    return projetos

def atualizar_status_projeto(id_projeto, novo_status):
    conn = sqlite3.connect('gestao_projetos.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE projetos SET status_projeto = ? WHERE id = ?", (novo_status, id_projeto))
    conn.commit()
    conn.close()

# def listar_tarefas_por_projeto(id_projeto):
#     conn = sqlite3.connect('gestao_projetos.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT id, nome_tarefa, status_tarefa FROM tarefas_projetos WHERE id_projeto = ?", (id_projeto,))
#     tarefas = cursor.fetchall()
#     conn.close()
#     return tarefas



# def atualizar_status_tarefa_por_projeto(id_tarefa, novo_status):
#     conn = sqlite3.connect('gestao_projetos.db')
#     cursor = conn.cursor()
#     cursor.execute("UPDATE tarefas_projetos SET status_tarefa = ? WHERE id = ?", (novo_status, id_tarefa))
#     conn.commit()
#     conn.close()

# database.py

def criar_tabela_envolvidos():
    conn = sqlite3.connect('gestao_projetos.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS envolvidos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_projeto INTEGER,
        id_tarefa INTEGER,
        id_melhoria INTEGER,
        id_tarefa_melhoria INTEGER,
        nome_envolvido TEXT NOT NULL,
        papel_envolvido TEXT NOT NULL,
        contato_envolvido TEXT,
        departamento TEXT,
        coordenacao TEXT,
        data_cadastro TEXT,     
        FOREIGN KEY (id_projeto) REFERENCES projetos(id),
        FOREIGN KEY (id_tarefa) REFERENCES tarefas_projetos(id),
        FOREIGN KEY (id_melhoria) REFERENCES melhorias(id),
        FOREIGN KEY (id_tarefa_melhoria) REFERENCES tarefas_melhorias(id)
    )
    ''')
    conn.commit()
    conn.close()


# Atualizar funções de busca e atualização
def buscar_envolvidos(id_projeto, filtro=None):
    conn = sqlite3.connect('gestao_projetos.db')
    cursor = conn.cursor()
    query = '''
    SELECT id, nome_envolvido, papel_envolvido, contato_envolvido, 
           departamento, coordenacao, data_cadastro
    FROM envolvidos 
    WHERE id_projeto = ?
    '''
    params = [id_projeto]
    
    if filtro:
        query += '''
        AND (nome_envolvido LIKE ? OR 
             papel_envolvido LIKE ? OR 
             contato_envolvido LIKE ? OR
             departamento LIKE ? OR
             coordenacao LIKE ?)
        '''
        params.extend([f'%{filtro}%'] * 5)
    
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.close()
    return result

def atualizar_envolvido(id_envolvido, dados):
    conn = sqlite3.connect('gestao_projetos.db')
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE envolvidos 
    SET nome_envolvido = ?,
        papel_envolvido = ?,
        contato_envolvido = ?,
        departamento = ?,
        coordenacao = ?,
        data_cadastro = ?
    WHERE id = ?
    ''', (*dados, id_envolvido))
    conn.commit()
    conn.close()

# Função para buscar todos os envolvidos (para reaproveitamento)
def buscar_todos_envolvidos():
    conn = sqlite3.connect('gestao_projetos.db')
    cursor = conn.cursor()
    cursor.execute('''
    SELECT id, nome_envolvido, papel_envolvido, contato_envolvido, 
           departamento, coordenacao, data_cadastro
    FROM envolvidos
    ORDER BY nome_envolvido
    ''')
    result = cursor.fetchall()
    conn.close()
    return result