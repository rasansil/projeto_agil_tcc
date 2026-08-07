from pathlib import Path
import pandas as pd

from utils.database import publish_dataframe

RAW_PATH = Path("raw")
BRONZE_PATH = Path("bronze")

BRONZE_PATH.mkdir(exist_ok=True)

for arquivo in RAW_PATH.glob("*.parquet"):

    print(f"Copiando {arquivo.name}")

    df = pd.read_parquet(arquivo)

    destino = BRONZE_PATH / arquivo.name

    df.to_parquet(destino, index=False)

    publish_dataframe(
        df=df,
        camada="bronze",
        tabela=arquivo.stem
    )

print("Bronze criada com sucesso.")
