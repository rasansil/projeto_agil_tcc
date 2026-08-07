from pathlib import Path

import pandas as pd

from utils.database import (
    get_connection,
    publish_dataframe,
    close_connection
)

BRONZE_PATH = Path("bronze")
SILVER_PATH = Path("silver")

SILVER_PATH.mkdir(exist_ok=True)

con = get_connection()

for arquivo in BRONZE_PATH.glob("*.parquet"):

    print(f"Copiando {arquivo.name}")

    df = pd.read_parquet(arquivo)

    destino = SILVER_PATH / arquivo.name

    df.to_parquet(destino, index=False)

    publish_dataframe(
        con,
        df,
        "silver",
        arquivo.stem
    )

close_connection(con)

print("Camada Silver criada com sucesso.")
