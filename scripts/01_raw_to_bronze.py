from pathlib import Path

import pandas as pd

from utils.database import (
    get_connection,
    create_schemas,
    publish_dataframe,
    close_connection
)

RAW_PATH = Path("raw")
BRONZE_PATH = Path("bronze")

BRONZE_PATH.mkdir(exist_ok=True)

con = get_connection()

create_schemas(con)

for arquivo in RAW_PATH.glob("*.parquet"):

    print(f"Copiando {arquivo.name}")

    df = pd.read_parquet(arquivo)

    destino = BRONZE_PATH / arquivo.name

    df.to_parquet(destino, index=False)

    publish_dataframe(
        con,
        df,
        "bronze",
        arquivo.stem
    )

close_connection(con)

print("Camada Bronze criada com sucesso.")
