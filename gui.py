import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import sqlite3
from datetime import datetime
from database import (
    criar_tabela_projetos,
    salvar_projeto,
    listar_projetos,
    atualizar_status_projeto,
    criar_tabela_tarefas_melhorias,
    criar_tabela_tarefas_projetos,
    criar_tabela_melhorias,
    criar_tabela_envolvidos,
    buscar_envolvidos,
    atualizar_envolvido
)

# Variáveis globais para o calendário
calendario_inicio = None
calendario_fim = None
confirm_button_inicio = None
confirm_button_fim = None

def criar_tela_inicial(root):
    frame_tela = tk.Frame(root)
    frame_tela.pack(padx=10, pady=10)

    criar_tabela_projetos()
    criar_tabela_tarefas_melhorias()
    criar_tabela_tarefas_projetos()
    criar_tabela_melhorias()
    criar_tabela_envolvidos()

    # Botão para adicionar um novo projeto
    botao_adicionar_projeto = tk.Button(frame_tela, text="Adicionar Novo Projeto", command=lambda: criar_tela_novo_projeto(root))
    botao_adicionar_projeto.grid(row=0, column=0, pady=10)

    # Botão para acessar projetos existentes
    botao_projetos_existentes = tk.Button(frame_tela, text="Projetos Existentes", command=lambda: criar_tela_projeto_existente(root))
    botao_projetos_existentes.grid(row=1, column=0, pady=10)

    # Botão para listar todos os projetos com status
    listar_button = tk.Button(frame_tela, text="Listar Projetos com Status", command=lambda: listar_projetos_com_status(root))
    listar_button.grid(row=2, column=0, pady=10)

def criar_tela_novo_projeto(root):
    for widget in root.winfo_children():
        widget.destroy()

    frame_projeto = tk.Frame(root, width=500, height=400)
    frame_projeto.pack_propagate(False)
    frame_projeto.pack(padx=10, pady=10, fill='both', expand=True)

    tk.Label(frame_projeto, text="Nome do Projeto:").grid(row=0, column=0, sticky="e")
    project_name_entry = tk.Entry(frame_projeto)
    project_name_entry.grid(row=0, column=1, pady=5)

    tk.Label(frame_projeto, text="Descrição:").grid(row=1, column=0, sticky="e")
    project_description_entry = tk.Entry(frame_projeto)
    project_description_entry.grid(row=1, column=1, pady=5)

    tk.Label(frame_projeto, text="Data de Início:").grid(row=2, column=0, sticky="e")
    project_start_date_entry = tk.Entry(frame_projeto, state="disabled")
    project_start_date_entry.grid(row=2, column=1, pady=5)

    project_start_date_button = tk.Button(frame_projeto, text="Escolher Data", command=lambda: abrir_calendario_inicio(root, project_start_date_entry))
    project_start_date_button.grid(row=2, column=2, pady=5)

    tk.Label(frame_projeto, text="Data de Término Proposto:").grid(row=3, column=0, sticky="e")
    project_end_date_entry = tk.Entry(frame_projeto, state="disabled")
    project_end_date_entry.grid(row=3, column=1, pady=5)

    project_end_date_button = tk.Button(frame_projeto, text="Escolher Data", command=lambda: abrir_calendario_fim(root, project_end_date_entry))
    project_end_date_button.grid(row=3, column=2, pady=5)

    tk.Label(frame_projeto, text="Status Atual:").grid(row=4, column=0, sticky="e")
    project_status_combobox = ttk.Combobox(frame_projeto, values = [
        "Não iniciado (projeto aprovado, mas execução não começou)",
        "Em planejamento (em fase de escopo, cronograma ou orçamento)",
        "Em andamento (execução ativa e dentro do prazo)",
        "Em revisão (validação pela equipe ou stakeholders)",
        "Pausado (interrompido temporariamente - ex.: falta de recursos)",
        "Bloqueado (impedido por dependências externas)",
        "Em atraso (execução ativa, mas fora do prazo)",
        "Concluído (entregue e aceito formalmente)",
        "Cancelado (abandonado antes da conclusão)",
        "Entregue com pendências (concluído, mas com ajustes menores pendentes)"
    ],width=70)
    project_status_combobox.grid(row=4, column=1, pady=5)

    tk.Label(frame_projeto, text="Prioridade:").grid(row=5, column=0, sticky="e")
    project_priority_combobox = ttk.Combobox(frame_projeto, values = [
        "Crítica (impacto imediato em operações/receita)",
        "Alta (prazo inflexível ou estratégico)",
        "Média (importante, mas com flexibilidade)",
        "Baixa (melhoria ou demanda opcional)",
        "Planejamento (prioridade futura, sem ação imediata)"
    ],width=70)
    project_priority_combobox.grid(row=5, column=1, pady=5)

    tk.Label(frame_projeto, text="Categoria:").grid(row=6, column=0, sticky="e")
    project_category_combobox = ttk.Combobox(frame_projeto, values = [
        "Análise de Dados (se o foco for insights via Power BI)",
        "APP (se envolver desenvolvimento de aplicativo)",
        "Automação Parcial (RPA + etapas manuais)",
        "Automação de Processo (RPA como principal solução)",
        "Dashboard (se o Power BI for o produto final)",
        "ETL (para integração/transformação de dados)",
        "Melhoria Contínua (otimização geral do processo)",
        "Melhoria de Processo (redesenho + automação)",
        "Monitoramento de Dados (se o Power BI for usado para acompanhamento)",
        "Power BI (se a ferramenta for o destaque)",
        "Process Mining (se incluir análise de logs/eventos do processo)",
        "RPA (se a automação robótica for o core)",
        "Sistema Híbrido (combina automação e etapas manuais)"
    ],width=70)
    project_category_combobox.grid(row=6, column=1, pady=5)

    def salvar():
        # Validar campos obrigatórios
        nome = project_name_entry.get()
        descricao = project_description_entry.get()
        data_inicio = project_start_date_entry.get()
        data_fim = project_end_date_entry.get()
        status = project_status_combobox.get()
        prioridade = project_priority_combobox.get()
        categoria = project_category_combobox.get()

        if not nome or not descricao or not data_inicio or not data_fim or not status or not prioridade or not categoria:
            messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos antes de salvar.")
            return

        # Salvar o projeto no banco de dados
        try:
            salvar_projeto(nome, descricao, data_inicio, data_fim, status, prioridade, categoria)
            messagebox.showinfo("Sucesso", "Projeto salvo com sucesso!")
            voltar_tela_inicial(root)
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar o projeto: {e}")

    salvar_button = tk.Button(frame_projeto, text="Salvar Projeto", command=salvar)
    salvar_button.grid(row=7, column=1, pady=10, sticky="e")

    voltar_button = tk.Button(frame_projeto, text="Voltar Tela Inicial", command=lambda: voltar_tela_inicial(root))
    voltar_button.grid(row=7, column=0, pady=10, sticky="w")

def  abrir_calendario_inicio(root, entry):
    global calendario_inicio, confirm_button_inicio
    if calendario_inicio:
        calendario_inicio.place_forget()
        calendario_inicio = None
    if confirm_button_inicio:
        confirm_button_inicio.place_forget()
        confirm_button_inicio = None

    # Aumentando o tamanho do calendário
    calendario_inicio = Calendar(root, date_pattern="dd/mm/yyyy", width=400, height=300)
    calendario_inicio.place(x=100, y=200)

    # Adicionar o botão "Confirmar Data" no calendário de início
    confirm_button_inicio = tk.Button(root, text="Confirmar Data", command=lambda: confirmar_data_inicio(calendario_inicio, entry, confirm_button_inicio))
    confirm_button_inicio.place(x=400, y=230)

def abrir_calendario_fim(root, entry):
    global calendario_fim, confirm_button_fim
    if calendario_fim:
        calendario_fim.place_forget()
        calendario_fim = None
    if confirm_button_fim:
        confirm_button_fim.place_forget()
        confirm_button_fim = None

    # Aumentando o tamanho do calendário
    calendario_fim = Calendar(root, date_pattern="dd/mm/yyyy", width=400, height=300)
    calendario_fim.place(x=100, y=200)

    # Adicionar o botão "Confirmar Data" no calendário de fim
    confirm_button_fim = tk.Button(root, text="Confirmar Data", command=lambda: confirmar_data_fim(calendario_fim, entry, confirm_button_fim))
    confirm_button_fim.place(x=400, y=230)


def confirmar_data_inicio(calendario, entry, confirm_button):
    global calendario_inicio, confirm_button_inicio
    data_inicio = calendario.get_date()

    # Habilita o campo para preenchê-lo
    entry.config(state="normal")
    entry.delete(0, tk.END)
    entry.insert(0, data_inicio)
    entry.config(state="disabled")  # Desabilita o campo novamente

    calendario.place_forget()  # Fecha o calendário de início
    confirm_button.place_forget()  # Fecha o botão "Confirmar Data"
    calendario_inicio = None  # Limpa a referência ao calendário
    confirm_button_inicio = None  # Limpa a referência ao botão

def confirmar_data_fim(calendario, entry, confirm_button):
    global calendario_fim, confirm_button_fim
    data_fim = calendario.get_date()

    # Habilita o campo para preenchê-lo
    entry.config(state="normal")
    entry.delete(0, tk.END)
    entry.insert(0, data_fim)
    entry.config(state="disabled")  # Desabilita o campo novamente

    calendario.place_forget()  # Fecha o calendário de início
    confirm_button.place_forget()  # Fecha o botão "Confirmar Data"
    calendario_fim = None  # Limpa a referência ao calendário
    confirm_button_fim = None  # Limpa a referência ao botão

def voltar_tela_inicial(root):
    for widget in root.winfo_children():
        widget.destroy()
    criar_tela_inicial(root)

