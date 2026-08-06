from pathlib import Path

import duckdb
import pandas as pd

BRONZE_PATH = Path("bronze")
SILVER_PATH = Path("silver")
DATABASE = "database/dev_duckdb.duckdb"

SILVER_PATH.mkdir(exist_ok=True)

con = duckdb.connect(DATABASE)

con.execute("""
CREATE SCHEMA IF NOT EXISTS silver;
""")

for arquivo in BRONZE_PATH.glob("*.parquet"):

    df = pd.read_parquet(arquivo)

    nome = arquivo.stem

    destino = SILVER_PATH / arquivo.name

    df.to_parquet(destino, index=False)

    con.register("df_temp", df)

    con.execute(f"""
        CREATE OR REPLACE TABLE silver.{nome} AS
        SELECT *
        FROM df_temp
    """)

    print(f"Tabela silver.{nome} criada")

con.close()

print("Camada Silver concluída.")
