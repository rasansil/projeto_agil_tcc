from pathlib import Path
import pandas as pd

BRONZE_PATH = Path("bronze")
SILVER_PATH = Path("silver")

SILVER_PATH.mkdir(exist_ok=True)

for arquivo in BRONZE_PATH.glob("*.parquet"):

    print(f"Copiando {arquivo.name}")

    df = pd.read_parquet(arquivo)

    df.to_parquet(
        SILVER_PATH / arquivo.name,
        index=False
    )

print("Silver criada.")
