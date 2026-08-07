from pathlib import Path

import pandas as pd

from utils.database import (
    get_connection,
    create_schemas,
    publish_dataframe,
    close_connection
)

# ======================================================
# Configurações
# ======================================================

RAW_PATH = Path("raw")
BRONZE_PATH = Path("bronze")

BRONZE_PATH.mkdir(exist_ok=True)

# ======================================================
# Conexão com o DuckDB
# ======================================================

con = get_connection()

create_schemas(con)

print("=" * 60)
print("INICIANDO CAMADA BRONZE")
print("=" * 60)

# ======================================================
# Processamento
# ======================================================

arquivos = list(RAW_PATH.glob("*"))

if len(arquivos) == 0:
    print("Nenhum arquivo encontrado na camada Raw.")
else:

    for arquivo in arquivos:

        print(f"\nLendo arquivo: {arquivo.name}")

        # --------------------------
        # Leitura
        # --------------------------

        if arquivo.suffix.lower() == ".csv":

            df = pd.read_csv(arquivo)

        elif arquivo.suffix.lower() == ".parquet":

            df = pd.read_parquet(arquivo)

        else:

            print(f"Arquivo ignorado: {arquivo.name}")
            continue

        # --------------------------
        # Padronização simples
        # --------------------------

        for coluna in df.select_dtypes(include=["object"]).columns:
            df[coluna] = df[coluna].fillna("").astype(str)

        # --------------------------
        # Salva Bronze
        # --------------------------

        nome_tabela = arquivo.stem

        destino = BRONZE_PATH / f"{nome_tabela}.parquet"

        df.to_parquet(destino, index=False)

        # --------------------------
        # Publica DuckDB
        # --------------------------

        publish_dataframe(
            con=con,
            dataframe=df,
            schema="bronze",
            table=nome_tabela
        )

        print(f"Tabela bronze.{nome_tabela} criada.")
        print(f"Arquivo salvo em {destino}")
        print(f"Registros: {len(df)}")

# ======================================================
# Encerramento
# ======================================================

close_connection(con)

print("\nCamada Bronze finalizada com sucesso.")