def listar_projetos_com_status(root):
    for widget in root.winfo_children():
        widget.destroy()

    criar_tabela_projetos()

    projetos = listar_projetos()

    if len(projetos) == 0:
        messagebox.showinfo("Nenhum Projeto", "Nenhum projeto cadastrado!")
        voltar_tela_inicial(root)
    else:
        frame_lista_projetos = tk.Frame(root)
        frame_lista_projetos.pack(padx=10, pady=10)

        tk.Label(frame_lista_projetos, text="Lista de Projetos e Status:").grid(row=0, column=0, columnspan=3, pady=10)
        voltar_button = tk.Button(frame_lista_projetos, text="Voltar Tela Inicial", command=lambda: voltar_tela_inicial(root))
        voltar_button.grid(row=1, column=0, columnspan=3, pady=10)

        tk.Label(frame_lista_projetos, text="Projeto").grid(row=2, column=0, pady=5)
        tk.Label(frame_lista_projetos, text="Status Atual").grid(row=2, column=1, pady=5)

        for idx, projeto in enumerate(projetos, start=3):
            id_projeto, nome_projeto, status = projeto
            tk.Label(frame_lista_projetos, text=nome_projeto).grid(row=idx, column=0, pady=5)
            tk.Label(frame_lista_projetos, text=status).grid(row=idx, column=1, pady=5)

            alterar_status_button = tk.Button(frame_lista_projetos, text="Alterar Status do Projeto", command=lambda id=id_projeto: mostrar_status_projeto(root, id))
            alterar_status_button.grid(row=idx, column=2, pady=5)

            ver_status_tarefas_button = tk.Button(frame_lista_projetos, text="Ver Status Tarefas do Projeto", command=lambda id=id_projeto: listar_tarefas_por_projeto(root, id))
            ver_status_tarefas_button.grid(row=idx, column=3, pady=5)

            ver_status_melhorias_button = tk.Button(frame_lista_projetos, text="Ver Status Melhorias", command=lambda id=id_projeto: listar_melhorias_por_projeto(root, id))
            ver_status_melhorias_button.grid(row=idx, column=4, pady=5)

            ver_status_tarefas_melhorias_button = tk.Button(frame_lista_projetos, text="Ver Status Tarefas da Melhoria", command=lambda id=id_projeto: listar_tarefas_por_melhoria(root, id))
            ver_status_tarefas_melhorias_button.grid(row=idx, column=5, pady=5)

def mostrar_status_projeto(root, id_projeto):
    status_atual = obter_status_projeto(id_projeto)

    def salvar_novo_status():
        novo_status = status_combobox.get()
        atualizar_status_projeto(id_projeto, novo_status)
        messagebox.showinfo("Sucesso", "Status do projeto alterado com sucesso!")
        voltar_tela_inicial(root)

    janela_status = tk.Toplevel(root)
    janela_status.title("Alterar Status do Projeto")

    tk.Label(janela_status, text=f"Status Atual do Projeto: {status_atual}").pack(pady=10)

    status_combobox = ttk.Combobox(janela_status, values = [
        "Não iniciado (projeto aprovado, mas execução não começou)",
        "Em planejamento (em fase de escopo, cronograma ou orçamento)",
        "Em andamento (execução ativa e dentro do prazo)",
        "Em revisão (validação pela equipe ou stakeholders)",
        "Pausado (interrompido temporariamente - ex.: falta de recursos)",
        "Bloqueado (impedido por dependências externas)",
        "Em atraso (execução ativa, mas fora do prazo)",
        "Concluído (entregue e aceito formalmente)",
        "Cancelado (abandonado antes da conclusão)",
        "Entregue com pendências (concluído, mas com ajustes menores pendentes)"
    ],width=70, state="readonly")
    status_combobox.set(status_atual)
    status_combobox.pack(pady=10)

    tk.Button(janela_status, text="Salvar", command=salvar_novo_status).pack(pady=10)
    tk.Button(janela_status, text="Cancelar", command=janela_status.destroy).pack(pady=10)

def listar_tarefas_por_projeto(root, id_projeto):
    for widget in root.winfo_children():
        widget.destroy()

    criar_tabela_tarefas_projetos()

    conn = sqlite3.connect('gestao_projetos.db')
    cursor = conn.cursor()

    # Selecionar as tarefas relacionadas ao projeto
    cursor.execute("SELECT id, nome_tarefa, status_tarefa FROM tarefas_projetos WHERE id_projeto = ?", (id_projeto,))
    tarefas = cursor.fetchall()

    if len(tarefas) == 0:
        messagebox.showinfo("Nenhuma Tarefa", "Nenhuma tarefa cadastrada para este projeto.")
        voltar_tela_inicial(root)
    else:
        frame_lista_tarefas = tk.Frame(root)
        frame_lista_tarefas.pack(padx=10, pady=10)

        tk.Label(frame_lista_tarefas, text="Lista de Tarefas e Status:").grid(row=0, column=0, columnspan=3, pady=10)
        voltar_button = tk.Button(frame_lista_tarefas, text="Voltar a Lista de Projetos", command=lambda: listar_projetos_com_status(root))
        voltar_button.grid(row=1, column=0, columnspan=3, pady=10)

        tk.Label(frame_lista_tarefas, text="Tarefa").grid(row=2, column=0, pady=5)
        tk.Label(frame_lista_tarefas, text="Status Atual").grid(row=2, column=1, pady=5)

        for idx, tarefa in enumerate(tarefas, start=3):
            id_tarefa, nome_tarefa, status_tarefa = tarefa
            tk.Label(frame_lista_tarefas, text=nome_tarefa).grid(row=idx, column=0, pady=5)
            tk.Label(frame_lista_tarefas, text=status_tarefa).grid(row=idx, column=1, pady=5)

            # Botão para alterar o status da tarefa
            alterar_status_button = tk.Button(frame_lista_tarefas, text="Alterar Status", command=lambda id=id_tarefa, status=status_tarefa, proj_id=id_projeto: mostrar_status_tarefa_por_projeto(root, id, status, proj_id))
            alterar_status_button.grid(row=idx, column=2, pady=5)

    conn.close()

