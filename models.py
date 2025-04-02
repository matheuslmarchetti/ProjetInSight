class Projeto:
    def __init__(self, id, nome, descricao, data_inicio, data_fim, status, prioridade, categoria):
        self.id = id
        self.nome = nome
        self.descricao = descricao
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.status = status
        self.prioridade = prioridade
        self.categoria = categoria

class Tarefa:
    def __init__(self, id, id_projeto, nome, descricao, data_inicio, data_fim, status, responsavel, prioridade):
        self.id = id
        self.id_projeto = id_projeto
        self.nome = nome
        self.descricao = descricao
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.status = status
        self.responsavel = responsavel
        self.prioridade = prioridade

class Melhoria:
    def __init__(self, id, id_projeto, descricao_melhoria, impacto_melhoria, data_inicio_melhoria, data_termino_melhoria, status_melhoria):
        self.id = id
        self.id_projeto = id_projeto
        self.descricao_melhoria = descricao_melhoria
        self.impacto_melhoria = impacto_melhoria
        self.data_inicio_melhoria = data_inicio_melhoria
        self.data_termino_melhoria = data_termino_melhoria
        self.status_melhoria = status_melhoria