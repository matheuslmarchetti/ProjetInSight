import sqlite3
import pandas as pd
import pyarrow.parquet as pq
from pathlib import Path

def exportar_para_parquet(caminho_db, diretorio_saida):
    """
    Exporta todas as tabelas do banco SQLite para arquivos Parquet
    
    Args:
        caminho_db (str): Caminho para o arquivo .db
        diretorio_saida (str): Pasta onde os arquivos serão salvos
    """
    # Criar diretório se não existir
    Path(diretorio_saida).mkdir(parents=True, exist_ok=True)
    
    # Conexão com o banco
    conn = sqlite3.connect(caminho_db)
    cursor = conn.cursor()
    
    # Obter lista de tabelas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tabelas = [t[0] for t in cursor.fetchall() if t[0] != 'sqlite_sequence']
    
    # Exportar cada tabela
    for tabela in tabelas:
        print(f"Exportando tabela: {tabela}")
        
        # Ler dados
        df = pd.read_sql_query(f"SELECT * FROM {tabela}", conn)
        
        # Tratar tipos de dados para compatibilidade com Parquet
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str)
        
        # Salvar em Parquet (com compressão Snappy)
        caminho_arquivo = Path(diretorio_saida) / f"{tabela}.parquet"
        df.to_parquet(
            caminho_arquivo,
            engine='pyarrow',
            compression='snappy',
            index=False
        )
        
        print(f"Salvo em: {caminho_arquivo}")
    
    conn.close()
    print("Exportação concluída!")

# Uso (substitua pelos seus caminhos)
if __name__ == "__main__":
    exportar_para_parquet(
        caminho_db='gestao_projetos.db',
        diretorio_saida='dados_parquet'
    )