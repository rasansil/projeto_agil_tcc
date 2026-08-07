from pathlib import Path
import sys

# Adiciona a raiz do projeto ao PYTHONPATH
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
import pandas as pd

from utils.database import publish_dataframe

BRONZE_PATH = Path("bronze")
SILVER_PATH = Path("silver")

SILVER_PATH.mkdir(exist_ok=True)

for arquivo in BRONZE_PATH.glob("*.parquet"):

    print(f"Copiando {arquivo.name}")

    df = pd.read_parquet(arquivo)

    destino = SILVER_PATH / arquivo.name

    df.to_parquet(destino, index=False)

    publish_dataframe(
        df=df,
        camada="silver",
        tabela=arquivo.stem
    )

print("Silver criada com sucesso.")
