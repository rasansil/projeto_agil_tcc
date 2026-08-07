from sqlalchemy import create_engine
import pandas as pd

# ======================================
# CONFIGURAÇÃO MYSQL
# ======================================

HOST = "localhost"
PORT = 3306

DATABASE = "projeto_agil_tcc"

USER = "root"
PASSWORD = "SUA_SENHA"

engine = create_engine(
    f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
)

# ======================================
# PUBLICAR DATAFRAME
# ======================================

def publish_dataframe(df: pd.DataFrame,
                      camada: str,
                      tabela: str):

    nome_tabela = f"{camada}_{tabela}"

    df.to_sql(
        nome_tabela,
        con=engine,
        if_exists="replace",
        index=False
    )
