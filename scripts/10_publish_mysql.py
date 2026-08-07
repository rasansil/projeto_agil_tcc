from pathlib import Path

import pandas as pd

from utils.database import publish_dataframe

CAMADAS = {

    "bronze": Path("bronze"),

    "silver": Path("silver"),

    "gold": Path("gold")
}

for camada, pasta in CAMADAS.items():

    if not pasta.exists():
        continue

    for arquivo in pasta.glob("*.parquet"):

        print(f"Publicando {arquivo.name}")

        df = pd.read_parquet(arquivo)

        publish_dataframe(
            df,
            f"{camada}_{arquivo.stem}"
        )

print("Publicação concluída.")
