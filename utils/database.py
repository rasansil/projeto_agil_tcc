from pathlib import Path

import yaml
import pandas as pd

from sqlalchemy import create_engine, text

# ======================================================
# Carregar configuração
# ======================================================

CONFIG_FILE = Path("config/database.yaml")

with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# ======================================================
# Configurações do banco
# ======================================================

HOST = config["host"]
PORT = config["port"]

DATABASE = config["database"]

USER = config["user"]
PASSWORD = config["password"]

# ======================================================
# Engine SQLAlchemy
# ======================================================

ENGINE = create_engine(
    f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}",
    pool_pre_ping=True,
    echo=False
)

# ======================================================
# Publicar DataFrame
# ======================================================

def publish_dataframe(
    df: pd.DataFrame,
    camada: str,
    tabela: str
):

    nome_tabela = f"{camada}_{tabela}"

    df.to_sql(
        name=nome_tabela,
        con=ENGINE,
        if_exists="replace",
        index=False
    )

# ======================================================
# Ler tabela
# ======================================================

def read_table(nome_tabela):

    return pd.read_sql(
        f"SELECT * FROM {nome_tabela}",
        ENGINE
    )

# ======================================================
# Executar SQL
# ======================================================

def execute_sql(sql):

    with ENGINE.begin() as conn:
        conn.execute(text(sql))

# ======================================================
# Verificar existência da tabela
# ======================================================

def table_exists(nome_tabela):

    sql = f"""
    SELECT COUNT(*)
    FROM information_schema.tables
    WHERE table_schema = '{DATABASE}'
      AND table_name = '{nome_tabela}'
    """

    with ENGINE.begin() as conn:
        return conn.execute(text(sql)).scalar() > 0

# ======================================================
# Excluir tabela
# ======================================================

def drop_table(nome_tabela):

    execute_sql(
        f"DROP TABLE IF EXISTS {nome_tabela}"
    )
