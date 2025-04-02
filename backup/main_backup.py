import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import Calendar
import sqlite3

# Declaração global das variáveis para o calendário
calendario_inicio = None
calendario_fim = None

# Função para listar todos os projetos com seus status
def listar_projetos_com_status():
    for widget in root.winfo_children():
        widget.destroy()

    conn = sqlite3.connect('gestao_projetos.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id, nome, status FROM projetos")
    projetos = cursor.fetchall()

    if len(projetos) == 0:
        messagebox.showinfo("Nenhum Projeto", "Nenhum projeto cadastrado!")
        voltar_tela_inicial()
    else:
        frame_lista_projetos = tk.Frame(root)
        frame_lista_projetos.pack(padx=10, pady=10)

        tk.Label(frame_lista_projetos, text="Lista de Projetos e Status:").grid(row=0, column=0, columnspan=3, pady=10)
        voltar_button = tk.Button(frame_lista_projetos, text="Voltar Tela Inicial", command=voltar_tela_inicial)
        voltar_button.grid(row=1, column=0, columnspan=3, pady=10)

        tk.Label(frame_lista_projetos, text="Projeto").grid(row=2, column=0, pady=5)
        tk.Label(frame_lista_projetos, text="Status Atual").grid(row=2, column=1, pady=5)

        for idx, projeto in enumerate(projetos, start=3):
            id_projeto, nome_projeto, status = projeto
            tk.Label(frame_lista_projetos, text=nome_projeto).grid(row=idx, column=0, pady=5)
            tk.Label(frame_lista_projetos, text=status).grid(row=idx, column=1, pady=5)

            # Botão para alterar o status
            alterar_status_button = tk.Button(frame_lista_projetos, text="Alterar Status", command=lambda id=id_projeto, status=status: mostrar_status_projeto(id))
            alterar_status_button.grid(row=idx, column=2, pady=5)

            # Botão para ver as tarefas relacionadas ao projeto
            ver_status_tarefas_button = tk.Button(frame_lista_projetos, text="Ver Status Tarefas", command=lambda id=id_projeto: listar_tarefas_por_projeto(id))
            ver_status_tarefas_button.grid(row=idx, column=3, pady=5)

    conn.close()

def listar_tarefas_por_projeto(id_projeto):
    for widget in root.winfo_children():
        widget.destroy()

    conn = sqlite3.connect('gestao_projetos.db')
    cursor = conn.cursor()

    # Selecionar as tarefas relacionadas ao projeto
    cursor.execute("SELECT id, nome, status FROM tarefas WHERE id_projeto = ?", (id_projeto,))
    tarefas = cursor.fetchall()

    if len(tarefas) == 0:
        messagebox.showinfo("Nenhuma Tarefa", "Nenhuma tarefa cadastrada para este projeto.")
        voltar_tela_inicial()
    else:
        frame_lista_tarefas = tk.Frame(root)
        frame_lista_tarefas.pack(padx=10, pady=10)

        tk.Label(frame_lista_tarefas, text="Lista de Tarefas e Status:").grid(row=0, column=0, columnspan=3, pady=10)
        voltar_button = tk.Button(frame_lista_tarefas, text="Voltar a Lista de Projetos", command=voltar_tela_lista_de_projetos)
        voltar_button.grid(row=1, column=0, columnspan=3, pady=10)

        tk.Label(frame_lista_tarefas, text="Tarefa").grid(row=2, column=0, pady=5)
        tk.Label(frame_lista_tarefas, text="Status Atual").grid(row=2, column=1, pady=5)

        for idx, tarefa in enumerate(tarefas, start=3):
            id_tarefa, nome_tarefa, status_tarefa = tarefa
            tk.Label(frame_lista_tarefas, text=nome_tarefa).grid(row=idx, column=0, pady=5)
            tk.Label(frame_lista_tarefas, text=status_tarefa).grid(row=idx, column=1, pady=5)

            # Botão para alterar o status da tarefa
            alterar_status_button = tk.Button(frame_lista_tarefas, text="Alterar Status", command=lambda id=id_tarefa, status=status_tarefa, proj_id=id_projeto: mostrar_status_tarefa(id, status, proj_id))
            alterar_status_button.grid(row=idx, column=2, pady=5)

    conn.close()

def mostrar_status_tarefa(id_tarefa, status_atual, id_projeto):
    def salvar_novo_status():
        novo_status = status_combobox.get()
        conn = sqlite3.connect('gestao_projetos.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE tarefas SET status = ? WHERE id = ?", (novo_status, id_tarefa))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Status da tarefa alterado com sucesso!")
        listar_tarefas_por_projeto(id_projeto)

    janela_status = tk.Toplevel(root)
    janela_status.title("Alterar Status da Tarefa")

    tk.Label(janela_status, text="Selecione o novo status para a tarefa:").pack(pady=10)

    status_combobox = ttk.Combobox(janela_status, values=["Em andamento", "Concluída", "Pendente"], state="readonly")
    status_combobox.set(status_atual)  # Preenche o combobox com o status atual
    status_combobox.pack(pady=10)

    tk.Button(janela_status, text="Salvar", command=salvar_novo_status).pack(pady=10)
    tk.Button(janela_status, text="Cancelar", command=janela_status.destroy).pack(pady=10)


def mostrar_status_projeto(id_projeto):
    # Buscar o status atual do projeto
    conn = sqlite3.connect('gestao_projetos.db')
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM projetos WHERE id = ?", (id_projeto,))
    status_atual = cursor.fetchone()[0]
    conn.close()

    # Função para salvar o novo status
    def salvar_novo_status():
        novo_status = status_combobox.get()
        conn = sqlite3.connect('gestao_projetos.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE projetos SET status = ? WHERE id = ?", (novo_status, id_projeto))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Status do projeto alterado com sucesso!")
        voltar_tela_lista_de_projetos()

    # Criar a janela de alteração de status
    janela_status = tk.Toplevel(root)
    janela_status.title("Alterar Status do Projeto")

    tk.Label(janela_status, text=f"Status Atual do Projeto: {status_atual}").pack(pady=10)

    # Combobox para selecionar o novo status
    status_combobox = ttk.Combobox(janela_status, values=["Em andamento", "Concluído", "Em atraso"], state="readonly")
    status_combobox.set(status_atual)  # Definir o status atual como valor padrão
    status_combobox.pack(pady=10)

    # Botões para salvar e cancelar
    tk.Button(janela_status, text="Salvar", command=salvar_novo_status).pack(pady=10)
    tk.Button(janela_status, text="Cancelar", command=janela_status.destroy).pack(pady=10)


def criar_tabela_tarefas_projetos():
    # Conectar ao banco de dados
    conn = sqlite3.connect('gestao_projetos.db')
    cursor = conn.cursor()

    # Criar a tabela tarefas, caso não exista
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tarefas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_projeto INTEGER,
        nome TEXT,
        descricao TEXT,
        data_inicio TEXT,
        data_fim TEXT,
        status TEXT,
        responsavel TEXT,
        prioridade TEXT,
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
        data_fim_tarefa TEXT,
        status_tarefa TEXT,
        responsavel TEXT,
        prioridade TEXT,
        FOREIGN KEY (id_melhoria) REFERENCES melhorias(id)
    )
    ''')

    conn.commit()
    conn.close()



# Função para salvar os dados do projeto
def salvar_projeto():
    projeto_nome = project_name_entry.get()
    projeto_descricao = project_description_entry.get()
    projeto_inicio = project_start_date_entry.get()
    projeto_fim = project_end_date_entry.get()
    projeto_status = project_status_combobox.get()
    projeto_prioridade = project_priority_combobox.get()
    projeto_categoria = project_category_combobox.get()

    # Insira os dados no banco ou salve conforme sua necessidade
    conn = sqlite3.connect('gestao_projetos.db')
    cursor = conn.cursor()

    # Criar a tabela de projetos, caso não exista
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS projetos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        descricao TEXT,
        data_inicio TEXT,
        data_fim TEXT,
        status TEXT,
        prioridade TEXT,
        categoria TEXT
    )
    ''')

    cursor.execute('''
    INSERT INTO projetos (nome, descricao, data_inicio, data_fim, status, prioridade, categoria)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (projeto_nome, projeto_descricao, projeto_inicio, projeto_fim, projeto_status, projeto_prioridade, projeto_categoria))

    conn.commit()
    conn.close()

    messagebox.showinfo("Sucesso", "Projeto salvo com sucesso!")
    voltar_tela_inicial()

# Função para voltar à tela inicial
def voltar_tela_inicial():
    for widget in root.winfo_children():
        widget.destroy()

    criar_tela_inicial()

# Função para voltar à tela inicial
def voltar_tela_lista_de_projetos():
    for widget in root.winfo_children():
        widget.destroy()

    listar_projetos_com_status()

def criar_tela_novo_projeto():
    for widget in root.winfo_children():
        widget.destroy()

    frame_projeto = tk.Frame(root, width=500, height=400)  # Aumentar tamanho do frame
    frame_projeto.pack_propagate(False)  # Impede que o frame se ajuste ao conteúdo
    frame_projeto.pack(padx=10, pady=10, fill='both', expand=True)

    tk.Label(frame_projeto, text="Nome do Projeto:").grid(row=0, column=0, sticky="e")
    global project_name_entry
    project_name_entry = tk.Entry(frame_projeto)
    project_name_entry.grid(row=0, column=1, pady=5)

    tk.Label(frame_projeto, text="Descrição:").grid(row=1, column=0, sticky="e")
    global project_description_entry
    project_description_entry = tk.Entry(frame_projeto)
    project_description_entry.grid(row=1, column=1, pady=5)

    tk.Label(frame_projeto, text="Data de Início:").grid(row=2, column=0, sticky="e")
    global project_start_date_entry
    project_start_date_entry = tk.Entry(frame_projeto)
    project_start_date_entry.grid(row=2, column=1, pady=5)

    # Botão para abrir o calendário de início
    project_start_date_button = tk.Button(frame_projeto, text="Escolher Data", command=lambda: abrir_calendario_inicio(project_start_date_entry))
    project_start_date_button.grid(row=2, column=2, pady=5)

    tk.Label(frame_projeto, text="Data de Término Proposto:").grid(row=3, column=0, sticky="e")
    global project_end_date_entry
    project_end_date_entry = tk.Entry(frame_projeto)
    project_end_date_entry.grid(row=3, column=1, pady=5)

    # Botão para abrir o calendário de término
    project_end_date_button = tk.Button(frame_projeto, text="Escolher Data", command=lambda: abrir_calendario_fim(project_end_date_entry))
    project_end_date_button.grid(row=3, column=2, pady=5)

    tk.Label(frame_projeto, text="Status Atual:").grid(row=4, column=0, sticky="e")
    global project_status_combobox
    project_status_combobox = ttk.Combobox(frame_projeto, values=["Em andamento", "Concluído", "Em atraso"])
    project_status_combobox.grid(row=4, column=1, pady=5)

    tk.Label(frame_projeto, text="Prioridade:").grid(row=5, column=0, sticky="e")
    global project_priority_combobox
    project_priority_combobox = ttk.Combobox(frame_projeto, values=["Alta", "Média", "Baixa"])
    project_priority_combobox.grid(row=5, column=1, pady=5)

    tk.Label(frame_projeto, text="Categoria:").grid(row=6, column=0, sticky="e")
    global project_category_combobox
    project_category_combobox = ttk.Combobox(frame_projeto, values=["RPA", "Power BI", "Melhoria de Processos"])
    project_category_combobox.grid(row=6, column=1, pady=5)

    salvar_button = tk.Button(frame_projeto, text="Salvar Projeto", command=salvar_projeto)
    salvar_button.grid(row=7, column=1, pady=10, sticky="e")

    voltar_button = tk.Button(frame_projeto, text="Voltar", command=voltar_tela_inicial)
    voltar_button.grid(row=7, column=0, pady=10, sticky="w")

# Inicializando as variáveis globais para os botões de confirmação
confirm_button_inicio = None
confirm_button_fim = None

# Função para abrir o calendário de início do projeto
def abrir_calendario_inicio(entry_cam):
    global calendario_inicio, confirm_button_inicio  # Garantindo que as variáveis globais são usadas
    if calendario_inicio:
        calendario_inicio.place_forget()
        calendario_inicio = None
    if confirm_button_inicio:
        confirm_button_inicio.place_forget()
        confirm_button_inicio = None

    # Aumentando o tamanho do calendário
    calendario_inicio = Calendar(root, date_pattern="dd/mm/yyyy", 
                                 width=400, height=300)  # Aumentando a largura e altura do calendário
    calendario_inicio.place(x=100, y=200)  # Posição fixa (100px, 200px)

    # Adicionar o botão "Confirmar Data" no calendário de início
    entry = entry_cam
    confirm_button_inicio = tk.Button(root, text="Confirmar Data", command=lambda: confirmar_data_inicio(entry))
    confirm_button_inicio.place(x=400, y=230)  # Ajuste a posição do botão conforme necessário

# Função para abrir o calendário de término do projeto
def abrir_calendario_fim(entry_cam):
    global calendario_fim, confirm_button_fim  # Garantindo que as variáveis globais são usadas
    if calendario_fim:
        calendario_fim.place_forget()
        calendario_fim = None
    if confirm_button_fim:
        confirm_button_fim.place_forget()
        confirm_button_fim = None

    # Aumentando o tamanho do calendário
    calendario_fim = Calendar(root, date_pattern="dd/mm/yyyy", 
                              width=400, height=300)  # Aumentando a largura e altura do calendário
    calendario_fim.place(x=100, y=200)  # Posição fixa (100px, 200px)

    # Adicionar o botão "Confirmar Data" no calendário de fim
    entry = entry_cam
    confirm_button_fim = tk.Button(root, text="Confirmar Data", command=lambda: confirmar_data_fim(entry))
    confirm_button_fim.place(x=400, y=230)  # Ajuste a posição do botão conforme necessário

# Função para confirmar e pegar a data de início
def confirmar_data_inicio(entry):
    global calendario_inicio, confirm_button_inicio  # Garantindo que as variáveis globais são usadas
    data_inicio = calendario_inicio.get_date()  # Pega a data selecionada no calendário de início
    entry.delete(0, tk.END)
    entry.insert(0, data_inicio)  # Insere no campo de entrada de data de início
    calendario_inicio.place_forget()  # Fecha o calendário de início
    confirm_button_inicio.place_forget()  # Fecha o botão "Confirmar Data"
    calendario_inicio = None
    confirm_button_inicio = None

# Função para confirmar e pegar a data de término
def confirmar_data_fim(entry):
    global calendario_fim, confirm_button_fim  # Garantindo que as variáveis globais são usadas
    data_fim = calendario_fim.get_date()  # Pega a data selecionada no calendário de término
    entry.delete(0, tk.END)
    entry.insert(0, data_fim)  # Insere no campo de entrada de data de término
    calendario_fim.place_forget()  # Fecha o calendário de término
    confirm_button_fim.place_forget()  # Fecha o botão "Confirmar Data"
    calendario_fim = None
    confirm_button_fim = None

# Função para a tela de projeto existente
def criar_tela_projeto_existente():
    for widget in root.winfo_children():
        widget.destroy()

    conn = sqlite3.connect('gestao_projetos.db')
    cursor = conn.cursor()

    # Verificar se a tabela de projetos existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS projetos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        descricao TEXT,
        data_inicio TEXT,
        data_fim TEXT,
        status TEXT,
        prioridade TEXT,
        categoria TEXT
    )''')

    cursor.execute("SELECT id, nome FROM projetos")
    projetos = cursor.fetchall()

    if len(projetos) == 0:
        messagebox.showinfo("Nenhum Projeto", "Nenhum projeto cadastrado!")
        voltar_tela_inicial()
    else:
        frame_projeto = tk.Frame(root)
        frame_projeto.pack(padx=10, pady=10)

        tk.Label(frame_projeto, text="Selecione um Projeto:").grid(row=0, column=0, columnspan=2, pady=10)

        # Criando o ComboBox para selecionar o projeto
        lista_nomes_projetos = [nome_projeto for _, nome_projeto in projetos]  # Extraindo apenas os nomes dos projetos
        combo_projetos = ttk.Combobox(frame_projeto, values=lista_nomes_projetos, state="readonly")
        combo_projetos.grid(row=1, column=0, columnspan=2, pady=5)

        # Função para abrir o projeto selecionado
        def selecionar_projeto():
            projeto_selecionado = combo_projetos.get()
            if projeto_selecionado:
                # Obter o ID do projeto selecionado
                id_projeto = next(id for id, nome in projetos if nome == projeto_selecionado)
                abrir_tela_projeto(id_projeto)
            else:
                messagebox.showwarning("Seleção Inválida", "Selecione um projeto da lista.")

        # Botão para selecionar o projeto
        botao_selecionar = tk.Button(frame_projeto, text="Selecionar", command=selecionar_projeto)
        botao_selecionar.grid(row=2, column=0, columnspan=2, pady=10)

    conn.close()

# Função para abrir os detalhes do projeto
def abrir_tela_projeto(id_projeto):
    for widget in root.winfo_children():
        widget.destroy()

    frame_projeto = tk.Frame(root)
    frame_projeto.pack(padx=10, pady=10)

    tk.Label(frame_projeto, text="Projeto Selecionado").grid(row=0, column=0, pady=10)

    add_task_button = tk.Button(frame_projeto, text="Adicionar Tarefa", command=lambda: adicionar_tarefa(id_projeto))
    add_task_button.grid(row=1, column=0, pady=5)

    add_improvement_button = tk.Button(frame_projeto, text="Adicionar Melhoria", command=lambda: adicionar_melhoria(id_projeto))
    add_improvement_button.grid(row=2, column=0, pady=5)

    add_deadline_button = tk.Button(frame_projeto, text="Adicionar Prazo")
    add_deadline_button.grid(row=3, column=0, pady=5)

    add_involved_button = tk.Button(frame_projeto, text="Adicionar Envolvido")
    add_involved_button.grid(row=4, column=0, pady=5)

    status_button = tk.Button(frame_projeto, text="Status do Projeto", command=lambda: mostrar_status_projeto(id_projeto))
    status_button.grid(row=5, column=0, pady=5)

    ver_status_tarefas_button = tk.Button(frame_projeto, text="Lista de Tarefas do Projeto", command=lambda: listar_tarefas_por_projeto(id_projeto))
    ver_status_tarefas_button.grid(row=6, column=0, pady=5)

    voltar_button = tk.Button(frame_projeto, text="Voltar Tela Inicial", command=voltar_tela_inicial)
    voltar_button.grid(row=7, column=0, pady=10)

# Função para adicionar tarefa
def adicionar_tarefa(id_projeto):
    # Verifica o status do projeto
    conn = sqlite3.connect('gestao_projetos.db')
    cursor = conn.cursor()

    cursor.execute("SELECT status FROM projetos WHERE id = ?", (id_projeto,))
    status_projeto = cursor.fetchone()[0]

    if status_projeto == "Concluído":
        # Se o projeto for "Concluído", abre a tela para selecionar uma melhoria
        try:
            cursor.execute("SELECT id, descricao_melhoria FROM melhorias WHERE id_projeto = ? AND status_melhoria = 'Em andamento'", (id_projeto,))
            melhorias = cursor.fetchall()

            if not melhorias:
                messagebox.showwarning("Nenhuma melhoria em andamento", "Não há melhorias em andamento para associar a uma tarefa.")
                conn.close()
                return

            for widget in root.winfo_children():
                widget.destroy()
        except Exception as e:
            messagebox.showwarning("Nenhuma melhoria em andamento", "Não há melhorias em andamento para associar a uma tarefa.")
            conn.close()  # Fechar a conexão
            return  # Retorna para evitar que a função continue

            for widget in root.winfo_children():
                widget.destroy()

        frame_tarefa = tk.Frame(root)
        frame_tarefa.pack(padx=10, pady=10)

        tk.Label(frame_tarefa, text="Adicionar Tarefa ao Projeto (Escolha a Melhoria)").grid(row=0, column=0, pady=10)

        # ComboBox para selecionar a melhoria
        melhoria_combobox = ttk.Combobox(frame_tarefa, values=[desc for id, desc in melhorias])
        melhoria_combobox.grid(row=1, column=1, pady=5)

        tk.Label(frame_tarefa, text="Nome da Tarefa:").grid(row=2, column=0, pady=5)
        nome_tarefa_entry = tk.Entry(frame_tarefa)
        nome_tarefa_entry.grid(row=2, column=1, pady=5)

        tk.Label(frame_tarefa, text="Descrição da Tarefa:").grid(row=3, column=0, pady=5)
        descricao_tarefa_entry = tk.Entry(frame_tarefa)
        descricao_tarefa_entry.grid(row=3, column=1, pady=5)

        tk.Label(frame_tarefa, text="Data de Início:").grid(row=4, column=0, sticky="e")
        data_inicio_tarefa_entry = tk.Entry(frame_tarefa)
        data_inicio_tarefa_entry.grid(row=4, column=1, pady=5)

        # Botão para abrir o calendário de início
        data_inicio_tarefa_button = tk.Button(frame_tarefa, text="Escolher Data", command=lambda: abrir_calendario_inicio(data_inicio_tarefa_entry))
        data_inicio_tarefa_button.grid(row=4, column=2, pady=5)

        tk.Label(frame_tarefa, text="Data de Término:").grid(row=5, column=0, sticky="e")
        data_termino_tarefa_entry = tk.Entry(frame_tarefa)
        data_termino_tarefa_entry.grid(row=5, column=1, pady=5)

        # Botão para abrir o calendário de término
        data_fim_tarefa_button = tk.Button(frame_tarefa, text="Escolher Data", command=lambda: abrir_calendario_fim(data_termino_tarefa_entry))
        data_fim_tarefa_button.grid(row=5, column=2, pady=5)

        tk.Label(frame_tarefa, text="Prioridade:").grid(row=6, column=0, pady=5)
        prioridade_combobox = ttk.Combobox(frame_tarefa, values=["Alta", "Média", "Baixa"])
        prioridade_combobox.grid(row=6, column=1, pady=5)

        tk.Label(frame_tarefa, text="Status:").grid(row=7, column=0, pady=5)
        status_combobox = ttk.Combobox(frame_tarefa, values=["Em andamento", "Concluída", "Pendente"])
        status_combobox.grid(row=7, column=1, pady=5)

        # Função para salvar a tarefa
        def salvar_tarefa():

            # Cria a tabela tarefas, se não existir
            criar_tabela_tarefas_melhorias()

            id_melhoria = melhoria_combobox.get()
            nome_tarefa = nome_tarefa_entry.get()
            descricao_tarefa = descricao_tarefa_entry.get()
            data_inicio_tarefa = data_inicio_tarefa_entry.get()
            data_termino_tarefa = data_termino_tarefa_entry.get()
            prioridade = prioridade_combobox.get()
            status = status_combobox.get()

            # Buscar o ID da melhoria selecionada
            cursor.execute("SELECT id FROM melhorias WHERE descricao_melhoria = ? AND id_projeto = ?", (id_melhoria, id_projeto))
            id_melhoria_selected = cursor.fetchone()[0]

            cursor.execute("INSERT INTO tarefas (id_melhoria, nome_tarefa, descricao_tarefa, data_inicio_tarefa, data_termino_tarefa, prioridade_tarefa, status_tarefa) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (id_melhoria_selected, nome_tarefa, descricao_tarefa, data_inicio_tarefa, data_termino_tarefa, prioridade, status))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Tarefa associada à melhoria com sucesso!")
            voltar_tela_inicial()

        salvar_button = tk.Button(frame_tarefa, text="Salvar", command=salvar_tarefa)
        salvar_button.grid(row=8, column=1, pady=10)

        voltar_button = tk.Button(frame_tarefa, text="Voltar", command=voltar_tela_inicial)
        voltar_button.grid(row=9, column=1, pady=10)

    else:
        # Se o projeto não for "Concluído", apenas adiciona a tarefa normalmente
        messagebox.showinfo("Status do Projeto", "Você está adicionando uma tarefa ao projeto.")

        for widget in root.winfo_children():
            widget.destroy()

        frame_tarefa = tk.Frame(root)
        frame_tarefa.pack(padx=10, pady=10)

        tk.Label(frame_tarefa, text="Adicionar Tarefa ao Projeto").grid(row=0, column=0, pady=10)

        tk.Label(frame_tarefa, text="Nome da Tarefa:").grid(row=1, column=0, pady=5)
        nome_tarefa_entry = tk.Entry(frame_tarefa)
        nome_tarefa_entry.grid(row=1, column=1, pady=5)

        tk.Label(frame_tarefa, text="Descrição da Tarefa:").grid(row=2, column=0, pady=5)
        descricao_tarefa_entry = tk.Entry(frame_tarefa)
        descricao_tarefa_entry.grid(row=2, column=1, pady=5)
        
        tk.Label(frame_tarefa, text="Data de Início:").grid(row=3, column=0, sticky="e")
        data_inicio_tarefa_entry = tk.Entry(frame_tarefa)
        data_inicio_tarefa_entry.grid(row=3, column=1, pady=5)

        # Botão para abrir o calendário de início
        data_inicio_tarefa_button = tk.Button(frame_tarefa, text="Escolher Data", command=lambda: abrir_calendario_inicio(data_inicio_tarefa_entry))
        data_inicio_tarefa_button.grid(row=3, column=2, pady=5)

        tk.Label(frame_tarefa, text="Data de Término:").grid(row=4, column=0, sticky="e")
        data_termino_tarefa_entry = tk.Entry(frame_tarefa)
        data_termino_tarefa_entry.grid(row=4, column=1, pady=5)

        # Botão para abrir o calendário de término
        data_fim_tarefa_button = tk.Button(frame_tarefa, text="Escolher Data", command=lambda: abrir_calendario_fim(data_termino_tarefa_entry))
        data_fim_tarefa_button.grid(row=4, column=2, pady=5)

        tk.Label(frame_tarefa, text="Prioridade:").grid(row=5, column=0, pady=5)
        prioridade_combobox = ttk.Combobox(frame_tarefa, values=["Alta", "Média", "Baixa"])
        prioridade_combobox.grid(row=5, column=1, pady=5)

        tk.Label(frame_tarefa, text="Status:").grid(row=6, column=0, pady=5)
        status_combobox = ttk.Combobox(frame_tarefa, values=["Em andamento", "Concluída", "Pendente"])
        status_combobox.grid(row=6, column=1, pady=5)
        

        # Função para salvar a tarefa
        def salvar_tarefa():
            # Cria a tabela tarefas, se não existir
            criar_tabela_tarefas_projetos()

            nome_tarefa = nome_tarefa_entry.get()
            descricao_tarefa = descricao_tarefa_entry.get()
            data_inicio_tarefa = data_inicio_tarefa_entry.get()
            data_termino_tarefa = data_termino_tarefa_entry.get()
            prioridade = prioridade_combobox.get()
            status = status_combobox.get()

            cursor.execute("INSERT INTO tarefas (id_projeto, nome_tarefa, descricao_tarefa, data_inicio_tarefa, data_termino_tarefa, prioridade_tarefa, status_tarefa) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (id_projeto, nome_tarefa, descricao_tarefa, data_inicio_tarefa, data_termino_tarefa, prioridade, status))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso!")
            voltar_tela_inicial()

        salvar_button = tk.Button(frame_tarefa, text="Salvar", command=salvar_tarefa)
        salvar_button.grid(row=7, column=1, pady=10)

        voltar_button = tk.Button(frame_tarefa, text="Voltar", command=voltar_tela_inicial)
        voltar_button.grid(row=8, column=1, pady=10)


def adicionar_melhoria(id_projeto):
    # Verifica o status do projeto
    conn = sqlite3.connect('gestao_projetos.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT status FROM projetos WHERE id = ?", (id_projeto,))
    status_projeto = cursor.fetchone()[0]
    
    if status_projeto != "Concluído":
        messagebox.showwarning(
            "Status do Projeto",
            f"O status atual do projeto é '{status_projeto}'.\n"
            "Você só pode adicionar melhorias se o projeto estiver com o status 'Concluído'."
        )
        conn.close()
        return  # Não continua a função

    # Se o status for "Concluído", abre a tela para adicionar a melhoria
    for widget in root.winfo_children():
        widget.destroy()

    frame_melhoria = tk.Frame(root)
    frame_melhoria.pack(padx=10, pady=10)

    tk.Label(frame_melhoria, text="Adicionar Melhoria ao Projeto").grid(row=0, column=0, pady=10)

    # Campos para adicionar melhoria
    tk.Label(frame_melhoria, text="Descrição da Melhoria:").grid(row=1, column=0, pady=5)
    descricao_entry = tk.Entry(frame_melhoria)
    descricao_entry.grid(row=1, column=1, pady=5)

    tk.Label(frame_melhoria, text="Status da Melhoria:").grid(row=2, column=0, pady=5)
    status_combobox = ttk.Combobox(frame_melhoria, values=["Planejada", "Implementada", "Em andamento"])
    status_combobox.grid(row=2, column=1, pady=5)

    tk.Label(frame_melhoria, text="Impacto da Melhoria:").grid(row=3, column=0, pady=5)
    impacto_combobox = ttk.Combobox(frame_melhoria, values=["Alto", "Médio", "Baixo"])
    impacto_combobox.grid(row=3, column=1, pady=5)

    tk.Label(frame_melhoria, text="Data Início:").grid(row=4, column=0, pady=5)
    data_inicio_entry = tk.Entry(frame_melhoria)
    data_inicio_entry.grid(row=4, column=1, pady=5)

    # Botão para abrir o calendário de início
    data_inicio_tarefa_button = tk.Button(frame_melhoria, text="Escolher Data", command=lambda: abrir_calendario_inicio(data_inicio_entry))
    data_inicio_tarefa_button.grid(row=4, column=2, pady=5)

    tk.Label(frame_melhoria, text="Data Término:").grid(row=5, column=0, pady=5)
    data_termino_entry = tk.Entry(frame_melhoria)
    data_termino_entry.grid(row=5, column=1, pady=5)

    # Botão para abrir o calendário de término
    data_fim_tarefa_button = tk.Button(frame_melhoria, text="Escolher Data", command=lambda: abrir_calendario_fim(data_termino_entry))
    data_fim_tarefa_button.grid(row=5, column=2, pady=5)

    # Função para salvar a melhoria no banco de dados
    def salvar_melhoria():
        criar_tabela_melhorias()
        descricao = descricao_entry.get()
        status = status_combobox.get()
        impacto = impacto_combobox.get()
        data_inicio = data_inicio_entry.get()
        data_termino = data_termino_entry.get()

        cursor.execute("INSERT INTO melhorias (id_projeto, descricao_melhoria, impacto_melhoria, data_inicio_melhoria, data_termino_melhoria, status_melhoria) VALUES (?, ?, ?, ?, ?, ?)",
                       (id_projeto, descricao, impacto, data_inicio, data_termino, status))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Melhoria adicionada com sucesso!")
        voltar_tela_inicial()

    salvar_button = tk.Button(frame_melhoria, text="Salvar", command=salvar_melhoria)
    salvar_button.grid(row=6, column=1, pady=10)

    voltar_button = tk.Button(frame_melhoria, text="Voltar", command=voltar_tela_inicial)
    voltar_button.grid(row=7, column=1, pady=10)



# Função principal para iniciar a interface gráfica
def criar_tela_inicial():
    frame_tela = tk.Frame(root)
    frame_tela.pack(padx=10, pady=10)

    # Botão para adicionar um novo projeto
    botao_adicionar_projeto = tk.Button(frame_tela, text="Adicionar Novo Projeto", command=criar_tela_novo_projeto)
    botao_adicionar_projeto.grid(row=0, column=0, pady=10)

    # Botão para acessar projetos existentes
    botao_projetos_existentes = tk.Button(frame_tela, text="Projetos Existentes", command=criar_tela_projeto_existente)
    botao_projetos_existentes.grid(row=1, column=0, pady=10)

    # Botão para listar todos os projetos com status
    listar_button = tk.Button(frame_tela, text="Listar Projetos com Status", command=listar_projetos_com_status)
    listar_button.grid(row=2, column=0, pady=10)


root = tk.Tk()
root.title("Gestão de Projetos")
root.geometry("600x500")
criar_tela_inicial()
root.mainloop()