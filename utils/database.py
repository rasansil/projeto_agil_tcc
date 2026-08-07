from pathlib import Path

import duckdb


DATABASE_PATH = Path("database/dev_duckdb.duckdb")


def get_connection():
    """
    Cria uma conexão com o banco DuckDB.
    Caso o banco não exista, ele será criado automaticamente.
    """

    DATABASE_PATH.parent.mkdir(exist_ok=True)

    return duckdb.connect(str(DATABASE_PATH))


def create_schemas(con):
    """
    Cria os schemas da arquitetura Medalhão.
    """

    con.execute("CREATE SCHEMA IF NOT EXISTS bronze;")
    con.execute("CREATE SCHEMA IF NOT EXISTS silver;")
    con.execute("CREATE SCHEMA IF NOT EXISTS gold;")


def publish_dataframe(con, dataframe, schema, table):
    """
    Publica um DataFrame como tabela no DuckDB.
    """

    con.register("df_temp", dataframe)

    con.execute(f"""
        CREATE OR REPLACE TABLE {schema}.{table} AS
        SELECT *
        FROM df_temp
    """)


def close_connection(con):
    """
    Fecha a conexão com o banco.
    """

    con.close()
