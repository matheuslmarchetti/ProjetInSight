# import sqlite3

# # # Conectar ao banco de dados
# # conn = sqlite3.connect('gestao_projetos.db')
# # cursor = conn.cursor()

# # # Renomear a tabela
# # try:
# #     cursor.execute("ALTER TABLE tarefas RENAME TO tarefas_projetos;")
# #     conn.commit()  # Confirmar a alteração
# #     print("Tabela renomeada com sucesso!")
# # except sqlite3.OperationalError as e:
# #     print(f"Erro ao renomear a tabela: {e}")

# # # Fechar a conexão
# # conn.close()


# # Conectar ao banco de dados (ou criar se não existir)
# conn = sqlite3.connect('gestao_projetos.db')
# cursor = conn.cursor()

# # Listar todas as tabelas no banco de dados
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# tables = cursor.fetchall()

# # Excluir todas as tabelas, exceto a tabela interna `sqlite_sequence`
# for table in tables:
#     table_name = table[0]
#     if table_name != "sqlite_sequence":  # Ignorar a tabela `sqlite_sequence`
#         cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
#         print(f"Tabela {table_name} excluída.")

# # Commit para salvar as alterações
# conn.commit()

# # Fechar a conexão
# conn.close()

# # Conectar ao banco de dados
# conn = sqlite3.connect('gestao_projetos.db')
# cursor = conn.cursor()

# # Consulta para listar as tabelas
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# tabelas = cursor.fetchall()

# # Exibir as tabelas
# print("Tabelas no banco de dados:")
# for tabela in tabelas:
#     print(tabela[0])

# # Fechar a conexão
# conn.close()


# # Conectar ao banco de dados
# conn = sqlite3.connect('gestao_projetos.db')
# cursor = conn.cursor()

# # Lista de todas as tabelas do banco
# tabelas = ['projetos', 'tarefas_melhorias', 'tarefas_projetos', 'melhorias', 'envolvidos']  # Substitua pelos nomes reais das suas tabelas

# # Limpar cada tabela e resetar a numeração do ID
# for tabela in tabelas:
#     # Deletar todos os registros
#     cursor.execute(f"DELETE FROM {tabela};")
#     # Resetar o contador de auto-incremento (SQLite)
#     cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{tabela}';")

# # Confirmar as alterações e fechar a conexão
# conn.commit()
# conn.close()