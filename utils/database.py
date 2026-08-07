from sqlalchemy import create_engine, text
import pandas as pd

# ==========================================
# Configuração do Banco
# ==========================================

HOST = "127.0.0.1"
PORT = 3306

DATABASE = "projeto_agil_tcc"

USER = "root"
PASSWORD = "SUA_SENHA"

ENGINE = create_engine(
    f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}",
    pool_pre_ping=True
)


# ==========================================
# Publica DataFrame
# ==========================================

def publish_dataframe(
    df: pd.DataFrame,
    camada: str,
    tabela: str
):

    nome_tabela = f"{camada}_{tabela}"

    df.to_sql(
        nome_tabela,
        ENGINE,
        if_exists="replace",
        index=False
    )


# ==========================================
# Executa SQL
# ==========================================

def execute_sql(sql):

    with ENGINE.begin() as conn:
        conn.execute(text(sql))


# ==========================================
# Ler tabela
# ==========================================

def read_table(nome):

    return pd.read_sql(
        f"SELECT * FROM {nome}",
        ENGINE
    )
