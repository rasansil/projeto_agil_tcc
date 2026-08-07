from pathlib import Path
import pandas as pd

RAW_PATH = Path("raw")
BRONZE_PATH = Path("bronze")

BRONZE_PATH.mkdir(exist_ok=True)

for arquivo in RAW_PATH.glob("*.parquet"):

    print(f"Copiando {arquivo.name}")

    df = pd.read_parquet(arquivo)

    df.to_parquet(
        BRONZE_PATH / arquivo.name,
        index=False
    )

print("Bronze criada.")