def mostrar_status_tarefa_por_projeto(root, id_tarefa, status_atual, id_projeto):
    def salvar_novo_status():
        novo_status = status_combobox.get()
        conn = sqlite3.connect('gestao_projetos.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE tarefas_projetos SET status_tarefa = ? WHERE id = ?", (novo_status, id_tarefa))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Status da tarefa alterado com sucesso!")
        listar_tarefas_por_projeto(root, id_projeto)  # Passando root como argumento

    janela_status = tk.Toplevel(root)
    janela_status.title("Alterar Status da Tarefa")

    tk.Label(janela_status, text="Selecione o novo status para a tarefa:").pack(pady=10)

    status_combobox = ttk.Combobox(janela_status, values=[
            "Não iniciada (aguardando dependência ou priorização)",
            "Em andamento (em execução ativa)",
            "Pausada (esperando info/recursos)",  # Diferente de "Pendente"
            "Bloqueada (impedida por problema externo)",  # Ex.: falta de aprovação
            "Concluída (validada e entregue)",
            "Cancelada (não será realizada)",
            "Pendente (aguardando revisão/validação)",  # Útil para checklists
            "Atrasada (fora do prazo planejado)"  # Destaque para gestão
        ],width=70, state="readonly")
    status_combobox.set(status_atual)  # Preenche o combobox com o status atual
    status_combobox.pack(pady=10)

    tk.Button(janela_status, text="Salvar", command=salvar_novo_status).pack(pady=10)
    tk.Button(janela_status, text="Cancelar", command=janela_status.destroy).pack(pady=10)

def listar_melhorias_por_projeto(root, id_projeto):
    for widget in root.winfo_children():
        widget.destroy()

    criar_tabela_melhorias()

    conn = sqlite3.connect('gestao_projetos.db')
    cursor = conn.cursor()

    # Selecionar as melhorias relacionadas ao projeto
    cursor.execute("SELECT id, nome_melhoria, status_melhoria FROM melhorias WHERE id_projeto = ?", (id_projeto,))
    melhorias = cursor.fetchall()

    if len(melhorias) == 0:
        messagebox.showinfo("Nenhuma Melhoria", "Nenhuma melhoria cadastrada para este projeto.")
        voltar_tela_inicial(root)
    else:
        frame_lista_melhorias = tk.Frame(root)
        frame_lista_melhorias.pack(padx=10, pady=10)

        tk.Label(frame_lista_melhorias, text="Lista de Melhorias e Status:").grid(row=0, column=0, columnspan=3, pady=10)
        voltar_button = tk.Button(frame_lista_melhorias, text="Voltar a Lista de Projetos", command=lambda: listar_projetos_com_status(root))
        voltar_button.grid(row=1, column=0, columnspan=3, pady=10)

        tk.Label(frame_lista_melhorias, text="Melhoria").grid(row=2, column=0, pady=5)
        tk.Label(frame_lista_melhorias, text="Status Atual").grid(row=2, column=1, pady=5)

        for idx, melhoria in enumerate(melhorias, start=3):
            id_melhoria, nome_melhoria, status_melhoria = melhoria
            tk.Label(frame_lista_melhorias, text=nome_melhoria).grid(row=idx, column=0, pady=5)
            tk.Label(frame_lista_melhorias, text=status_melhoria).grid(row=idx, column=1, pady=5)

            # Botão para alterar o status da melhoria
            alterar_status_button = tk.Button(frame_lista_melhorias, text="Alterar Status", command=lambda id=id_melhoria, status=status_melhoria, proj_id=id_projeto: mostrar_status_melhoria(root, id, status, proj_id))
            alterar_status_button.grid(row=idx, column=2, pady=5)

    conn.close()
    
def mostrar_status_melhoria(root, id_melhoria, status_atual, id_projeto):
    def salvar_novo_status():
        novo_status = status_combobox.get()
        conn = sqlite3.connect('gestao_projetos.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE melhorias SET status_melhoria = ? WHERE id = ?", (novo_status, id_melhoria))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Status da melhoria alterado com sucesso!")
        listar_melhorias_por_projeto(root, id_projeto)  # Passando root como argumento

    janela_status = tk.Toplevel(root)
    janela_status.title("Alterar Status da Melhorias")

    tk.Label(janela_status, text="Selecione o novo status para a melhoria:").pack(pady=10)

    status_combobox = ttk.Combobox(janela_status, values=[
        "Planejada (aprovada, aguardando alocação)",
        "Em desenvolvimento (em implementação ativa)",
        "Em revisão (testes/validação)",
        "Implementada (liberada em produção)", 
        "Adiada (priorizada para outro ciclo)",
        "Cancelada (não será implementada)",
        "Retrabalho (requer ajustes pós-implantação)"
    ],width=70, state="readonly")
    status_combobox.set(status_atual)  # Preenche o combobox com o status atual
    status_combobox.pack(pady=10)

    tk.Button(janela_status, text="Salvar", command=salvar_novo_status).pack(pady=10)
    tk.Button(janela_status, text="Cancelar", command=janela_status.destroy).pack(pady=10)

def listar_tarefas_por_melhoria(root, id_projeto):
    # Limpa a tela atual
    for widget in root.winfo_children():
        widget.destroy()

    # Conectar ao banco de dados
    conn = sqlite3.connect('gestao_projetos.db')
    cursor = conn.cursor()

    # Buscar melhorias relacionadas ao projeto
    cursor.execute("SELECT id, nome_melhoria FROM melhorias WHERE id_projeto = ?", (id_projeto,))
    melhorias = cursor.fetchall()

    if len(melhorias) == 0:
        # Se não houver melhorias, exibir mensagem e voltar à tela inicial
        messagebox.showinfo("Sem Melhorias", "Este projeto não possui melhorias cadastradas.")
        voltar_tela_inicial(root)
    else:
        # Criar o frame principal
        frame_principal = tk.Frame(root)
        frame_principal.pack(padx=10, pady=10)

        # Label e Combobox para selecionar a melhoria
        tk.Label(frame_principal, text="Selecione a Melhoria:").grid(row=0, column=0, pady=10)
        combo_melhorias = ttk.Combobox(frame_principal, state="readonly")
        combo_melhorias['values'] = [f"{melhoria[0]} - {melhoria[1]}" for melhoria in melhorias]
        combo_melhorias.grid(row=0, column=1, pady=10)
        combo_melhorias.current(0)  # Seleciona a primeira melhoria por padrão

        # Frame para exibir as tarefas
        frame_tarefas = tk.Frame(frame_principal)
        frame_tarefas.grid(row=1, column=0, columnspan=2, pady=10)

        def carregar_tarefas():
            # Limpa o frame de tarefas antes de carregar novas tarefas
            for widget in frame_tarefas.winfo_children():
                widget.destroy()

            # Conectar ao banco de dados
            conn = sqlite3.connect('gestao_projetos.db')
            cursor = conn.cursor()

            # Obter o ID da melhoria selecionada
            id_melhoria_selecionada = int(combo_melhorias.get().split(" - ")[0])

            # Buscar tarefas relacionadas à melhoria selecionada
            cursor.execute("SELECT id, nome_tarefa, status_tarefa FROM tarefas_melhorias WHERE id_melhoria = ?", (id_melhoria_selecionada,))
            tarefas = cursor.fetchall()

            conn.close()

            if len(tarefas) == 0:
                # Se não houver tarefas, exibir mensagem
                tk.Label(frame_tarefas, text="Nenhuma tarefa cadastrada para esta melhoria.").grid(row=0, column=0, pady=5)
            else:
                # Exibir as tarefas
                tk.Label(frame_tarefas, text="Tarefa").grid(row=0, column=0, pady=5)
                tk.Label(frame_tarefas, text="Status").grid(row=0, column=1, pady=5)

                for idx, tarefa in enumerate(tarefas, start=1):
                    id_tarefa, nome_tarefa, status_tarefa = tarefa
                    tk.Label(frame_tarefas, text=nome_tarefa).grid(row=idx, column=0, pady=5)
                    tk.Label(frame_tarefas, text=status_tarefa).grid(row=idx, column=1, pady=5)

                    # Botão para alterar o status da tarefa
                    alterar_status_button = tk.Button(frame_tarefas, text="Alterar Status", command=lambda id=id_tarefa, status=status_tarefa, melhor_id=id_melhoria_selecionada: mostrar_status_tarefa_por_melhoria(root, id, status, melhor_id))
                    alterar_status_button.grid(row=idx, column=2, pady=5)
            

        # Botão para carregar as tarefas da melhoria selecionada
        tk.Button(frame_principal, text="Carregar Tarefas", command=carregar_tarefas).grid(row=0, column=2, pady=10)

        # Botão para voltar à lista de projetos
        tk.Button(frame_principal, text="Voltar à Lista de Projetos", command=lambda: listar_projetos_com_status(root)).grid(row=2, column=0, columnspan=3, pady=10)

    conn.close()

def mostrar_status_tarefa_por_melhoria(root, id_tarefa, status_atual, id_melhoria):
    def salvar_novo_status():
        novo_status = status_combobox.get()
        conn = sqlite3.connect('gestao_projetos.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE tarefas_melhorias SET status_tarefa = ? WHERE id = ?", (novo_status, id_tarefa))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Status da tarefa alterado com sucesso!")
        listar_tarefas_por_melhoria(root, id_melhoria)  # Passando root como argumento

    janela_status = tk.Toplevel(root)
    janela_status.title("Alterar Status da Tarefa")

    tk.Label(janela_status, text="Selecione o novo status para a tarefa:").pack(pady=10)

    status_combobox = ttk.Combobox(janela_status, values=[
            "Não iniciada (aguardando dependência ou priorização)",
            "Em andamento (em execução ativa)",
            "Pausada (esperando info/recursos)",  # Diferente de "Pendente"
            "Bloqueada (impedida por problema externo)",  # Ex.: falta de aprovação
            "Concluída (validada e entregue)",
            "Cancelada (não será realizada)",
            "Pendente (aguardando revisão/validação)",  # Útil para checklists
            "Atrasada (fora do prazo planejado)"  # Destaque para gestão
        ],width=70, state="readonly")
    status_combobox.set(status_atual)  # Preenche o combobox com o status atual
    status_combobox.pack(pady=10)

    tk.Button(janela_status, text="Salvar", command=salvar_novo_status).pack(pady=10)
    tk.Button(janela_status, text="Cancelar", command=janela_status.destroy).pack(pady=10)


def criar_tela_projeto_existente(root):
    for widget in root.winfo_children():
        widget.destroy()

    criar_tabela_projetos()

    projetos = listar_projetos()

    if len(projetos) == 0:
        messagebox.showinfo("Nenhum Projeto", "Nenhum projeto cadastrado!")
        voltar_tela_inicial(root)
    else:
        frame_projeto = tk.Frame(root)
        frame_projeto.pack(padx=10, pady=10)

        tk.Label(frame_projeto, text="Selecione um Projeto:").grid(row=0, column=0, columnspan=2, pady=10)

        # Criando o ComboBox para selecionar o projeto
        # lista_nomes_projetos = [nome_projeto for _, nome_projeto in projetos]
        lista_nomes_projetos = [nome_projeto for _, nome_projeto, *_ in projetos]
        combo_projetos = ttk.Combobox(frame_projeto, values=lista_nomes_projetos, state="readonly")
        combo_projetos.grid(row=1, column=0, columnspan=2, pady=5)

        # Função para abrir o projeto selecionado
        def selecionar_projeto():
            projeto_selecionado = combo_projetos.get()
            if projeto_selecionado:
                # Obter o ID do projeto selecionado
                id_projeto = next(id for id, nome, *_ in projetos if nome == projeto_selecionado)
                abrir_tela_projeto(root, id_projeto)
            else:
                messagebox.showwarning("Seleção Inválida", "Selecione um projeto da lista.")

        # Botão para selecionar o projeto
        botao_selecionar = tk.Button(frame_projeto, text="Selecionar", command=selecionar_projeto)
        botao_selecionar.grid(row=2, column=0, columnspan=2, pady=10)

        voltar_button = tk.Button(frame_projeto, text="Voltar Tela Inicial", command=lambda: voltar_tela_inicial(root))
        voltar_button.grid(row=3, column=0, columnspan=2, pady=10)



def obter_status_projeto(id_projeto):
    conn = sqlite3.connect('gestao_projetos.db')
    cursor = conn.cursor()
    cursor.execute("SELECT status_projeto FROM projetos WHERE id = ?", (id_projeto,))
    status = cursor.fetchone()[0]
    conn.close()
    return status

def obter_status_tarefa_por_projeto(id_tarefa):
    conn = sqlite3.connect('gestao_projetos.db')
    cursor = conn.cursor()
    cursor.execute("SELECT status_tarefa FROM tarefas_projetos WHERE id = ?", (id_tarefa,))
    status = cursor.fetchone()[0]
    conn.close()
    return status

def abrir_tela_projeto(root, id_projeto):
    for widget in root.winfo_children():
        widget.destroy()

    frame_projeto = tk.Frame(root)
    frame_projeto.pack(padx=10, pady=10)

    tk.Label(frame_projeto, text="Projeto Selecionado").grid(row=0, column=0, pady=10)

    add_task_button = tk.Button(frame_projeto, text="Adicionar Tarefa", command=lambda: adicionar_tarefa(root, id_projeto))
    add_task_button.grid(row=1, column=0, pady=5)

    add_improvement_button = tk.Button(frame_projeto, text="Adicionar Melhoria", command=lambda: adicionar_melhoria(root, id_projeto))
    add_improvement_button.grid(row=2, column=0, pady=5)

    add_deadline_button = tk.Button(frame_projeto, text="Editar Prazos", command=lambda: editar_prazos(root, id_projeto))
    add_deadline_button.grid(row=3, column=0, pady=5)

    add_involved_button = tk.Button(frame_projeto, text="Adicionar Envolvido", 
                              command=lambda: adicionar_envolvido(root, id_projeto))
    add_involved_button.grid(row=4, column=0, pady=5)

    status_button = tk.Button(frame_projeto, text="Status do Projeto", command=lambda: mostrar_status_projeto(root, id_projeto))
    status_button.grid(row=5, column=0, pady=5)

    ver_status_tarefas_button = tk.Button(frame_projeto, text="Lista de Tarefas do Projeto", command=lambda: listar_tarefas_por_projeto(root, id_projeto))
    ver_status_tarefas_button.grid(row=6, column=0, pady=5)

    voltar_button = tk.Button(frame_projeto, text="Voltar Tela Inicial", command=lambda: voltar_tela_inicial(root))
    voltar_button.grid(row=7, column=0, pady=10)

def adicionar_tarefa(root, id_projeto):
    # Verifica o status do projeto
    conn = sqlite3.connect('gestao_projetos.db')
    cursor = conn.cursor()

    cursor.execute("SELECT status_projeto FROM projetos WHERE id = ?", (id_projeto,))
    status_projeto = cursor.fetchone()[0]

    if status_projeto == "Concluído (entregue e aceito formalmente)":
        # Se o projeto for "Concluído", abre a tela para selecionar uma melhoria
        try:
            cursor.execute("SELECT id, nome_melhoria FROM melhorias WHERE id_projeto = ? AND status_melhoria = 'Em desenvolvimento (em implementação ativa)'", (id_projeto,))
            melhorias = cursor.fetchall()

            if not melhorias:
                messagebox.showwarning("Nenhuma melhoria em desenvolvimento", "Não há melhorias em desenvolvimento para associar a uma tarefa.")
                conn.close()
                return

            for widget in root.winfo_children():
                widget.destroy()
        except Exception as e:
            messagebox.showwarning("Nenhuma melhoria em desenvolvimento", "Não há melhorias em desenvolvimento para associar a uma tarefa.")
            conn.close()
            return

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
        data_inicio_tarefa_entry = tk.Entry(frame_tarefa, state="disabled")
        data_inicio_tarefa_entry.grid(row=4, column=1, pady=5)

        # Botão para abrir o calendário de início
        data_inicio_tarefa_button = tk.Button(frame_tarefa, text="Escolher Data", command=lambda: abrir_calendario_inicio(root, data_inicio_tarefa_entry))
        data_inicio_tarefa_button.grid(row=4, column=2, pady=5)

        tk.Label(frame_tarefa, text="Data de Término:").grid(row=5, column=0, sticky="e")
        data_termino_tarefa_entry = tk.Entry(frame_tarefa, state="disabled")
        data_termino_tarefa_entry.grid(row=5, column=1, pady=5)

        # Botão para abrir o calendário de término
        data_fim_tarefa_button = tk.Button(frame_tarefa, text="Escolher Data", command=lambda: abrir_calendario_fim(root, data_termino_tarefa_entry))
        data_fim_tarefa_button.grid(row=5, column=2, pady=5)

        tk.Label(frame_tarefa, text="Prioridade:").grid(row=6, column=0, pady=5)
        prioridade_combobox = ttk.Combobox(frame_tarefa, values= [
            "Urgente 🔴 (prazo ≤ 24h ou bloqueia outras tarefas)",
            "Alta ⚠️ (prazo ≤ 3 dias ou impacto direto no projeto)",
            "Média 🔵 (prazo ≤ 1 semana)",
            "Baixa ⚪ (sem urgência, pode ser reagendada)"
        ])
        prioridade_combobox.grid(row=6, column=1, pady=5)

        tk.Label(frame_tarefa, text="Status:").grid(row=7, column=0, pady=5)
        status_combobox = ttk.Combobox(frame_tarefa, values=[
            "Não iniciada (aguardando dependência ou priorização)",
            "Em andamento (em execução ativa)",
            "Pausada (esperando info/recursos)",  # Diferente de "Pendente"
            "Bloqueada (impedida por problema externo)",  # Ex.: falta de aprovação
            "Concluída (validada e entregue)",
            "Cancelada (não será realizada)",
            "Pendente (aguardando revisão/validação)",  # Útil para checklists
            "Atrasada (fora do prazo planejado)"  # Destaque para gestão
        ],width=70)
        status_combobox.grid(row=7, column=1, pady=5)



        # Função para salvar a tarefa
        def salvar_tarefa():
            criar_tabela_tarefas_melhorias()

            id_melhoria = melhoria_combobox.get()
            nome_tarefa = nome_tarefa_entry.get()
            descricao_tarefa = descricao_tarefa_entry.get()
            data_inicio_tarefa = data_inicio_tarefa_entry.get()
            data_termino_tarefa = data_termino_tarefa_entry.get()
            prioridade = prioridade_combobox.get()
            status = status_combobox.get()

            # Buscar o ID da melhoria selecionada
            cursor.execute("SELECT id FROM melhorias WHERE nome_melhoria = ? AND id_projeto = ?", (id_melhoria, id_projeto))
            id_melhoria_selected = cursor.fetchone()[0]

            cursor.execute("INSERT INTO tarefas_melhorias (id_melhoria, nome_tarefa, descricao_tarefa, data_inicio_tarefa, data_termino_tarefa, prioridade_tarefa, status_tarefa) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (id_melhoria_selected, nome_tarefa, descricao_tarefa, data_inicio_tarefa, data_termino_tarefa, prioridade, status))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Tarefa associada à melhoria com sucesso!")
            voltar_tela_inicial(root)

        salvar_button = tk.Button(frame_tarefa, text="Salvar", command=salvar_tarefa)
        salvar_button.grid(row=9, column=1, pady=10)

        voltar_button = tk.Button(frame_tarefa, text="Voltar", command=lambda: voltar_tela_inicial(root))
        voltar_button.grid(row=10, column=1, pady=10)

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
        data_inicio_tarefa_entry = tk.Entry(frame_tarefa, state="disabled")
        data_inicio_tarefa_entry.grid(row=3, column=1, pady=5)

        # Botão para abrir o calendário de início
        data_inicio_tarefa_button = tk.Button(frame_tarefa, text="Escolher Data", command=lambda: abrir_calendario_inicio(root, data_inicio_tarefa_entry))
        data_inicio_tarefa_button.grid(row=3, column=2, pady=5)

        tk.Label(frame_tarefa, text="Data de Término:").grid(row=4, column=0, sticky="e")
        data_termino_tarefa_entry = tk.Entry(frame_tarefa, state="disabled")
        data_termino_tarefa_entry.grid(row=4, column=1, pady=5)

        # Botão para abrir o calendário de término
        data_fim_tarefa_button = tk.Button(frame_tarefa, text="Escolher Data", command=lambda: abrir_calendario_fim(root, data_termino_tarefa_entry))
        data_fim_tarefa_button.grid(row=4, column=2, pady=5)

        tk.Label(frame_tarefa, text="Prioridade:").grid(row=5, column=0, pady=5)
        prioridade_combobox = ttk.Combobox(frame_tarefa, values= [
            "Urgente 🔴 (prazo ≤ 24h ou bloqueia outras tarefas)",
            "Alta ⚠️ (prazo ≤ 3 dias ou impacto direto no projeto)",
            "Média 🔵 (prazo ≤ 1 semana)",
            "Baixa ⚪ (sem urgência, pode ser reagendada)"
        ],width=70)
        prioridade_combobox.grid(row=5, column=1, pady=5)

        tk.Label(frame_tarefa, text="Status:").grid(row=6, column=0, pady=5)
        status_combobox = ttk.Combobox(frame_tarefa, values=[
            "Não iniciada (aguardando dependência ou priorização)",
            "Em andamento (em execução ativa)",
            "Pausada (esperando info/recursos)",  # Diferente de "Pendente"
            "Bloqueada (impedida por problema externo)",  # Ex.: falta de aprovação
            "Concluída (validada e entregue)",
            "Cancelada (não será realizada)",
            "Pendente (aguardando revisão/validação)",  # Útil para checklists
            "Atrasada (fora do prazo planejado)"  # Destaque para gestão
        ],width=70)
        status_combobox.grid(row=6, column=1, pady=5)


        # Função para salvar a tarefa
        def salvar_tarefa():
            criar_tabela_tarefas_projetos()

            nome_tarefa = nome_tarefa_entry.get()
            descricao_tarefa = descricao_tarefa_entry.get()
            data_inicio_tarefa = data_inicio_tarefa_entry.get()
            data_termino_tarefa = data_termino_tarefa_entry.get()
            prioridade = prioridade_combobox.get()
            status = status_combobox.get()

            cursor.execute("INSERT INTO tarefas_projetos (id_projeto, nome_tarefa, descricao_tarefa, data_inicio_tarefa, data_termino_tarefa, prioridade_tarefa, status_tarefa) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (id_projeto, nome_tarefa, descricao_tarefa, data_inicio_tarefa, data_termino_tarefa, prioridade, status))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso!")
            voltar_tela_inicial(root)

        salvar_button = tk.Button(frame_tarefa, text="Salvar", command=salvar_tarefa)
        salvar_button.grid(row=8, column=1, pady=10)

        voltar_button = tk.Button(frame_tarefa, text="Voltar", command=lambda: voltar_tela_inicial(root))
        voltar_button.grid(row=9, column=1, pady=10)

def adicionar_melhoria(root, id_projeto):
    # Verifica o status do projeto
    conn = sqlite3.connect('gestao_projetos.db')
    cursor = conn.cursor()

    cursor.execute("SELECT status_projeto FROM projetos WHERE id = ?", (id_projeto,))
    status_projeto = cursor.fetchone()[0]

    if status_projeto != "Concluído (entregue e aceito formalmente)":
        messagebox.showwarning(
            "Status do Projeto",
            f"O status atual do projeto é '{status_projeto}'.\n"
            "Você só pode adicionar melhorias se o projeto estiver com o status 'Concluído (entregue e aceito formalmente)'."
        )
        conn.close()
        return

    # Se o status for "Concluído", abre a tela para adicionar a melhoria
    for widget in root.winfo_children():
        widget.destroy()

    frame_melhoria = tk.Frame(root)
    frame_melhoria.pack(padx=10, pady=10)

    tk.Label(frame_melhoria, text="Adicionar Melhoria ao Projeto").grid(row=0, column=0, pady=10)

    # Campos para adicionar melhoria
    tk.Label(frame_melhoria, text="Nome da Melhoria:").grid(row=1, column=0, pady=5)
    nome_entry = tk.Entry(frame_melhoria)
    nome_entry.grid(row=1, column=1, pady=5)

    tk.Label(frame_melhoria, text="Descrição da Melhoria:").grid(row=2, column=0, pady=5)
    descricao_entry = tk.Entry(frame_melhoria)
    descricao_entry.grid(row=2, column=1, pady=5)

    tk.Label(frame_melhoria, text="Status da Melhoria:").grid(row=3, column=0, pady=5)
    status_combobox = ttk.Combobox(frame_melhoria, values=[
        "Planejada (aprovada, aguardando alocação)",
        "Em desenvolvimento (em implementação ativa)",
        "Em revisão (testes/validação)",
        "Implementada (liberada em produção)", 
        "Adiada (priorizada para outro ciclo)",
        "Cancelada (não será implementada)",
        "Retrabalho (requer ajustes pós-implantação)"
    ],width=70)
    status_combobox.grid(row=3, column=1, pady=5)

    tk.Label(frame_melhoria, text="Impacto da Melhoria:").grid(row=4, column=0, pady=5)
    impacto_combobox = ttk.Combobox(frame_melhoria, values=[
        "Crítica 🔴 (resolve problema operacional urgente)",
        "Alta ⚠️ (impacta KPIs estratégicos)",
        "Média 🔵 (incremento de eficiência)",
        "Baixa ⚪ (melhoria cosmética)"
    ],width=70)
    impacto_combobox.grid(row=4, column=1, pady=5)

    tk.Label(frame_melhoria, text="Data Início:").grid(row=5, column=0, pady=5)
    data_inicio_entry = tk.Entry(frame_melhoria, state="disabled")
    data_inicio_entry.grid(row=5, column=1, pady=5)

    # Botão para abrir o calendário de início
    data_inicio_tarefa_button = tk.Button(frame_melhoria, text="Escolher Data", command=lambda: abrir_calendario_inicio(root, data_inicio_entry))
    data_inicio_tarefa_button.grid(row=5, column=2, pady=5)

    tk.Label(frame_melhoria, text="Data Término:").grid(row=6, column=0, pady=5)
    data_termino_entry = tk.Entry(frame_melhoria, state="disabled")
    data_termino_entry.grid(row=6, column=1, pady=5)

    # Botão para abrir o calendário de término
    data_fim_tarefa_button = tk.Button(frame_melhoria, text="Escolher Data", command=lambda: abrir_calendario_fim(root, data_termino_entry))
    data_fim_tarefa_button.grid(row=6, column=2, pady=5)

    # Função para salvar a melhoria no banco de dados
    def salvar_melhoria():
        criar_tabela_melhorias()
        nome = nome_entry.get()
        descricao = descricao_entry.get()
        status = status_combobox.get()
        impacto = impacto_combobox.get()
        data_inicio = data_inicio_entry.get()
        data_termino = data_termino_entry.get()

        cursor.execute("INSERT INTO melhorias (id_projeto, nome_melhoria, descricao_melhoria, impacto_melhoria, data_inicio_melhoria, data_termino_melhoria, status_melhoria) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (id_projeto, nome, descricao, impacto, data_inicio, data_termino, status))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Melhoria adicionada com sucesso!")
        voltar_tela_inicial(root)

    salvar_button = tk.Button(frame_melhoria, text="Salvar", command=salvar_melhoria)
    salvar_button.grid(row=7, column=1, pady=10)

    voltar_button = tk.Button(frame_melhoria, text="Voltar", command=lambda: voltar_tela_inicial(root))
    voltar_button.grid(row=8, column=1, pady=10)

def editar_prazos(root, id_projeto):
    # Janela de seleção do tipo de prazo a editar
    janela_selecao = tk.Toplevel(root)
    janela_selecao.title("Editar Prazos")
    janela_selecao.geometry("400x300")

    tk.Label(janela_selecao, text="Selecione o que deseja editar:").pack(pady=20)

    # Funções para cada tipo de edição
    def editar_projeto():
        conn = sqlite3.connect('gestao_projetos.db')
        cursor = conn.cursor()
        cursor.execute("SELECT status_projeto FROM projetos WHERE id = ?", (id_projeto,))
        status = cursor.fetchone()[0]
        conn.close()

        if status == "Concluído (entregue e aceito formalmente)":
            messagebox.showwarning("Edição Bloqueada", "Projetos concluídos não podem ter alteração de prazo.")
            janela_selecao.destroy()
            return

        janela_datas = tk.Toplevel(root)
        janela_datas.geometry("800x500")
        janela_datas.title("Editar Prazos do Projeto")
        # janela_datas.grab_set()  # Modal (bloqueia interação com a janela principal)
        
        # Variáveis para armazenar as datas
        data_inicio = tk.StringVar()
        data_termino = tk.StringVar()

        tk.Label(janela_datas, text="Nova Data de Início:").pack(pady=5)
        entry_inicio = tk.Entry(janela_datas, textvariable=data_inicio, state='disabled')
        entry_inicio.pack(pady=5)
        tk.Button(janela_datas, text="Selecionar Data", 
                 command=lambda: abrir_calendario_inicio(janela_datas, entry_inicio)).pack(pady=5)

        tk.Label(janela_datas, text="Nova Data de Término:").pack(pady=5)
        entry_termino = tk.Entry(janela_datas, textvariable=data_termino, state='disabled')
        entry_termino.pack(pady=5)
        tk.Button(janela_datas, text="Selecionar Data", 
                 command=lambda: abrir_calendario_fim(janela_datas, entry_termino)).pack(pady=5)

        def salvar_datas():
            if not data_inicio.get() or not data_termino.get():
                messagebox.showwarning("Campos obrigatórios", "Selecione ambas as datas.")
                return

            conn = sqlite3.connect('gestao_projetos.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE projetos SET data_inicio = ?, data_fim = ? WHERE id = ?",
                          (data_inicio.get(), data_termino.get(), id_projeto))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Prazos do projeto atualizados com sucesso!")
            janela_datas.destroy()
            janela_selecao.destroy()

        tk.Button(janela_datas, text="Salvar", command=salvar_datas).pack(pady=20)

    def editar_tarefas_projeto():
        conn = sqlite3.connect('gestao_projetos.db')
        cursor = conn.cursor()
        
        # Buscar tarefas não concluídas
        cursor.execute("SELECT id, nome_tarefa FROM tarefas_projetos WHERE id_projeto = ? AND status_tarefa != 'Concluída (validada e entregue)'", (id_projeto,))
        tarefas = cursor.fetchall()
        
        if not tarefas:
            cursor.execute("SELECT COUNT(*) FROM tarefas_projetos WHERE id_projeto = ?", (id_projeto,))
            if cursor.fetchone()[0] == 0:
                messagebox.showinfo("Sem Tarefas", "Este projeto não possui tarefas cadastradas.")
            else:
                messagebox.showinfo("Tarefas Concluídas", "Todas as tarefas deste projeto já estão concluídas e não podem ter prazos alterados.")
            conn.close()
            janela_selecao.destroy()
            return
        
        janela_tarefas = tk.Toplevel(root)
        janela_tarefas.title("Selecionar Tarefa")
        
        tk.Label(janela_tarefas, text="Selecione a tarefa:").pack(pady=10)
        
        combo_tarefas = ttk.Combobox(janela_tarefas, values=[f"{t[0]} - {t[1]}" for t in tarefas])
        combo_tarefas.pack(pady=10)
        combo_tarefas.current(0)
        
        def abrir_edicao_tarefa():
            id_tarefa = int(combo_tarefas.get().split(" - ")[0])
            
            janela_datas = tk.Toplevel(root)
            janela_datas.geometry("800x500")
            janela_datas.title("Editar Prazos da Tarefa")
            
            # Variáveis para armazenar as datas
            data_inicio = tk.StringVar()
            data_termino = tk.StringVar()

            tk.Label(janela_datas, text="Nova Data de Início:").pack(pady=5)
            entry_inicio = tk.Entry(janela_datas, textvariable=data_inicio, state='disabled')
            entry_inicio.pack(pady=5)
            tk.Button(janela_datas, text="Selecionar Data", 
                     command=lambda: abrir_calendario_inicio(janela_datas, entry_inicio)).pack(pady=5)

            tk.Label(janela_datas, text="Nova Data de Término:").pack(pady=5)
            entry_termino = tk.Entry(janela_datas, textvariable=data_termino, state='disabled')
            entry_termino.pack(pady=5)
            tk.Button(janela_datas, text="Selecionar Data", 
                     command=lambda: abrir_calendario_fim(janela_datas, entry_termino)).pack(pady=5)

            def salvar_datas_tarefa():
                if not data_inicio.get() or not data_termino.get():
                    messagebox.showwarning("Campos obrigatórios", "Selecione ambas as datas.")
                    return

                conn = sqlite3.connect('gestao_projetos.db')
                cursor = conn.cursor()
                cursor.execute("UPDATE tarefas_projetos SET data_inicio_tarefa = ?, data_termino_tarefa = ? WHERE id = ?",
                             (data_inicio.get(), data_termino.get(), id_tarefa))
                conn.commit()
                conn.close()
                messagebox.showinfo("Sucesso", "Prazos da tarefa atualizados com sucesso!")
                janela_datas.destroy()
                janela_tarefas.destroy()
                janela_selecao.destroy()

            tk.Button(janela_datas, text="Salvar", command=salvar_datas_tarefa).pack(pady=20)
        
        tk.Button(janela_tarefas, text="Continuar", command=abrir_edicao_tarefa).pack(pady=20)
        conn.close()

    def editar_melhorias():
        conn = sqlite3.connect('gestao_projetos.db')
        cursor = conn.cursor()
        
        # Verificar se existem melhorias
        cursor.execute("SELECT COUNT(*) FROM melhorias WHERE id_projeto = ?", (id_projeto,))
        if cursor.fetchone()[0] == 0:
            messagebox.showinfo("Sem Melhorias", "Este projeto não possui melhorias cadastradas.")
            conn.close()
            janela_selecao.destroy()
            return
        
        # Buscar melhorias não implementadas
        cursor.execute("SELECT id, nome_melhoria FROM melhorias WHERE id_projeto = ? AND status_melhoria != 'Implementada (liberada em produção)'", (id_projeto,))
        melhorias = cursor.fetchall()
        
        if not melhorias:
            messagebox.showinfo("Melhorias Implementadas", "Todas as melhorias deste projeto já estão implementadas e não podem ter prazos alterados.")
            conn.close()
            janela_selecao.destroy()
            return
        
        janela_melhorias = tk.Toplevel(root)
        janela_melhorias.title("Selecionar Melhoria")
        
        tk.Label(janela_melhorias, text="Selecione a melhoria:").pack(pady=10)
        
        combo_melhorias = ttk.Combobox(janela_melhorias, values=[f"{m[0]} - {m[1]}" for m in melhorias])
        combo_melhorias.pack(pady=10)
        combo_melhorias.current(0)
        
        def abrir_edicao_melhoria():
            id_melhoria = int(combo_melhorias.get().split(" - ")[0])
            
            janela_datas = tk.Toplevel(root)
            janela_datas.geometry("800x500")
            janela_datas.title("Editar Prazos da Melhoria")
            
            # Variáveis para armazenar as datas
            data_inicio = tk.StringVar()
            data_termino = tk.StringVar()

            tk.Label(janela_datas, text="Nova Data de Início:").pack(pady=5)
            entry_inicio = tk.Entry(janela_datas, textvariable=data_inicio, state='disabled')
            entry_inicio.pack(pady=5)
            tk.Button(janela_datas, text="Selecionar Data", 
                     command=lambda: abrir_calendario_inicio(janela_datas, entry_inicio)).pack(pady=5)

            tk.Label(janela_datas, text="Nova Data de Término:").pack(pady=5)
            entry_termino = tk.Entry(janela_datas, textvariable=data_termino, state='disabled')
            entry_termino.pack(pady=5)
            tk.Button(janela_datas, text="Selecionar Data", 
                     command=lambda: abrir_calendario_fim(janela_datas, entry_termino)).pack(pady=5)

            def salvar_datas_melhoria():
                if not data_inicio.get() or not data_termino.get():
                    messagebox.showwarning("Campos obrigatórios", "Selecione ambas as datas.")
                    return

                conn = sqlite3.connect('gestao_projetos.db')
                cursor = conn.cursor()
                cursor.execute("UPDATE melhorias SET data_inicio_melhoria = ?, data_termino_melhoria = ? WHERE id = ?",
                             (data_inicio.get(), data_termino.get(), id_melhoria))
                conn.commit()
                conn.close()
                messagebox.showinfo("Sucesso", "Prazos da melhoria atualizados com sucesso!")
                janela_datas.destroy()
                janela_melhorias.destroy()
                janela_selecao.destroy()

            tk.Button(janela_datas, text="Salvar", command=salvar_datas_melhoria).pack(pady=20)
        
        tk.Button(janela_melhorias, text="Continuar", command=abrir_edicao_melhoria).pack(pady=20)
        conn.close()

    def editar_tarefas_melhorias():
        conn = sqlite3.connect('gestao_projetos.db')
        cursor = conn.cursor()
        
        # Verificar se existem melhorias com tarefas
        cursor.execute('''
            SELECT COUNT(*) FROM tarefas_melhorias tm
            JOIN melhorias m ON tm.id_melhoria = m.id
            WHERE m.id_projeto = ?
        ''', (id_projeto,))
        
        if cursor.fetchone()[0] == 0:
            messagebox.showinfo("Sem Tarefas", "Este projeto não possui tarefas de melhorias cadastradas.")
            conn.close()
            janela_selecao.destroy()
            return
        
        # Buscar tarefas não concluídas
        cursor.execute('''
            SELECT tm.id, tm.nome_tarefa 
            FROM tarefas_melhorias tm
            JOIN melhorias m ON tm.id_melhoria = m.id
            WHERE m.id_projeto = ? AND tm.status_tarefa != 'Concluída (validada e entregue)'
        ''', (id_projeto,))
        
        tarefas = cursor.fetchall()
        
        if not tarefas:
            messagebox.showinfo("Tarefas Concluídas", "Todas as tarefas de melhorias deste projeto já estão concluídas e não podem ter prazos alterados.")
            conn.close()
            janela_selecao.destroy()
            return
        
        janela_tarefas = tk.Toplevel(root)
        janela_tarefas.title("Selecionar Tarefa de Melhoria")
        
        tk.Label(janela_tarefas, text="Selecione a tarefa:").pack(pady=10)
        
        combo_tarefas = ttk.Combobox(janela_tarefas, values=[f"{t[0]} - {t[1]}" for t in tarefas])
        combo_tarefas.pack(pady=10)
        combo_tarefas.current(0)
        
        def abrir_edicao_tarefa_melhoria():
            id_tarefa = int(combo_tarefas.get().split(" - ")[0])
            
            janela_datas = tk.Toplevel(root)
            janela_datas.geometry("800x500")
            janela_datas.title("Editar Prazos da Tarefa de Melhoria")
            
            # Variáveis para armazenar as datas
            data_inicio = tk.StringVar()
            data_termino = tk.StringVar()

            tk.Label(janela_datas, text="Nova Data de Início:").pack(pady=5)
            entry_inicio = tk.Entry(janela_datas, textvariable=data_inicio, state='disabled')
            entry_inicio.pack(pady=5)
            tk.Button(janela_datas, text="Selecionar Data", 
                     command=lambda: abrir_calendario_inicio(janela_datas, entry_inicio)).pack(pady=5)

            tk.Label(janela_datas, text="Nova Data de Término:").pack(pady=5)
            entry_termino = tk.Entry(janela_datas, textvariable=data_termino, state='disabled')
            entry_termino.pack(pady=5)
            tk.Button(janela_datas, text="Selecionar Data", 
                     command=lambda: abrir_calendario_fim(janela_datas, entry_termino)).pack(pady=5)

            def salvar_datas_tarefa():
                if not data_inicio.get() or not data_termino.get():
                    messagebox.showwarning("Campos obrigatórios", "Selecione ambas as datas.")
                    return

                conn = sqlite3.connect('gestao_projetos.db')
                cursor = conn.cursor()
                cursor.execute("UPDATE tarefas_melhorias SET data_inicio_tarefa = ?, data_termino_tarefa = ? WHERE id = ?",
                             (data_inicio.get(), data_termino.get(), id_tarefa))
                conn.commit()
                conn.close()
                messagebox.showinfo("Sucesso", "Prazos da tarefa de melhoria atualizados com sucesso!")
                janela_datas.destroy()
                janela_tarefas.destroy()
                janela_selecao.destroy()

            tk.Button(janela_datas, text="Salvar", command=salvar_datas_tarefa).pack(pady=20)
        
        tk.Button(janela_tarefas, text="Continuar", command=abrir_edicao_tarefa_melhoria).pack(pady=20)
        conn.close()

    # Botões para cada opção
    tk.Button(janela_selecao, text="Projeto", command=editar_projeto, width=20).pack(pady=10)
    tk.Button(janela_selecao, text="Tarefas do Projeto", command=editar_tarefas_projeto, width=20).pack(pady=10)
    tk.Button(janela_selecao, text="Melhoria", command=editar_melhorias, width=20).pack(pady=10)
    tk.Button(janela_selecao, text="Tarefas da Melhoria", command=editar_tarefas_melhorias, width=20).pack(pady=10)

# gui.py - função adicionar_envolvido atualizada
def adicionar_envolvido(root, id_projeto):
    # Fecha janela anterior
    for widget in root.winfo_children():
        widget.destroy()

    criar_tabela_envolvidos()

    # Container principal com scrollbar
    main_container = tk.Frame(root)
    main_container.pack(fill='both', expand=True)

    # Canvas e Scrollbar
    canvas = tk.Canvas(main_container)
    scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    # Configuração do scroll
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Layout dos elementos de scroll
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Frame principal dentro da área rolável
    frame_principal = tk.Frame(scrollable_frame)
    frame_principal.pack(fill='both', expand=True, padx=10, pady=10)

    # --- Frame de Seleção do Tipo ---
    frame_selecao = tk.LabelFrame(frame_principal, text="Onde adicionar o envolvido?", padx=10, pady=10)
    frame_selecao.pack(fill='x', pady=10)

    tipo_selecionado = tk.StringVar(value="projeto")

    # Radio buttons
    rb_projeto = tk.Radiobutton(frame_selecao, text="No Projeto", variable=tipo_selecionado, 
                               value="projeto")
    rb_projeto.grid(row=0, column=0, sticky="w", padx=5)
    
    rb_tarefa = tk.Radiobutton(frame_selecao, text="Em Tarefa", variable=tipo_selecionado, 
                              value="tarefa")
    rb_tarefa.grid(row=0, column=1, sticky="w", padx=5)
    
    rb_melhoria = tk.Radiobutton(frame_selecao, text="Em Melhoria", variable=tipo_selecionado, 
                                value="melhoria")
    rb_melhoria.grid(row=0, column=2, sticky="w", padx=5)
    
    rb_tarefa_melhoria = tk.Radiobutton(frame_selecao, text="Em Tarefa de Melhoria", variable=tipo_selecionado, 
                                       value="tarefa_melhoria")
    rb_tarefa_melhoria.grid(row=0, column=3, sticky="w", padx=5)

    # --- Frame para seleção específica ---
    frame_selecao_especifica = tk.Frame(frame_principal)
    frame_selecao_especifica.pack(fill='x', pady=5)

    combo_tarefas_var = tk.StringVar()
    combo_melhorias_var = tk.StringVar()
    combo_tarefas_melhorias_var = tk.StringVar()

    label_tarefas = tk.Label(frame_selecao_especifica, text="Selecione a Tarefa:")
    combo_tarefas = ttk.Combobox(frame_selecao_especifica, textvariable=combo_tarefas_var, state="readonly")

    label_melhorias = tk.Label(frame_selecao_especifica, text="Selecione a Melhoria:")
    combo_melhorias = ttk.Combobox(frame_selecao_especifica, textvariable=combo_melhorias_var, state="readonly")

    label_tarefas_melhorias = tk.Label(frame_selecao_especifica, text="Selecione a Tarefa de Melhoria:")
    combo_tarefas_melhorias = ttk.Combobox(frame_selecao_especifica, textvariable=combo_tarefas_melhorias_var, state="readonly")

    # Combobox para reaproveitar
    frame_reaproveitar = tk.Frame(frame_principal)
    frame_reaproveitar.pack(fill='x', pady=5)
    
    tk.Label(frame_reaproveitar, text="Reaproveitar envolvido:").pack(side='left')
    combo_envolvidos_existentes = ttk.Combobox(frame_reaproveitar, state="readonly", width=30)
    combo_envolvidos_existentes.pack(side='left', padx=5, fill='x', expand=True)
    btn_carregar = tk.Button(frame_reaproveitar, text="Carregar")
    btn_carregar.pack(side='left', padx=5)

    # --- Formulário ---
    frame_form = tk.LabelFrame(frame_principal, text="Dados do Envolvido", padx=10, pady=10)
    frame_form.pack(fill='x', pady=10)

    # Campos do formulário
    campos = [
        ("Nome do Envolvido*:", tk.Entry(frame_form, width=40)),
        ("Papel/Função*:", ttk.Combobox(frame_form, values=["Gestor", "Desenvolvedor", "Analista", "Designer"], width=37)),
        ("Departamento:", tk.Entry(frame_form, width=40)),
        ("Coordenação:", tk.Entry(frame_form, width=40)),
        ("Contato (Email/Tel)*:", tk.Entry(frame_form, width=40)),
    ]
    
    for i, (label_text, widget) in enumerate(campos):
        tk.Label(frame_form, text=label_text).grid(row=i, column=0, sticky="e", pady=5)
        widget.grid(row=i, column=1, pady=5, padx=5)
        if label_text.startswith("Papel"):
            combo_papel = widget
    
    # Data de cadastro
    tk.Label(frame_form, text="Data de Cadastro:").grid(row=len(campos), column=0, sticky="e", pady=5)
    entry_data = tk.Entry(frame_form, width=40, state='disabled')
    entry_data.grid(row=len(campos), column=1, pady=5, padx=5)
    btn_data_hoje = tk.Button(frame_form, text="Hoje")
    btn_data_hoje.grid(row=len(campos), column=2, pady=5)

    # Variáveis para acesso aos campos
    entry_nome = campos[0][1]
    entry_departamento = campos[2][1]
    entry_coordenacao = campos[3][1]
    entry_contato = campos[4][1]

    # --- Lista de Envolvidos ---
    frame_lista = tk.LabelFrame(frame_principal, text="Envolvidos Cadastrados", padx=10, pady=10)
    frame_lista.pack(fill='both', expand=True)

    columns = ("ID", "Nome", "Papel", "Departamento", "Coordenação", "Contato", "Data", "Vinculado a")
    tree = ttk.Treeview(frame_lista, columns=columns, show="headings", height=8)
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor='w', stretch=True)

    vsb = ttk.Scrollbar(frame_lista, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame_lista, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    
    tree.grid(row=0, column=0, sticky='nsew')
    vsb.grid(row=0, column=1, sticky='ns')
    hsb.grid(row=1, column=0, sticky='ew')
    
    frame_lista.grid_rowconfigure(0, weight=1)
    frame_lista.grid_columnconfigure(0, weight=1)

    # --- Funções principais ---
    def limpar_campos():
        for entry in [entry_nome, entry_departamento, entry_coordenacao, entry_contato]:
            entry.delete(0, 'end')
        combo_papel.set('')
        entry_data.config(state='normal')
        entry_data.delete(0, 'end')
        entry_data.config(state='disabled')
        tree.selection_remove(tree.selection())
        combo_envolvidos_existentes.set('')

    def carregar_para_edicao():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um envolvido para editar")
            return

        item = tree.item(selecionado[0])
        entry_nome.delete(0, 'end')
        entry_nome.insert(0, item['values'][1])
        combo_papel.set(item['values'][2])
        entry_departamento.delete(0, 'end')
        entry_departamento.insert(0, item['values'][3])
        entry_coordenacao.delete(0, 'end')
        entry_coordenacao.insert(0, item['values'][4])
        entry_contato.delete(0, 'end')
        entry_contato.insert(0, item['values'][5])
        entry_data.config(state='normal')
        entry_data.delete(0, 'end')
        entry_data.insert(0, item['values'][6])
        entry_data.config(state='disabled')
        combo_envolvidos_existentes.set('')

    def salvar_envolvido():
        # Validação básica
        if not combo_envolvidos_existentes.get() and not entry_nome.get():
            messagebox.showwarning("Aviso", "Nome é obrigatório para novos cadastros!")
            return

        # Determinar vínculo
        tipo = tipo_selecionado.get()
        id_vinculado = None
        vinculado_a = "Projeto"
        
        if tipo == "tarefa":
            if not combo_tarefas_var.get():
                messagebox.showwarning("Aviso", "Selecione uma tarefa!")
                return
            id_vinculado = int(combo_tarefas_var.get().split(" - ")[0])
            vinculado_a = f"Tarefa: {combo_tarefas_var.get()}"
        elif tipo == "melhoria":
            if not combo_melhorias_var.get():
                messagebox.showwarning("Aviso", "Selecione uma melhoria!")
                return
            id_vinculado = int(combo_melhorias_var.get().split(" - ")[0])
            vinculado_a = f"Melhoria: {combo_melhorias_var.get()}"
        elif tipo == "tarefa_melhoria":
            if not combo_tarefas_melhorias_var.get():
                messagebox.showwarning("Aviso", "Selecione uma tarefa de melhoria!")
                return
            id_vinculado = int(combo_tarefas_melhorias_var.get().split(" - ")[0])
            vinculado_a = f"Tarefa Melhoria: {combo_tarefas_melhorias_var.get()}"

        conn = sqlite3.connect('gestao_projetos.db')
        cursor = conn.cursor()

        try:
            if tree.selection():  # Edição
                id_envolvido = tree.item(tree.selection()[0])['values'][0]
                cursor.execute('''
                    UPDATE envolvidos 
                    SET nome_envolvido=?, papel_envolvido=?, contato_envolvido=?, 
                        departamento=?, coordenacao=?, data_cadastro=?,
                        id_projeto=?, id_tarefa=?, id_melhoria=?, id_tarefa_melhoria=?
                    WHERE id=?
                ''', (
                    entry_nome.get(),
                    combo_papel.get(),
                    entry_contato.get(),
                    entry_departamento.get(),
                    entry_coordenacao.get(),
                    entry_data.get() if entry_data.get() else datetime.now().strftime("%d/%m/%Y"),
                    id_projeto if tipo == "projeto" else None,
                    id_vinculado if tipo == "tarefa" else None,
                    id_vinculado if tipo == "melhoria" else None,
                    id_vinculado if tipo == "tarefa_melhoria" else None,
                    id_envolvido
                ))
                mensagem = "Vínculo atualizado!"
            else:  # Novo cadastro ou reaproveitamento
                if combo_envolvidos_existentes.get():  # Reaproveitamento
                    id_original = int(combo_envolvidos_existentes.get().split(" - ")[0])
                    cursor.execute('''
                        INSERT INTO envolvidos 
                        (nome_envolvido, papel_envolvido, contato_envolvido, 
                         departamento, coordenacao, data_cadastro,
                         id_projeto, id_tarefa, id_melhoria, id_tarefa_melhoria)
                        SELECT nome_envolvido, papel_envolvido, contato_envolvido,
                               departamento, coordenacao, ?,
                               ?, ?, ?, ?
                        FROM envolvidos WHERE id=?
                    ''', (
                        datetime.now().strftime("%d/%m/%Y"),
                        id_projeto if tipo == "projeto" else None,
                        id_vinculado if tipo == "tarefa" else None,
                        id_vinculado if tipo == "melhoria" else None,
                        id_vinculado if tipo == "tarefa_melhoria" else None,
                        id_original
                    ))
                    mensagem = "Envolvido vinculado com sucesso!"
                else:  # Novo cadastro
                    if not combo_papel.get():
                        messagebox.showwarning("Aviso", "Papel/Função é obrigatório!")
                        return
                    
                    cursor.execute('''
                        INSERT INTO envolvidos 
                        (nome_envolvido, papel_envolvido, contato_envolvido, 
                         departamento, coordenacao, data_cadastro,
                         id_projeto, id_tarefa, id_melhoria, id_tarefa_melhoria)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        entry_nome.get(),
                        combo_papel.get(),
                        entry_contato.get(),
                        entry_departamento.get(),
                        entry_coordenacao.get(),
                        entry_data.get() if entry_data.get() else datetime.now().strftime("%d/%m/%Y"),
                        id_projeto if tipo == "projeto" else None,
                        id_vinculado if tipo == "tarefa" else None,
                        id_vinculado if tipo == "melhoria" else None,
                        id_vinculado if tipo == "tarefa_melhoria" else None
                    ))
                    mensagem = "Envolvido cadastrado com sucesso!"

            conn.commit()
            messagebox.showinfo("Sucesso", mensagem)
            limpar_campos()
            atualizar_lista()
            atualizar_comboboxes()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro no banco de dados: {str(e)}")
        finally:
            conn.close()

    def remover_envolvido():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um envolvido para remover")
            return

        if messagebox.askyesno("Confirmar", "Deseja remover este vínculo do envolvido?"):
            conn = sqlite3.connect('gestao_projetos.db')
            cursor = conn.cursor()

            try:
                cursor.execute('DELETE FROM envolvidos WHERE id=?', (tree.item(selecionado[0])['values'][0],))
                conn.commit()
                messagebox.showinfo("Sucesso", "Vínculo removido com sucesso!")
                limpar_campos()
                atualizar_lista()
                atualizar_comboboxes()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao remover: {str(e)}")
            finally:
                conn.close()

    def atualizar_globalmente():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um envolvido para atualizar")
            return

        nome_envolvido = tree.item(selecionado[0])['values'][1]
        
        if not messagebox.askyesno("Confirmar", f"Atualizar TODOS os registros de {nome_envolvido}?"):
            return

        dados = (
            entry_nome.get(),
            combo_papel.get(),
            entry_contato.get(),
            entry_departamento.get(),
            entry_coordenacao.get(),
            entry_data.get() if entry_data.get() else datetime.now().strftime("%d/%m/%Y"),
            nome_envolvido
        )

        conn = sqlite3.connect('gestao_projetos.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE envolvidos 
                SET nome_envolvido=?, papel_envolvido=?, contato_envolvido=?,
                    departamento=?, coordenacao=?, data_cadastro=?
                WHERE nome_envolvido=?
            ''', dados)
            
            conn.commit()
            messagebox.showinfo("Sucesso", f"Todos os registros de {nome_envolvido} foram atualizados!")
            limpar_campos()
            atualizar_lista()
            atualizar_comboboxes()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar: {str(e)}")
        finally:
            conn.close()

    def remover_globalmente():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um envolvido para remover")
            return

        nome_envolvido = tree.item(selecionado[0])['values'][1]
        
        if not messagebox.askyesno("Confirmar", f"Remover TODOS os registros de {nome_envolvido}?"):
            return

        conn = sqlite3.connect('gestao_projetos.db')
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM envolvidos WHERE nome_envolvido=?", (nome_envolvido,))
            conn.commit()
            messagebox.showinfo("Sucesso", f"Todos os registros de {nome_envolvido} foram removidos!")
            limpar_campos()
            atualizar_lista()
            atualizar_comboboxes()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao remover: {str(e)}")
        finally:
            conn.close()

    def atualizar_lista():
        conn = sqlite3.connect('gestao_projetos.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT e.id, e.nome_envolvido, e.papel_envolvido, e.departamento, 
                   e.coordenacao, e.contato_envolvido, e.data_cadastro,
                   CASE
                       WHEN e.id_projeto IS NOT NULL THEN 'Projeto'
                       WHEN e.id_tarefa IS NOT NULL THEN 'Tarefa: ' || (SELECT nome_tarefa FROM tarefas_projetos WHERE id = e.id_tarefa)
                       WHEN e.id_melhoria IS NOT NULL THEN 'Melhoria: ' || (SELECT nome_melhoria FROM melhorias WHERE id = e.id_melhoria)
                       WHEN e.id_tarefa_melhoria IS NOT NULL THEN 'Tarefa Melhoria: ' || 
                           (SELECT tm.nome_tarefa FROM tarefas_melhorias tm WHERE tm.id = e.id_tarefa_melhoria) || 
                           ' (' || (SELECT m.nome_melhoria FROM melhorias m JOIN tarefas_melhorias tm ON m.id = tm.id_melhoria WHERE tm.id = e.id_tarefa_melhoria) || ')'
                   END as vinculado_a
            FROM envolvidos e
            WHERE e.id_projeto = ? OR 
                  e.id_tarefa IN (SELECT id FROM tarefas_projetos WHERE id_projeto = ?) OR
                  e.id_melhoria IN (SELECT id FROM melhorias WHERE id_projeto = ?) OR
                  e.id_tarefa_melhoria IN (SELECT tm.id FROM tarefas_melhorias tm JOIN melhorias m ON tm.id_melhoria = m.id WHERE m.id_projeto = ?)
            ORDER BY e.nome_envolvido, vinculado_a
        ''', (id_projeto, id_projeto, id_projeto, id_projeto))
        
        registros = cursor.fetchall()
        conn.close()

        tree.delete(*tree.get_children())
        for reg in registros:
            tree.insert('', 'end', values=reg)

    def verificar_opcoes():
        conn = sqlite3.connect('gestao_projetos.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM tarefas_projetos WHERE id_projeto = ?", (id_projeto,))
        tem_tarefas = cursor.fetchone()[0] > 0
        
        cursor.execute("SELECT COUNT(*) FROM melhorias WHERE id_projeto = ?", (id_projeto,))
        tem_melhorias = cursor.fetchone()[0] > 0
        
        cursor.execute('''
            SELECT COUNT(*) FROM tarefas_melhorias tm
            JOIN melhorias m ON tm.id_melhoria = m.id
            WHERE m.id_projeto = ?
        ''', (id_projeto,))
        tem_tarefas_melhorias = cursor.fetchone()[0] > 0
        
        conn.close()
        
        rb_tarefa.config(state=tk.NORMAL if tem_tarefas else tk.DISABLED)
        rb_melhoria.config(state=tk.NORMAL if tem_melhorias else tk.DISABLED)
        rb_tarefa_melhoria.config(state=tk.NORMAL if tem_tarefas_melhorias else tk.DISABLED)
        
        if (tipo_selecionado.get() == "tarefa" and not tem_tarefas) or \
           (tipo_selecionado.get() == "melhoria" and not tem_melhorias) or \
           (tipo_selecionado.get() == "tarefa_melhoria" and not tem_tarefas_melhorias):
            tipo_selecionado.set("projeto")
        atualizar_comboboxes()

    def atualizar_comboboxes():
        conn = sqlite3.connect('gestao_projetos.db')
        cursor = conn.cursor()
        
        # Tarefas
        cursor.execute("SELECT id, nome_tarefa FROM tarefas_projetos WHERE id_projeto = ?", (id_projeto,))
        combo_tarefas['values'] = [f"{t[0]} - {t[1]}" for t in cursor.fetchall()]
        
        # Melhorias
        cursor.execute("SELECT id, nome_melhoria FROM melhorias WHERE id_projeto = ?", (id_projeto,))
        combo_melhorias['values'] = [f"{m[0]} - {m[1]}" for m in cursor.fetchall()]
        
        # Tarefas de melhorias
        cursor.execute('''
            SELECT tm.id, tm.nome_tarefa, m.nome_melhoria 
            FROM tarefas_melhorias tm
            JOIN melhorias m ON tm.id_melhoria = m.id
            WHERE m.id_projeto = ?
        ''', (id_projeto,))
        combo_tarefas_melhorias['values'] = [f"{tm[0]} - {tm[1]} ({tm[2]})" for tm in cursor.fetchall()]
        
        # Envolvidos existentes (agrupados por nome, sem repetição)
        cursor.execute('''
            SELECT MIN(id) as id, nome_envolvido, departamento 
            FROM envolvidos 
            GROUP BY nome_envolvido
            ORDER BY nome_envolvido
        ''')
        combo_envolvidos_existentes['values'] = [f"{e[0]} - {e[1]} ({e[2]})" for e in cursor.fetchall()]
        
        conn.close()
        
        # Mostrar/ocultar comboboxes conforme seleção
        tipo = tipo_selecionado.get()
        
        label_tarefas.pack_forget()
        combo_tarefas.pack_forget()
        label_melhorias.pack_forget()
        combo_melhorias.pack_forget()
        label_tarefas_melhorias.pack_forget()
        combo_tarefas_melhorias.pack_forget()
        
        if tipo == "tarefa" and combo_tarefas['values']:
            label_tarefas.pack(side='left', padx=5)
            combo_tarefas.pack(side='left', padx=5, fill='x', expand=True)
        elif tipo == "melhoria" and combo_melhorias['values']:
            label_melhorias.pack(side='left', padx=5)
            combo_melhorias.pack(side='left', padx=5, fill='x', expand=True)
        elif tipo == "tarefa_melhoria" and combo_tarefas_melhorias['values']:
            label_tarefas_melhorias.pack(side='left', padx=5)
            combo_tarefas_melhorias.pack(side='left', padx=5, fill='x', expand=True)

    def carregar_envolvido_existente():
        selecionado = combo_envolvidos_existentes.get()
        if not selecionado:
            return
            
        id_envolvido = int(selecionado.split(" - ")[0])
        conn = sqlite3.connect('gestao_projetos.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT nome_envolvido, papel_envolvido, contato_envolvido, 
                   departamento, coordenacao, data_cadastro
            FROM envolvidos WHERE id=?
        ''', (id_envolvido,))
        dados = cursor.fetchone()
        conn.close()
        
        if dados:
            entry_nome.delete(0, tk.END)
            entry_nome.insert(0, dados[0])
            combo_papel.set(dados[1])
            entry_contato.delete(0, tk.END)
            entry_contato.insert(0, dados[2])
            entry_departamento.delete(0, tk.END)
            entry_departamento.insert(0, dados[3])
            entry_coordenacao.delete(0, tk.END)
            entry_coordenacao.insert(0, dados[4])
            entry_data.config(state='normal')
            entry_data.delete(0, tk.END)
            entry_data.insert(0, dados[5])
            entry_data.config(state='disabled')

    # Configurar comandos dos botões
    btn_carregar.config(command=carregar_envolvido_existente)
    btn_data_hoje.config(command=lambda: entry_data.config(state='normal') or entry_data.delete(0, 'end') or 
                                      entry_data.insert(0, datetime.now().strftime("%d/%m/%Y")) or 
                                      entry_data.config(state='disabled'))
    
    rb_projeto.config(command=verificar_opcoes)
    rb_tarefa.config(command=verificar_opcoes)
    rb_melhoria.config(command=verificar_opcoes)
    rb_tarefa_melhoria.config(command=verificar_opcoes)

    # --- Botões otimizados para telas pequenas ---
    frame_botoes = tk.Frame(frame_principal)
    frame_botoes.pack(fill='x', pady=5)

    # Linha 1 - Ações básicas (2 botões)
    frame_linha1 = tk.Frame(frame_botoes)
    frame_linha1.pack(fill='x', pady=2)
    
    btn_novo = tk.Button(frame_linha1, text="Novo", command=limpar_campos)
    btn_novo.pack(side='left', expand=True, fill='x', padx=2)
    
    btn_editar = tk.Button(frame_linha1, text="Editar", command=carregar_para_edicao)
    btn_editar.pack(side='left', expand=True, fill='x', padx=2)

    # Linha 2 - Ações básicas (2 botões)
    frame_linha2 = tk.Frame(frame_botoes)
    frame_linha2.pack(fill='x', pady=2)
    
    btn_salvar = tk.Button(frame_linha2, text="Salvar", command=salvar_envolvido)
    btn_salvar.pack(side='left', expand=True, fill='x', padx=2)
    
    btn_remover = tk.Button(frame_linha2, text="Remover", command=remover_envolvido)
    btn_remover.pack(side='left', expand=True, fill='x', padx=2)

    # Linha 3 - Ações globais (2 botões)
    frame_linha3 = tk.Frame(frame_botoes)
    frame_linha3.pack(fill='x', pady=2)
    
    btn_atualizar = tk.Button(frame_linha3, text="Atualizar Todos", command=atualizar_globalmente, bg='#FFA500')
    btn_atualizar.pack(side='left', expand=True, fill='x', padx=2)
    
    btn_remover_todos = tk.Button(frame_linha3, text="Remover Todos", command=remover_globalmente, bg='#FF6347')
    btn_remover_todos.pack(side='left', expand=True, fill='x', padx=2)

    # Linha 4 - Voltar
    frame_linha4 = tk.Frame(frame_botoes)
    frame_linha4.pack(fill='x', pady=2)
    
    tk.Button(frame_linha4, text="Voltar", command=lambda: voltar_tela_inicial(root)).pack(fill='x')

    # Configuração adicional para o scroll com mouse
    canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

    # Inicialização
    verificar_opcoes()
    atualizar_lista()
    atualizar_comboboxes()

    # Eventos
    tree.bind('<Double-1>', lambda e: carregar_para_edicao())